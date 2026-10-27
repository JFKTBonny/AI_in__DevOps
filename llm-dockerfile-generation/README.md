# LLM-Powered Dockerfile Generator

This chapter contains two Python examples that generate a Dockerfile draft
from a programming-language name:

| Script | Provider | Model |
|---|---|---|
| `generate_dockerfile_ollama.py` | Local Ollama service | `llama3.2:1b` |
| `generate_dockerfile_gemini.py` | Gemini API | `gemini-2.5-flash` by default |

Both scripts print the generated Dockerfile to the terminal. They do not
inspect your project, save a file, build an image, or verify that the result
works. Treat the output as a starting point and review it before use.

## Requirements

- Python 3.9 or newer
- For Ollama: Ollama installed and running on your machine
- For Gemini: a Gemini API key and internet access

## 1. Install Python dependencies

Run these commands from this directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

On Windows PowerShell, activate the environment with:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## 2. Choose a provider

### Option A: Ollama (local model)

Make sure the Ollama service is running. If it is not already running, start
it in a separate terminal:

```bash
ollama serve
```

Download the model used by the script:

```bash
ollama pull llama3.2:1b
```

Run the generator:

```bash
python3 generate_dockerfile_ollama.py
```

### Option B: Gemini API

Set your API key in the environment. Do not put the key in the Python file or
commit it to the repository.

Linux or macOS:

```bash
export GEMINI_API_KEY="your-api-key"
python3 generate_dockerfile_gemini.py
```

Windows PowerShell:

```powershell
$env:GEMINI_API_KEY = "your-api-key"
python generate_dockerfile_gemini.py
```

The script uses `gemini-2.5-flash` by default. To use a different model
available to your account, set `GEMINI_MODEL` before running it.

## 3. Enter a language

When prompted, enter a language or runtime, for example:

```text
Enter the programming language: Python
```

The generated Dockerfile appears in the terminal. Copy it into your project
only after reviewing and adapting it.

## Review before using the output

A language name alone may not provide enough information to generate a
working Dockerfile. Check that the result matches your project's runtime
version, dependency files, build and start commands, ports, and directory
layout. Also review the base image, permissions, copied files, and handling of
secrets. Build and test the image in a suitable environment before deployment.

For background on how the examples work and additional review guidance, see
[`notes.txt`](notes.txt).
