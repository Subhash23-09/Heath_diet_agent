## Multi‑Agent Health & Wellness Assistant
Multi‑Agent Health & Wellness Assistant is a Flask‑based backend that uses LangChain and Google Gemini to provide safe, non‑diagnostic health and wellness guidance. Multiple specialized agents (symptom, lifestyle, diet, fitness) collaborate via shared memory, and an orchestrator merges their outputs into a single structured response.​

## Features
Multi‑agent pipeline for symptom analysis, lifestyle tips, diet, and fitness.​

Shared short‑term memory using ConversationBufferMemory so agents can see each other’s outputs.​

RAG hook over a local knowledge.json file.

API key–protected REST endpoints (/health-assist, /history/<user_id>).

Structured JSON response with synthesized_guidance and recommendations.​

## Tech Stack
Python 3.11

Flask

LangChain (langchain, langchain-google-genai)

Google Gemini 2.5 Flash (ChatGoogleGenerativeAI)

JSON file storage for user history and knowledge base

## Result


POST- http://127.0.0.1:5000/health-assist
<img width="1370" height="796" alt="image" src="https://github.com/user-attachments/assets/a7b9af5e-8282-41b2-98f1-841812ded4da" />

<img width="1341" height="790" alt="image" src="https://github.com/user-attachments/assets/b7d25509-d23a-4878-a501-71f751e3f4c4" />

GET- http://127.0.0.1:5000/history/test1
<img width="1322" height="778" alt="image" src="https://github.com/user-attachments/assets/3ae19224-4344-4a57-a029-f89e640c9fc6" />

