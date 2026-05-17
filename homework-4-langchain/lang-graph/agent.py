import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import HumanMessage, SystemMessage
from tools import get_post, get_user_posts

load_dotenv()

# LLM
llm = ChatOpenAI(
    openai_api_key=os.getenv("PROXYAPI_KEY"),
    openai_api_base=os.getenv("OPENAI_BASE_URL"),
    model="gpt-4o-mini",
    temperature=0
)

# Список инструментов
tools = [get_post, get_user_posts]

# Привязываем инструменты к LLM
llm_with_tools = llm.bind_tools(tools)

# Системный промпт с контрактом ответа
SYSTEM_PROMPT = """
Ты — API-оператор. У тебя есть доступ к инструментам:
- get_post(post_id) — получить пост по ID
- get_user_posts(user_id) — получить все посты пользователя

Всегда отвечай в формате:
Status: success/error
Action: что сделал
Data: результат API
Errors: ошибки или None
"""

def call_model(state: MessagesState):
    """Узел агента — принимает решение о вызове инструментов"""
    messages = state["messages"]
    if not messages or messages[0].type != "system":
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + list(messages)

    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

# Строим граф
workflow = StateGraph(MessagesState)

# Добавляем узлы
workflow.add_node("agent", call_model)
workflow.add_node("tools", ToolNode(tools))

# Добавляем ребра
workflow.add_edge(START, "agent")
workflow.add_conditional_edges(
    "agent",
    tools_condition,  # встроенная функция: если есть tool_calls → "tools", иначе END
)
workflow.add_edge("tools", "agent")  # после инструментов — обратно к агенту

# Добавляем память
checkpointer = InMemorySaver()
app = workflow.compile(checkpointer=checkpointer)

# Запуск
if __name__ == "__main__":
    config = {"configurable": {"thread_id": "homework-1"}}

    while True:
        user_input = input("\nВы: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        result = app.invoke(
            {"messages": [HumanMessage(content=user_input)]},
            config=config
        )

        last_message = result["messages"][-1]
        print("\nАгент:", last_message.content)
