import os
from dotenv import load_dotenv
import google.generativeai as genai


def main() -> None:
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise SystemExit("GEMINI_API_KEY not set")

    genai.configure(api_key=api_key)

    for model in genai.list_models():
        methods = getattr(model, "supported_generation_methods", []) or []
        methods_text = ", ".join(methods) if methods else "(no methods)"
        print(f"{model.name} | {methods_text}")


if __name__ == "__main__":
    main()
