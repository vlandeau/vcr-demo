# VCR Demo

THis repo has been used for demonstrating the use of 
[pytest-recording](https://github.com/kiwicom/pytest-recording/tree/master) 
during the 2025 Voxxed Days Luxembourg conference.

It reproduces a really simplified version of [UPGRAIL](https://upgrail.ekinox.io),
especially its test-suite generation feature.

What you should do before running the tests:
1. Install the dependencies:
   ```bash
   uv sync
   ```
2. Launch ollama server if you want to use ollama model:
   ```bash
   ollama run <ollama-model-name>
   ```
3.Create a `.env` file from the provided `.env.template` and fill in the required environment variables:
OPENAI_API_KEY=your_openai_api_key
OLLAMA_MODEL_NAME=ollama-model-name
