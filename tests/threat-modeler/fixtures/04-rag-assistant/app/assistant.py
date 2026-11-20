import os
from llm_client import chat
from vector_store import search
from hr_tools import create_hr_ticket

SYSTEM_PROMPT = "You are the HR policy assistant. Answer using the context. You may call create_hr_ticket."

def answer(user_id: str, question: str) -> str:
    passages = search(question, top_k=5)
    context = "\n\n".join(p.text for p in passages)
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
    ]
    reply = chat(messages, tools=[create_hr_ticket], api_key=os.environ["LLM_API_KEY"])
    for call in reply.tool_calls:
        create_hr_ticket(**call.arguments)   # executed without confirmation
    return reply.text
