import json
import re
import urllib.request

from pypdf import PdfReader


OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "qwen3:8b"


def extract_pdf_text(file_path):
    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text.strip()


def ask_local_ai(prompt, history=None, json_mode=False):
    messages = []

    if history:
        messages.extend(history)

    messages.append({
        "role": "user",
        "content": prompt
    })

    payload = {
        "model": OLLAMA_MODEL,
        "messages": messages,
        "stream": False,
        "think": False
    }

    # Force Ollama to return valid JSON
    # when the feature needs structured data.
    if json_mode:
        payload["format"] = "json"

    data = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        OLLAMA_URL,
        data=data,
        headers={
            "Content-Type": "application/json"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(
            request,
            timeout=120
        ) as response:

            result = json.loads(
                response.read().decode("utf-8")
            )

        return result["message"]["content"]

    except Exception as e:
        raise RuntimeError(
            f"Local AI connection failed: {str(e)}"
        )


def extract_json(text):
    text = text.strip()

    # Remove markdown code fences if the AI adds them.
    text = re.sub(
        r"```json\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"```\s*",
        "",
        text
    )

    # First try to parse the complete response.
    try:
        return json.loads(text)

    except json.JSONDecodeError:
        pass

    # Try to extract a JSON object.
    start_object = text.find("{")
    end_object = text.rfind("}")

    if start_object != -1 and end_object != -1:

        candidate = text[
            start_object:end_object + 1
        ]

        try:
            return json.loads(candidate)

        except json.JSONDecodeError:
            pass

    # Try to extract a JSON array.
    start_array = text.find("[")
    end_array = text.rfind("]")

    if start_array != -1 and end_array != -1:

        candidate = text[
            start_array:end_array + 1
        ]

        try:
            return json.loads(candidate)

        except json.JSONDecodeError:
            pass

    raise ValueError(
        "The AI returned a response that could not be parsed as JSON."
    )