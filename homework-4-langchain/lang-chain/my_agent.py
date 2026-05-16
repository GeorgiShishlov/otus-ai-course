# my_agent.py
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate

# 1. Загружаем API ключ из файла .env
load_dotenv()

# 2. Определяем инструмент (tool), который будет использовать агент
@tool
def multiply(x: float, y: float) -> float:
    """Умножает x на y."""
    print(f"🔧 Вызываю инструмент 'multiply' с аргументами {x} и {y}")
    return x * y

# 3. Создаем экземпляр языковой модели
llm = ChatOpenAI(
    openai_api_key=os.getenv("PROXYAPI_KEY"),
    openai_api_base=os.getenv("OPENAI_BASE_URL"), # "https://api.proxyapi.ru/openai/v1"
    model="gpt-4o-mini", # или "gpt-3.5-turbo", "gpt-4o"
    temperature=0
)

# 4. Создаем список доступных инструментов
tools = [multiply]

# 5. Создаем шаблон промпта для агента
prompt = ChatPromptTemplate.from_messages([
    ("system", "Ты полезный ассистент. Используй доступные инструменты для ответа на вопросы."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

# 6. Собираем агента
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 7. Запускаем агента с запросом
if __name__ == "__main__":
    result = agent_executor.invoke({"input": "Сколько будет 15 умножить на 3?"})
    print("\n📝 Итоговый ответ агента:", result["output"])