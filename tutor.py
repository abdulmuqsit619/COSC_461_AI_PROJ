import os
from openai import OpenAI
from dotenv import load_dotenv
import tiktoken

# Load environment variables
load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("MODEL", "gpt-5.1")

client = OpenAI(api_key=API_KEY)

#SYSTEM PROMPT
system_prompt = (
    "You are a patient, friendly Python tutor for absolute beginners.\n"
    "You MUST ALWAYS produce a response containing ALL FOUR of the following "
    "sections in this exact order. NONE of the sections may be empty:\n\n"
    "Concept Explanation:\n"
    "Code Example:\n"
    "Practice Exercise:\n"
    "Feedback:\n\n"
    "Guidelines:\n"
    "- Every section MUST have meaningful content.\n"
    "- NEVER return an empty message.\n"
    "- NEVER write only code.\n"
    "- If the student asks for an example (e.g., a while loop), you must STILL "
    "fill all 4 sections.\n"
    "- Keep explanations simple, beginner-friendly, and encouraging.\n"
    "- Use short examples (<= 12 lines).\n"
)

# Token encoder
ENC = tiktoken.get_encoding("cl100k_base")


# TOKEN + COST FUNCTION
def count_tokens_for_messages(messages):
    text = "".join([m["role"] + m["content"] for m in messages])
    return len(ENC.encode(text))


def cost_estimate(prompt_tokens, completion_tokens):
    p = float(os.getenv("PRICE_PER_1K_PROMPT_TOKENS", 0)) / 1000
    c = float(os.getenv("PRICE_PER_1K_COMPLETION_TOKENS", 0)) / 1000
    return prompt_tokens * p + completion_tokens * c


#INTENT DETECTOR
def detect_mode(user_text: str) -> str:
    s = user_text.lower().strip()

    # Explanation-style requests
    if "explain" in s or "example" in s or "show me" in s or "what is" in s or "what's" in s:
        return "explain"

    # Exercises
    if "exercise" in s or "practice" in s or "problem" in s:
        return "exercise"

    # Debugging only if errors appear
    if "error" in s or "traceback" in s or "doesn't work" in s or "bug" in s:
        return "debug"

    # Code feedback
    if (
        "def " in s or
        "return" in s or
        "print(" in s or
        "\n" in s and "=" in s
    ):
        return "code_feedback"

    return "feedback"


#PROMPT BUILDER(DIFFERENT MODES)
def build_prompt(user_input: str, mode: str) -> str:

    if mode == "explain":
        return (
            f"Student question: {user_input}\n\n"
            "Provide a full explanation with ALL required sections:\n\n"
            "Concept Explanation:\n"
            "Code Example:\n"
            "Practice Exercise:\n"
            "Feedback:\n"
        )

    if mode == "exercise":
        return (
            f"Student request: {user_input}\n\n"
            "Create a beginner-friendly Python exercise. Use this structure:\n"
            "Exercise:\n"
            "Difficulty: Beginner\n"
            "Hint:\n"
            "Solution:\n"
            "Challenge Variants:\n"
        )

    if mode == "debug":
        return (
            f"Student code or error: {user_input}\n\n"
            "Analyze the code and respond using:\n"
            "Error Explanation:\n"
            "Corrected Code:\n"
            "Why This Fix Works:\n"
            "Practice Exercise:\n"
        )

    if mode == "code_feedback":
        return (
            f"Student submitted code:\n{user_input}\n\n"
            "Provide analysis using:\n"
            "What the Code Does:\n"
            "Corrections / Improvements:\n"
            "Improved Version:\n"
            "Explanation:\n"
        )

    return (
        f"Student message: {user_input}\n\n"
        "Give encouragement and helpful next steps."
    )


#MAIN ASK FUNCTION
def ask_tutor(user_input: str, conversation_history=None):

    if conversation_history is None:
        conversation_history = [{"role": "system", "content": system_prompt}]

    mode = detect_mode(user_input)
    prompt = build_prompt(user_input, mode)

    conversation_history.append({"role": "user", "content": prompt})

    # Token count before sending a request
    prompt_tokens = count_tokens_for_messages(conversation_history)

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=conversation_history,
            max_completion_tokens=600,
            temperature=0.25
        )
    except Exception as e:
        return f"[Tutor Error: {str(e)}]", {}, conversation_history

    # Extract complete
    result = response.choices[0].message.content

    # Attempted failsafe for empty respnse
    if not result or not result.strip():
        result = (
            "[Tutor Warning] The model returned an empty response.\n"
            "Let’s try again! Here is a fresh explanation:\n\n"
            "Concept Explanation:\nWhile loops run repeatedly while a condition is True.\n\n"
            "Code Example:\nwhile x < 5:\n    print(x)\n    x += 1\n\n"
            "Practice Exercise:\nWrite a loop that counts down from 10 to 1.\n\n"
            "Feedback:\nGreat question! Loops are core to Python—keep experimenting!"
        )

    completion_tokens = response.usage.completion_tokens
    total_tokens = response.usage.total_tokens

    est_cost = cost_estimate(prompt_tokens, completion_tokens)

    # Save reply to history
    conversation_history.append({"role": "assistant", "content": result})

    metadata = {
        "mode": mode,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens,
        "estimated_cost": est_cost
    }

    return result, metadata, conversation_history

