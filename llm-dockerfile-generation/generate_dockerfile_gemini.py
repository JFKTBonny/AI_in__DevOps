import os

from google import genai


PROMPT = """
Generate a Dockerfile for {language} using practical security and build best
practices. Include a base image, dependency installation, working directory,
source copy, and startup command. Return only the Dockerfile.
"""


def generate_dockerfile(language):
    """Generate a Dockerfile using the Gemini API."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set.")

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=os.environ.get("GEMINI_MODEL", "gemini-2.5-flash"),
        contents=PROMPT.format(language=language),
    )
    if not response.text:
        raise RuntimeError("Gemini returned an empty response.")
    return response.text


if __name__ == "__main__":
    language = input("Enter the programming language: ").strip()
    if not language:
        raise SystemExit("Please provide a programming language.")
    dockerfile = generate_dockerfile(language)
    print("\nGenerated Dockerfile:\n")
    print(dockerfile)
