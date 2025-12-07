import json
import re
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage

from healthbackend.services.agents import (
    symptom_agent,
    lifestyle_agent,
    diet_agent,
    fitness_agent,
)
from healthbackend.services.history_store import save_history
from healthbackend.services.memory import get_shared_memory, reset_memory
from healthbackend.config.settings import GOOGLE_API_KEY, MODEL_NAME


async def orchestrate(symptoms: str, medical_report: str, user_id: str):
    reset_memory()
    memory = get_shared_memory()

    symptom_result = await symptom_agent(symptoms)
    lifestyle_result = await lifestyle_agent(symptoms)
    diet_result = await diet_agent(
        symptoms=symptoms,
        report=medical_report,
        lifestyle_notes=lifestyle_result,
    )
    fitness_result = await fitness_agent(
        symptoms=symptoms,
        diet_notes=diet_result,
    )

    history = memory.load_memory_variables({})["chat_history"]

    synth_llm = ChatGoogleGenerativeAI(
        model=MODEL_NAME,
        temperature=0,
        google_api_key=GOOGLE_API_KEY,
        convert_system_message_to_human=True,
    )

    synth_messages = [
        SystemMessage(
            content=(
                "You are an orchestrator that reads the entire conversation "
                "between symptom_agent, lifestyle_agent, diet_agent, and fitness_agent. "
                "Return ONLY valid JSON with keys:\n"
                "  - synthesized_guidance: long markdown text summary\n"
                "  - recommendations: array of short recommendation strings\n"
                "Do not wrap JSON in code fences or add any extra text."
            )
        ),
        *history,
        HumanMessage(content="Generate the JSON response now."),
    ]

    final_answer = await synth_llm.ainvoke(synth_messages)
    raw = final_answer.content.strip()

    # if the model still sends ```json fences, remove them

    import re

    if raw.startswith("```"):
        raw = re.sub(r"^```[a-zA-Z]*\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)




    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        data = {"synthesized_guidance": raw, "recommendations": []}

    output = {
        "user_id": user_id,
        "query": symptoms,
        "intent": "symptom",
        "symptom_analysis": symptom_result,
        "lifestyle": lifestyle_result,
        "diet": diet_result,
        "fitness": fitness_result,
        "synthesized_guidance": data.get("synthesized_guidance", ""),
        "recommendations": data.get("recommendations", []),
    }

    save_history(user_id, output)
    return output
