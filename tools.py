import requests

def web_search(query):
    try:
        res = requests.get(f"https://api.duckduckgo.com/?q={query}&format=json").json()
        answer = res.get("AbstractText") or res.get("RelatedTopics", [{}])[0].get("Text")
        return answer or "Не удалось найти точный ответ."
    except Exception as e:
        return f"Ошибка поиска: {e}"
