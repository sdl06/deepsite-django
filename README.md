# DeepSite Locally 🚀

Run **DeepSite** on your own environment, without depending on Hugging Face!  
Perfect for those who want to customize, integrate, or simply have full control over the platform.

---

## How to run it locally 🔥

### 1. Clone the repository
```bash
git clone https://github.com/MartinsMessias/deepsite-locally.git
```

### 2. Install dependencies
(Make sure you have **Node.js** installed)
```bash
npm install
```

### 3. Set up your environment

Create a `.env` file in the project root and add your **HF_TOKEN**:

```
HF_TOKEN=your-token-here
```
> The token must have **inference** permissions (and **write** permissions if you want to deploy results to Hugging Face Spaces).

### 4. Build the project
```bash
npm run build
```

### 5. Start the server
```bash
npm run start
```


