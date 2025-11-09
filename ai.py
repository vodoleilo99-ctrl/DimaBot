# ai.py — бесплатная версия через Hugging Face
import os
import requests

HF_TOKEN = os.getenv("HF_TOKEN")
MODEL = "mistralai/Mistral-7B-Instruct-v0.2"  # Можно заменить на flan-t5-base, если хочешь быстрее

headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def ask_openai(prompt):
    try:
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{MODEL}",
            headers=headers,
            json={"inputs": prompt, "options": {"wait_for_model": True}},
            timeout=60
        )
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list) and len(data) > 0 and "generated_text" in data[0]:
            return data[0]["generated_text"].strip()
        elif isinstance(data, dict) and "error" in data:
            return f"⚠️ Ошибка Hugging Face: {data['error']}"
        else:
            return "⚠️ Неизвестный ответ Hugging Face"
    except Exception as e:
        return f"⚠️ Ошибка запроса HF: {e}"
