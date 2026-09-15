import json
import os
import re
import urllib.request

from pypdf import PdfReader


# =========================
# AI Configuration
# =========================

AI_API_URL = os.environ.get(
    "AI_API_URL",
    "http://localhost:11434/v1/chat/completions"
)

AI_API_KEY = os.environ.get("AI_API_KEY", "")
AI_MODEL = os.environ.get("AI_MODEL", "qwen3:8b")


# =========================
# PDF Extraction
# =========================

def extract_pdf_text(file_path):
    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text.strip()


# =========================
# AI Request
# =========================

def ask_local_ai(prompt, history=None, json_mode=False):

    messages = []

    if history:
        messages.extend(history)

    messages.append({
        "role": "user",
        "content": prompt
    })

    payload = {
        "model": AI_MODEL,
        "messages": messages,
        "stream": False,
        "temperature": 0.2
    }

    if json_mode:
        payload["response_format"] = {
            "type": "json_object"
        }

    data = json.dumps(payload).encode("utf-8")

    headers = {
        "Content-Type": "application/json"
    }

    if AI_API_KEY:
        headers["Authorization"] = f"Bearer {AI_API_KEY}"

    request = urllib.request.Request(
        AI_API_URL,
        data=data,
        headers=headers,
        method="POST"
    )

    try:

        with urllib.request.urlopen(request, timeout=120) as response:

            result = json.loads(
                response.read().decode("utf-8")
            )

        return result["choices"][0]["message"]["content"]

    except Exception as e:

        raise RuntimeError(
            f"AI connection failed: {str(e)}"
        )


# =========================
# JSON Extraction
# =========================

def extract_json(text):

    text = text.strip()

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

    try:

        return json.loads(text)

    except json.JSONDecodeError:
        pass

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