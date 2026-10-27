import ollama


PROMPT = """
Generate a Dockerfile for {language} using practical security and build best
practices. Include a base image, dependency installation, working directory,
source copy, and startup command. Return only the Dockerfile.
"""


def generate_dockerfile(language):
    """Generate a Dockerfile using the locally running Ollama service."""
    response = ollama.chat(
        model="llama3.2:1b",
        messages=[{"role": "user", "content": PROMPT.format(language=language)}],
    )
    return response["message"]["content"]


if __name__ == "__main__":
    language = input("Enter the programming language: ").strip()
    if not language:
        raise SystemExit("Please provide a programming language.")
    dockerfile = generate_dockerfile(language)
    print("\nGenerated Dockerfile:\n")
    print(dockerfile)