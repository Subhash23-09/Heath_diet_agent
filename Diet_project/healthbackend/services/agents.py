from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage
from healthbackend.config.settings import GOOGLE_API_KEY, MODEL_NAME
from healthbackend.services.memory import get_shared_memory
from healthbackend.services.rag import retrieve_context

llm = ChatGoogleGenerativeAI(
    model=MODEL_NAME,
    temperature=0,
    google_api_key=GOOGLE_API_KEY,
    convert_system_message_to_human=True,
)

memory = get_shared_memory()


async def symptom_agent(symptoms: str) -> str:
    history = memory.load_memory_variables({})["chat_history"]

    messages = [
        SystemMessage(
            content=(
                "You are a safe medical triage assistant. "
                "You only assess severity and suggest if the user should see a doctor. "
                "Do not provide diagnoses or prescriptions."
            )
        ),
    ] + history + [
        HumanMessage(
            content=f"Analyze these symptoms and their possible severity: {symptoms}"
        )
    ]

    result = await llm.ainvoke(messages)

    memory.save_context(
        {"input": f"[symptom_agent] {symptoms}"},
        {"output": result.content},
    )
    return result.content


async def lifestyle_agent(symptoms: str) -> str:
    history = memory.load_memory_variables({})["chat_history"]

    prompt = (
        f"Given the conversation so far and these symptoms: {symptoms}, "
        f"suggest lifestyle changes and constraints."
    )

    messages = [
        SystemMessage(
            content=(
                "You are a lifestyle coach collaborating with other agents. "
                "Suggest simple lifestyle habits, sleep hygiene, stress management and daily routine tips. "
                "Keep suggestions safe and generic."
            )
        ),
    ] + history + [HumanMessage(content=prompt)]

    result = await llm.ainvoke(messages)

    # store correctly as lifestyle_agent, with a single input key
    memory.save_context(
        {"input": f"[lifestyle_agent] {prompt}"},
        {"output": result.content},
    )
    return result.content


async def diet_agent(symptoms: str, report: str, lifestyle_notes: str) -> str:
    history = memory.load_memory_variables({})["chat_history"]

    kb = retrieve_context(symptoms)

    prompt = (
        f"User symptoms: {symptoms}\n"
        f"Relevant medical report text (may be empty): {report}\n"
        f"Lifestyle information from lifestyle_agent: {lifestyle_notes}\n"
        f"Evidence / knowledge base snippets: {kb}\n\n"
        "Suggest a safe, balanced diet plan. Mention foods to prefer and foods to avoid. "
        "Highlight that this is not a replacement for a dietician or doctor."
    )

    messages = [
        SystemMessage(
            content=(
                "You are a dietician collaborating with other agents to give general diet guidance. "
                "Never claim to cure diseases or override a doctor's advice."
            )
        ),
    ] + history + [HumanMessage(content=prompt)]

    result = await llm.ainvoke(messages)

    memory.save_context(
        {"input": f"[diet_agent] {prompt}"},
        {"output": result.content},
    )
    return result.content


async def fitness_agent(symptoms: str, diet_notes: str) -> str:
    history = memory.load_memory_variables({})["chat_history"]

    prompt = (
        f"User symptoms: {symptoms}\n"
        f"Diet constraints from diet_agent: {diet_notes}\n\n"
        "Recommend only low‑risk, gentle physical activities, "
        "and clearly tell the user to stop if they feel pain or discomfort."
    )

    messages = [
        SystemMessage(
            content=(
                "You are a cautious fitness coach. "
                "You design simple, low‑intensity plans that are generally safe. "
                "Always recommend consulting a doctor before heavy exercise."
            )
        ),
    ] + history + [HumanMessage(content=prompt)]

    result = await llm.ainvoke(messages)

    # single input key, tagged with fitness_agent
    memory.save_context(
        {"input": f"[fitness_agent] {prompt}"},
        {"output": result.content},
    )
    return result.content
