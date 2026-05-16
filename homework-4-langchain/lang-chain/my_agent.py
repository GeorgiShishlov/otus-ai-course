# my_agent.py
import os
import sys
import requests
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate

# 1. Загружаем API ключ из файла .env
load_dotenv()

# 2. Определяем инструменты (tools), которые будет использовать агент
@tool
def get_post(post_id: int) -> str:
    """Получить пост по его ID. Параметр: целое число post_id."""
    print(f"[API] Запрашиваем пост с id={post_id}")
    url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"
    response = requests.get(url)
    return json.loads(response.text) if response.status_code == 200 else "Пост не найден"

@tool
def get_user_posts(user_id: int):
    """Получить все посты пользователя по его ID. Параметр: целое число user_id."""
    print(f"[API] Запрашиваем посты пользователя с id={user_id}")
    url = f"https://jsonplaceholder.typicode.com/posts?userId={user_id}"
    response = requests.get(url)
    return json.loads(response.text) if response.status_code == 200 else "Посты не найдены"

@tool
def create_post(title: str, body: str, userId: int):
    """Создать новый пост. Параметры: title (строка), body (строка), userId (целое число)."""
    print(f"[API] Создаем новый пост для пользователя с id={userId}")
    url = "https://jsonplaceholder.typicode.com/posts"
    payload = {
        "title": title,
        "body": body,
        "userId": userId
    }
    response = requests.post(url, json=payload)
    return json.loads(response.text) if response.status_code == 201 else "Ошибка при создании поста"

# 3. Создаем экземпляр языковой модели
llm = ChatOpenAI(
    openai_api_key=os.getenv("PROXYAPI_KEY"),
    openai_api_base=os.getenv("OPENAI_BASE_URL"), # "https://api.proxyapi.ru/openai/v1"
    model="gpt-4o-mini", # или "gpt-3.5-turbo", "gpt-4o"
    temperature=0
)

# 4. Создаем список доступных инструментов
tools = [get_post, get_user_posts, create_post]

# 5. Создаем шаблон промпта для агента
prompt = ChatPromptTemplate.from_messages([
    ("system", """Ты — API-оператор. У тебя есть доступ к трём инструментам:
1. get_post(post_id) — получить пост по ID.
2. get_user_posts(user_id) — получить все посты пользователя.
3. create_post(title, body, userId) — создать новый пост.

Всегда отвечай строго в формате:

Status: success | error
Action: какое действие выполнил (например, "вызван get_post с id=3")
Data: результат API в удобном виде (если ошибка, то "None")
Errors: описание ошибки или "None"

Если пользователь спрашивает про пост — используй get_post.
Если про все посты пользователя — get_user_posts.
Если про создание — create_post.
Никогда не выдумывай данные — только вызывай инструменты.
"""),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

# 6. Собираем агента
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 7. Запускаем агента с запросом
if __name__ == "__main__":
    user_input = sys.argv[1] if len(sys.argv) > 1 else "Сколько будет 15 умножить на 3?"
    result = agent_executor.invoke({"input": user_input})
    print("\n📝 Итоговый ответ агента:", result["output"])