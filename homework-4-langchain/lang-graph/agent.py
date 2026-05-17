import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

# 1. Инициализируем LLM через ProxyAPI
llm = ChatOpenAI(
    openai_api_key=os.getenv("PROXYAPI_KEY"),
    openai_api_base=os.getenv("OPENAI_BASE_URL"),
    model="gpt-4o-mini",
    temperature=0
)

# 2. Определяем системный промпт
SYSTEM_PROMPT = "Ты полезный ассистент. Отвечай кратко и по делу."

# 3. Определяем функцию-узел (node)
def call_model(state: MessagesState):
    """Узел, который вызывает LLM и возвращает ответ"""
    messages = state["messages"]
    
    # Добавляем системный промпт, если его нет
    if not messages or messages[0].type != "system":
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + list(messages)
    
    response = llm.invoke(messages)
    return {"messages": [response]}

# 4. Строим граф
workflow = StateGraph(MessagesState)  # MessagesState уже содержит поле messages
workflow.add_node("agent", call_model)  # добавляем узел "agent"
workflow.add_edge(START, "agent")       # START → агент
workflow.add_edge("agent", END)         # агент → конец

# 5. Добавляем память (checkpointer)
checkpointer = InMemorySaver()
app = workflow.compile(checkpointer=checkpointer)

# 6. Запускаем агента
if __name__ == "__main__":
    config = {"configurable": {"thread_id": "user-123"}}
    
    user_input = input("Ваш вопрос: ")
    
    result = app.invoke(
        {"messages": [HumanMessage(content=user_input)]},
        config=config
    )
    
    print("\nОтвет:", result["messages"][-1].content)