import os
import google.generativeai as genai

from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)

generation_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 8192,
}


def handle_gemini_model(input_text):
    model = genai.GenerativeModel('gemini-pro', generation_config=generation_config)
    chat = model.start_chat(history=[])
    response = chat.send_message(input_text)
    return response.text


def handle_gemini_image(image):
    prompt = "If image have text, transcribe it, otherwise describe it."
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content(contents=[prompt, image])
    response.resolve()
    return response.text
