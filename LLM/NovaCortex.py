import json
import ollama

MODEL_NAME = "qwen2.5:1.5b"

VALID_INTENTS = {
    "coding",
    "maths",
    "general",
    "reasoning",
    "writing skill",
    "realtime",
    "automation",
}

SYSTEM_ROUTER_PROMPT = """You are a strict intent classifier for Nova. 
Classify input into EXACTLY ONE category:
- coding
- maths
- general
- reasoning
- writing skill
- realtime
- automation

Output strictly JSON: {"intent": "<category>"}"""

# Few-shot examples act as rigid anchors for 1.5B weights
FEW_SHOT_EXAMPLES = [
    {"role": "user", "content": "what is the score of team india against eng in cricket"},
    {"role": "assistant", "content": '{"intent": "realtime"}'},
    {"role": "user", "content": "who won the F1 race today"},
    {"role": "assistant", "content": '{"intent": "realtime"}'},
    {"role": "user", "content": "open google chrome and search for formula 1"},
    {"role": "assistant", "content": '{"intent": "automation"}'},
    {"role": "user", "content": "kill all node processes in powershell"},
    {"role": "assistant", "content": '{"intent": "automation"}'},
    {"role": "user", "content": "hello how are you"},
    {"role": "assistant", "content": '{"intent": "general"}'},
]

def get_intent(user_input: str) -> str:
    try:
        messages = [{"role": "system", "content": SYSTEM_ROUTER_PROMPT}]
        messages.extend(FEW_SHOT_EXAMPLES)
        messages.append({"role": "user", "content": user_input})

        response = ollama.chat(
            model=MODEL_NAME,
            format="json",
            options={"temperature": 0.0},
            messages=messages
        )

        content = response["message"]["content"].strip()
        data = json.loads(content)
        intent = str(data.get("intent", "general")).strip().lower()

        return intent if intent in VALID_INTENTS else "general"

    except Exception:
        return "general"
