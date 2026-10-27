from groq_client import generate


PROMPT = """
Explain what `kubectl get pods` does for a DevOps beginner.
Cover its default namespace scope, how to request pods from all namespaces,
common output columns, and why pod STATUS can be values other than Running
or Pending. Do not suggest changing cluster resources. Use a concise
explanation and read-only command examples only.
"""


if __name__ == "__main__":
    print(generate(PROMPT))
