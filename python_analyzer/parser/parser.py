import base64
import json
import json5
import os
import time

import requests
from dotenv import load_dotenv

from .prompts import CONTINUE_PROMPT, STOP_WORD, STRUCTURED_OUTPUT_PROMPT

OPENROUTER_CHAT_URL = "https://openrouter.ai/api/v1/chat/completions"


def _encode_pdf_to_base64(pdf_path: str) -> str:
    with open(pdf_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    return f"data:application/pdf;base64,{b64}"


def preprocess_text(text: str) -> str:
    lines = text.splitlines()
    result = []
    for line in lines:
        result.append(line.lstrip())
    text = "".join(result)
    text = text.replace("\n", "").replace("\\n", " ")
    text = text.replace("```json", "").replace("```", "")
    text = text.strip()
    return text


def remove_trailing_object(text: str) -> str:
    for i in range(len(text) - 1, -1, -1):
        if text[i - 2 : i + 1] == "},{":
            return text[:i]
    return text


def cleanup_json(input_text: str) -> str:
    input_str = input_text
    try:
        parsed = json.loads(input_str)
        return json.dumps(parsed)
    except json.JSONDecodeError:
        try:
            parsed = json5.loads(input_str)
            return json5.dumps(parsed)
        except Exception as e:
            print("Error: Failed to parse JSON file")
            print(e)
    return input_str


def get_file_name(file_path: str) -> str:
    return os.path.basename(file_path).split(".")[0]


def _send_with_retry(api_key: str, model: str, messages: list, plugins: list | None = None):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {"model": model, "messages": messages}
    if plugins:
        payload["plugins"] = plugins
    attempts = 0
    max_attempts = 10
    while attempts < max_attempts:
        try:
            r = requests.post(OPENROUTER_CHAT_URL, headers=headers, json=payload, timeout=120)
            r.raise_for_status()
            data = r.json()
            return data
        except Exception as e:
            print("Error: Failed to send prompt", getattr(e, "message", str(e)))
            attempts += 1
            time.sleep(1)
    raise Exception("Max retry attempts reached. Failed to send message.")


class Parser:
    """
    Parser class for parsing PDF files and returning a string in JSON format.
    Uses OpenRouter with gemini-2.0-flash-lite (or configurable model).
    """

    DEFAULT_MODEL = "google/gemini-2.0-flash-lite-001"

    def __init__(self, model: str | None = None, api_key: str | None = None):
        if api_key is None:
            load_dotenv()
            api_key = os.getenv("OPENROUTER_API_KEY")
        if api_key is None:
            raise ValueError("OPENROUTER_API_KEY must be set (env or api_key=)")
        self._api_key = api_key
        self.model = model or self.DEFAULT_MODEL

    def parse_pdf(self, pdf_path: str, temp_out_dir: str = "") -> str:
        temp_out_path = (
            temp_out_dir
            + get_file_name(pdf_path)
            + "_"
            + time.strftime("%Y%m%d-%H-%M-%S")
            + ".json"
        )
        parsed_text = ""

        pdf_filename = os.path.basename(pdf_path)
        file_data = _encode_pdf_to_base64(pdf_path)

        initial_content = [
            {"type": "text", "text": STRUCTURED_OUTPUT_PROMPT},
            {
                "type": "file",
                "file": {
                    "filename": pdf_filename,
                    "file_data": file_data,
                },
            },
        ]

        plugins = [
            {
                "id": "file-parser",
                "pdf": {"engine": "pdf-text"},
            },
        ]

        messages = [{"role": "user", "content": initial_content}]

        prompts = 1
        continue_prompting = False
        print("sending initial prompt " + str(prompts))

        response = _send_with_retry(
            self._api_key,
            self.model,
            messages,
            plugins=plugins,
        )
        content = ""
        file_annotations = None
        if response.get("choices") and len(response["choices"]) > 0:
            msg = response["choices"][0].get("message") or {}
            content = msg.get("content") or ""
            file_annotations = msg.get("annotations")
            text = preprocess_text(content or "")

            if STOP_WORD in text:
                text = text.replace(STOP_WORD, "")
                continue_prompting = True
            else:
                text = remove_trailing_object(text)

            parsed_text += text
            if temp_out_dir:
                with open(temp_out_path, "w", encoding="utf-8") as f:
                    f.write(text)

            # Build annotation-based continuation history (no PDF resend).
            # First assistant message carries annotations so OpenRouter reuses pre-parsed doc.
            if file_annotations:
                continuation_messages = [
                    {"role": "user", "content": STRUCTURED_OUTPUT_PROMPT},
                    {"role": "assistant", "content": content, "annotations": file_annotations},
                ]
            else:
                continuation_messages = None  # fallback: will resend full messages with PDF

            while not continue_prompting and prompts <= 5:
                prompts += 1
                print("sending prompt " + str(prompts))
                if continuation_messages is not None:
                    continuation_messages.append({"role": "user", "content": CONTINUE_PROMPT})
                    follow_up_messages = continuation_messages
                else:
                    # Fallback: no annotations, resend full conversation with PDF
                    messages.append({"role": "assistant", "content": content})
                    messages.append({"role": "user", "content": CONTINUE_PROMPT})
                    follow_up_messages = messages

                response = _send_with_retry(
                    self._api_key,
                    self.model,
                    follow_up_messages,
                    plugins=plugins,
                )
                content = ""
                if response.get("choices") and len(response["choices"]) > 0:
                    msg = response["choices"][0].get("message") or {}
                    content = msg.get("content") or ""
                    if msg.get("annotations"):
                        file_annotations = msg["annotations"]
                if continuation_messages is not None:
                    continuation_messages.append({"role": "assistant", "content": content})
                text = preprocess_text(content or "")
                if "[" in text[:5]:
                    text = text.replace("[", "", 1)
                if STOP_WORD in text:
                    text = text.replace(STOP_WORD, "")
                    continue_prompting = True
                else:
                    text = remove_trailing_object(text)
                parsed_text += text
                if temp_out_dir:
                    with open(temp_out_path, "a", encoding="utf-8") as f:
                        f.write(text)

        print("prompting finished with " + str(prompts) + " prompts")
        print("initiating json cleanup")
        json_text = cleanup_json(parsed_text)
        print("json cleanup finished")
        print("parsing completed")
        return json_text


def main():
    load_dotenv()
    api_key = os.getenv("OPENROUTER_API_KEY")
    parser = Parser(api_key=api_key)
    output = parser.parse_pdf(
        pdf_path="2024_MED.pdf",
        temp_out_dir="../out/",
    )
    with open("2024_MED_FINAL.json", "w", encoding="utf-8") as f:
        f.write(output)
    print("2024_MED_FINAL.json saved")


if __name__ == "__main__":
    main()
