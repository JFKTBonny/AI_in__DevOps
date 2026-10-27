from groq_client import generate


PROMPT = """
These examples show Kubernetes Deployment commands:

1. Create a Deployment:
   kubectl create deployment nginx --image=nginx
2. List that Deployment:
   kubectl get deployment nginx
3. Inspect that Deployment:
   kubectl describe deployment nginx

Following the same command-line context, provide a command to scale the
Deployment named nginx to five replicas. Do not execute it or suggest another
cluster change. Briefly remind the user to verify the active context and
namespace before applying it.
"""


if __name__ == "__main__":
    print(generate(PROMPT))
