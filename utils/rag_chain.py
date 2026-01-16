from utils.retriever import retrieve_chunks
from utils.groq_llm import generate_answer

chat_history = []

def ask_rag(question: str, k: int = 4) -> str:
    docs = retrieve_chunks(question, k=k)

    context = "\n\n".join(
        doc.page_content for doc in docs
    )

    history_text = "\n".join(chat_history)

    answer = generate_answer(
        context=context,
        question=question,
        chat_history=history_text
    )

    chat_history.append(f"User: {question}")
    chat_history.append(f"Assistant: {answer}")

    return answer
