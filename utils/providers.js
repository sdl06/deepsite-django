export const PROVIDERS = {
  "fireworks-ai": {
    name: "Fireworks AI",
    max_tokens: 131_000,
    id: "fireworks-ai",
  },
  nebius: {
    name: "Nebius AI Studio",
    max_tokens: 131_000,
    id: "nebius",
  },
  sambanova: {
    name: "SambaNova",
    max_tokens: 8_000,
    id: "sambanova",
  },
  novita: {
    name: "NovitaAI",
    max_tokens: 16_000,
    id: "novita",
  },
  // hyperbolic: {
  //   name: "Hyperbolic",
  //   max_tokens: 131_000,
  //   id: "hyperbolic",
  // },
  local: {
    name: "Local (Ollama)",
    max_tokens: 131_000,
    id: "local",
  },
  // openai: {
  //   name: "OpenAI",
  //   max_tokens: 131_000,
  //   id: "openai",
  //   model: process.env.OPENAI_MODEL || "gpt-3.5-turbo",
  //   base_url: process.env.OPENAI_API_URL || "https://api.openai.com/v1",
  //   api_key: process.env.OPENAI_API_KEY,
  // }
};
