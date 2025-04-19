from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
from prompts import *

def preprocess_text(text: str) -> str:
    text = text.replace("\n", "").replace("\\n", " ")
    text = text.replace("```json", "").replace("```", "")
    text = text.strip()
    return text

def remove_trailing_object(text: str) -> str:
    for i in range(len(text) - 1, -1, -1):
        if text[i-3:i] == "},{":
            return text[:i-1]
    return text

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


    def parse_pdf(self, pdf_path: str, out_path: str = "response.txt") -> str:
        
        # upload the file
        file = self.client.files.upload(file=pdf_path)
        file_data = types.FileData(
            file_uri=file.uri,
            mime_type=file.mime_type
        )

        # Initialize the chat
        chat = self.client.chats.create(model=self.model)
        
        # send initial message
        prompts = 1
        continue_prompting = False
        print("sending initial message " + str(prompts))
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
        
        with open(out_path, "w") as f:
            f.write(text)

        print("saved response to file " + out_path)

        while not continue_prompting and prompts <= 5:
            prompts += 1

            print("sending message " + str(prompts))
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

            with open(out_path, "a") as f:
                f.write(text)

        print("prompting finished with " + str(prompts) + " prompts")

        # clean up
        print("initializing clean up")
        delete_response = self.client.files.delete(name=file.name)
        print("clean up finished")

        return ""


def main():
    load_dotenv() 
    gemini_api_key = os.getenv('GEMINI_API_KEY') 

    parser = Parser(api_key=gemini_api_key)
    output = parser.parse_pdf("2026_MED.pdf", "../out/2026_MED_5.json")
    print("----------------")
    print(output)

if __name__ == "__main__":
    main()
