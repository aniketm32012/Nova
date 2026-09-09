import json
import re
import ollama

MODEL_NAME = "qwen2.5:1.5b"

# EXPANDED FAST PATH REGEX (0ms Latency)
REALTIME_REGEX = re.compile(
    r"\b(f1|race|score|cricket|fifa|match|news|weather|today|live|ipl|football|winner|finals|cup|champion|tournament|stock|stocks|price|olympics|medal|right now|currently)\b",
    re.IGNORECASE,
)
AUTOMATION_REGEX = re.compile(
    r"\b(open|close|launch|kill|run|start|app|chrome|powershell|cmd|taskmanager|spotify|browser|terminal)\b",
    re.IGNORECASE,
)
CODING_REGEX = re.compile(
    r"\b(regex|python|javascript|c\+\+|rust|html|css|sql|script|function|code|bug|typeerror|syntaxerror)\b",
    re.IGNORECASE,
)

INTENT_SCHEMA = {
    "type": "object",
    "properties": {
        "intent": {
            "type": "string",
            "enum": [
                "coding",
                "maths",
                "general",
                "reasoning",
                "writing skill",
                "realtime",
                "automation",
            ],
        }
    },
    "required": ["intent"],
}

SYSTEM_PROMPT = """You are Nova's zero-latency Intent Classifier.
Classify the user's intent into EXACTLY ONE allowed enum value.

Strict Rules:
- coding: Writing/debugging code, programming scripts, regex patterns, software errors.
- maths: Active arithmetic calculations, solving equations (e.g. 2+2, solve for x, calculate 15%). Physical constants (e.g. speed of light) are GENERAL.
- reasoning: Logic puzzles, riddles, word games, trick questions (e.g. sheep remaining), step-by-step logical explanations.
- writing skill: Drafting emails, cover letters, essays, rephrasing prose, poetry.
- general: Conversational chat, casual jokes ("tell me a joke"), general facts, science constants, offline static knowledge.
- realtime: Live sports, current stock prices ("right now"), weather, live updates.
- automation: OS actions, app launching, terminal execution."""

def get_intent(user_input: str) -> str:
    clean_input = user_input.strip()

    # Fast-Path Keyword Routing
    if REALTIME_REGEX.search(clean_input):
        return "realtime"
    if AUTOMATION_REGEX.search(clean_input):
        return "automation"
    if CODING_REGEX.search(clean_input) and "draft" not in clean_input.lower():
        return "coding"

    try:
        response = ollama.chat(
            model=MODEL_NAME,
            format=INTENT_SCHEMA,
            options={"temperature": 0.0},
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Classify this input: {clean_input}"},
            ],
        )

        content = response["message"]["content"].strip()
        data = json.loads(content)
        return data.get("intent", "general")

    except Exception:
        return "general"
