from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
from .prompts import *
import json
import json5
import time

def preprocess_text(text: str) -> str:
    lines = text.splitlines()
    result = []
    for line in lines:
        result.append(line.lstrip())
    text = ''.join(result)
    text = text.replace("\n", "").replace("\\n", " ")
    text = text.replace("```json", "").replace("```", "")
    text = text.strip()
    return text

def remove_trailing_object(text: str) -> str:
    for i in range(len(text) - 1, -1, -1):
        if text[i-2:i+1] == "},{":
            return text[:i]
    return text


def cleanup_json(json_text: str) -> str:
    try:
        json_text = json.loads(json_text)
        json_text = json.dumps(json_text)
    except json.JSONDecodeError:
        try:
            json_text = json5.loads(json_text)
            json_text = json5.dumps(json_text)
        except Exception as e:
            print("Error: Failed to parse JSON file")
            print(e)
            json_text = None
    return json_text

def get_file_name(file_path: str) -> str:
    return os.path.basename(file_path).split(".")[0]

class Parser:
    """
    Parser class for parsing PDF files and returning a string in JSON format.
    """
    def __init__(self, model: str = "gemini-2.0-flash-lite", api_key: str = None):
        if api_key is None:
            load_dotenv()  # Load environment variables from .env file
            api_key = os.getenv('GEMINI_API_KEY')  # Get the environment variable
        self.client: genai.Client = genai.Client(api_key=api_key)
        self.model: str = model


    def parse_pdf(self, pdf_path: str, temp_out_dir: str = "") -> str:
        temp_out_path = temp_out_dir + get_file_name(pdf_path) + "_" + time.strftime("%Y%m%d-%H-%M-%S") + ".json"
        parsed_text = ""
        # upload the file
        file = self.client.files.upload(file=pdf_path)
        file_data = types.FileData(
            file_uri=file.uri,
            mime_type=file.mime_type
        )

        # # Initialize the chat
        chat = self.client.chats.create(model=self.model)
        
        # send initial message
        prompts = 1
        continue_prompting = False
        print("sending initial prompt " + str(prompts))
        response = chat.send_message(
            message=[
                types.Part(file_data=file_data),
                types.Part(text=STRUCTURED_OUTPUT_PROMPT)
            ]
        )

        text = preprocess_text(response.text)
        if STOP_WORD in text:
            text = text.replace(STOP_WORD, "")
            continue_prompting = True
        else:
            text = remove_trailing_object(text)

        parsed_text += text
        if temp_out_dir != "":
            with open(temp_out_path, "w", encoding="utf-8") as f:
                f.write(text)

        while not continue_prompting and prompts <= 5:
            prompts += 1
            print("sending prompt " + str(prompts))
            response = chat.send_message(message=[
                types.Part(text=CONTINUE_PROMPT),
            ])
            text = preprocess_text(response.text)
            if "[" in text[:5]:
                text = text.replace("[", "", 1)
            if STOP_WORD in text:
                text = text.replace(STOP_WORD, "")
                continue_prompting = True
            else:
                text = remove_trailing_object(text)
            parsed_text += text
            if temp_out_dir != "":
                with open(temp_out_path, "a", encoding="utf-8") as f:
                    f.write(text)

        print("prompting finished with " + str(prompts) + " prompts")
        print("initiating json cleanup")
        json_text = cleanup_json(parsed_text)
        print("json cleanup finished")

        # clean up gemini file
        print("initializing clean up")
        self.client.files.delete(name=file.name)
        print("clean up finished")

        print("parsing completed")
        return json_text


def main():
    load_dotenv() 
    gemini_api_key = os.getenv('GEMINI_API_KEY') 
    parser = Parser(api_key=gemini_api_key)
    output = parser.parse_pdf(
        pdf_path="2024_MED.pdf", 
        temp_out_dir="../out/"
    )
    with open("2024_MED_FINAL.json", "w", encoding="utf-8") as f:
        json.dump(output, f)
    print("2024_MED_FINAL.json saved")

if __name__ == "__main__":
    main()
