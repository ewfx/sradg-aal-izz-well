from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from src.config import GROQ_API_KEY

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0, groq_api_key=GROQ_API_KEY)

def query_llm(prompt):
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        return response.content.strip()
    except Exception:
        return "LLM response unavailable"