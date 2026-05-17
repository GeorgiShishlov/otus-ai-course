import requests
import json
from langchain_core.tools import tool


@tool
def get_post(post_id: int) -> str:
    """Получить пост по ID из JSONPlaceholder API"""
    print(f"[API] Запрос поста {post_id}")
    url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return json.dumps(response.json(), ensure_ascii=False, indent=2)
    except Exception as e:
        return f"Ошибка API: {e}"


@tool
def get_user_posts(user_id: int) -> str:
    """Получить все посты пользователя по его ID"""
    print(f"[API] Запрос постов пользователя {user_id}")
    url = f"https://jsonplaceholder.typicode.com/users/{user_id}/posts"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return json.dumps(response.json(), ensure_ascii=False, indent=2)
    except Exception as e:
        return f"Ошибка API: {e}"
