import json
import os
from django.http import JsonResponse, StreamingHttpResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import requests
from .providers import PROVIDERS

SYSTEM_PROMPT = (
    'ONLY USE HTML, CSS AND JAVASCRIPT. No explanations, ONLY CODE. If you want to use ICON make sure to import the library first. '
    'Try to create the best UI possible by using only HTML, CSS and JAVASCRIPT. Use as much as you can TailwindCSS for the CSS, '
    'if you can\'t do something with TailwindCSS, then use custom CSS (make sure to import <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script> in the head). '
    'Also, try to ellaborate as much as you can, to create something unique. ALWAYS GIVE THE RESPONSE INTO A SINGLE HTML FILE'
)

@csrf_exempt
def ask_ai(request):
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'message': 'Invalid method'}, status=405)
    try:
        body = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        body = {}
    prompt = body.get('prompt')
    html = body.get('html')
    previous_prompt = body.get('previousPrompt')
    provider = body.get('provider')

    if not prompt:
        return JsonResponse({'ok': False, 'message': 'Missing required fields'}, status=400)

    tokens_used = len(prompt)
    if previous_prompt:
        tokens_used += len(previous_prompt)
    if html:
        tokens_used += len(html)

    default_provider = PROVIDERS['openrouter']
    selected = default_provider if provider == 'auto' else PROVIDERS.get(provider, default_provider)

    if provider != 'auto' and tokens_used >= selected['max_tokens']:
        return JsonResponse({
            'ok': False,
            'openSelectProvider': True,
            'message': f"Context is too long. {selected['name']} allow {selected['max_tokens']} max tokens."
        }, status=400)

    if selected['id'] in ['local', 'openrouter']:
        api_key = body.get('ApiKey')
        api_url = body.get('ApiUrl')
        model = body.get('Model')
        if not api_url or not model:
            return JsonResponse({'ok': False, 'message': 'Missing required fields for provider, set API KEY, BASE URL, and MODEL.'}, status=400)

        payload = {
            'model': model,
            'messages': [
                {'role': 'system', 'content': SYSTEM_PROMPT},
            ]
        }
        if previous_prompt:
            payload['messages'].append({'role': 'user', 'content': previous_prompt})
        if html:
            payload['messages'].append({'role': 'assistant', 'content': f'The current code is: {html}.'})
        payload['messages'].append({'role': 'user', 'content': prompt})
        payload['stream'] = True

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }

        try:
            response = requests.post(f"{api_url}/chat/completions", json=payload, headers=headers, stream=True)
        except Exception as exc:
            return JsonResponse({'ok': False, 'message': str(exc)}, status=500)

        if not response.ok:
            return JsonResponse({'ok': False, 'message': f"API Error: {response.status_code} - {response.text}"}, status=response.status_code)

        def stream():
            for line in response.iter_lines():
                if not line:
                    continue
                line = line.decode()
                if not line.startswith('data: ') or '[DONE]' in line:
                    if 'exceeded' in line:
                        yield json.dumps({'ok': False, 'message': line})
                        return
                    continue
                try:
                    json_str = line[6:].strip()
                    if not json_str.startswith('{'):
                        continue
                    message = json.loads(json_str)
                    content = message.get('choices', [{}])[0].get('delta', {}).get('content')
                    if content:
                        yield content
                except Exception:
                    continue
        resp = StreamingHttpResponse(stream(), content_type='text/plain')
        resp['Cache-Control'] = 'no-cache'
        resp['Connection'] = 'keep-alive'
        return resp

    return JsonResponse({'ok': False, 'message': 'Provider not supported'}, status=400)

def index(request):
    path = settings.BASE_DIR / 'dist' / 'index.html'
    return FileResponse(open(path, 'rb'))
