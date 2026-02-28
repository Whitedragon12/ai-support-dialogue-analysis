from schema.definitions import Intent, Satisfaction, AgentMistake
from llm.client import standardize_llm_output, ask_llm

def build_intent_prompt(dialogue: str) -> str:

    allowed = Intent.llm_helper()

    prompt = f"""
You are an AI system that analyzes customer support conversations.

Your task is to determine the CUSTOMER'S INTENT.

Rules:
- Choose EXACTLY one value from the list below.
- Return ONLY the value itself.
- Do NOT explain your reasoning.
- Do NOT add extra words or punctuation.

Allowed values:
{allowed}

Conversation:
\"\"\"
{dialogue}
\"\"\"
"""
    return prompt

def parse_intent(llm_output: str) -> Intent:

    formatted = standardize_llm_output(llm_output)
    try:
        return Intent(formatted)
    except ValueError:
        return Intent.OTHER
    
def analyze_intent(dialogue: str) -> Intent:

    prompt = build_intent_prompt(dialogue)
    llm_output = ask_llm(prompt)
    intent = parse_intent(llm_output)
    return intent

def build_satisfaction_prompt(dialogue: str, intent: Intent) -> str:

    allowed = Satisfaction.llm_helper()

    prompt = f"""
You are an AI system that analyzes customer support conversations.

Your task is to determine the CUSTOMER'S SATISFACTION
based on the conversation and the detected customer intent.

Detected customer intent:
{intent.value}

Rules:
- Choose EXACTLY one value from the list below.
- Return ONLY the value itself.
- Do NOT explain your reasoning.
- Do NOT add extra words or punctuation.

Allowed values:
{allowed}

Conversation:
\"\"\"
{dialogue}
\"\"\"
"""
    return prompt

def parse_satisfaction(llm_output: str) -> Satisfaction:

    formatted = standardize_llm_output(llm_output)
    try:
        return Satisfaction(formatted)
    except ValueError:
        return Satisfaction.NEUTRAL

def analyze_satisfaction(dialogue: str, intent: Intent) -> Satisfaction:

    prompt = build_satisfaction_prompt(dialogue, intent)
    llm_output = ask_llm(prompt)
    satisfaction = parse_satisfaction(llm_output)
    return satisfaction

def build_quality_score_prompt(dialogue: str, intent: Intent) -> str:

    prompt = f"""
You are an AI system that evaluates the quality of a customer support agent.

Your task is to rate the SUPPORT AGENT'S PERFORMANCE.

Evaluate ONLY the agent's actions, not the customer's emotions.

Detected customer intent:
{intent.value}

Scoring scale (1–5):
1 = Very poor support (rude behavior, incorrect information, or no attempt to resolve the issue)
2 = Poor support (multiple mistakes, unclear guidance, weak attempt to help)
3 = Acceptable support (partially helpful but imperfect or incomplete resolution)
4 = Good support (mostly correct solution with minor issues or inefficiencies)
5 = Excellent support (correct solution, clear communication, professional behavior)

Rules:
- Return ONLY a single integer number.
- The number MUST be between 1 and 5.
- Return ONLY the number itself (e.g., 1, 2, 3, 4, or 5).
- Do NOT explain your reasoning.
- Do NOT add text or punctuation.

Conversation:
\"\"\"
{dialogue}
\"\"\"
"""
    return prompt

def parse_quality_score(llm_output: str) -> int:

    formatted = standardize_llm_output(llm_output)

    try:
        score = int(formatted)

        if 1 <= score <= 5:
            return score
        else:
            return 3

    except ValueError:
        return 3

def analyze_quality_score(dialogue: str, intent: Intent) -> int:

    prompt = build_quality_score_prompt(dialogue, intent)
    llm_output = ask_llm(prompt)
    quality_score = parse_quality_score(llm_output)
    return quality_score

def build_agent_mistakes_prompt(dialogue: str, intent: Intent) -> str:

    allowed = AgentMistake.llm_helper()

    prompt = f"""
You are an AI system that analyzes mistakes made by a customer support agent.

Your task is to identify ALL agent mistakes present in the conversation.

Detected customer intent:
{intent.value}

Allowed mistake types:
{allowed}

Rules:
- Return each mistake on a separate line.
- Return ONLY values from the allowed list.
- If no mistakes are present, return: none
- Do NOT explain your reasoning.
- Do NOT add extra text or punctuation.

Conversation:
\"\"\"
{dialogue}
\"\"\"
"""
    return prompt

def parse_agent_mistakes(llm_output: str) -> list[AgentMistake]:

    formatted = standardize_llm_output(llm_output)

    lines = formatted.splitlines()
    result: list[AgentMistake] = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        try:
            result.append(AgentMistake(line))
        except ValueError:
            pass  

    if not result:
        return [AgentMistake.NONE]

    return result

def analyze_agent_mistakes(dialogue: str, intent: Intent) -> list[AgentMistake]:

    prompt = build_agent_mistakes_prompt(dialogue, intent)
    llm_output = ask_llm(prompt)
    agent_mistakes = parse_agent_mistakes(llm_output)
    return agent_mistakes

def analyze_dialogue(dialogue: str) -> dict:
    
    # 1. Intent (перший, тому що інші залежать від нього)
    intent = analyze_intent(dialogue)

    # 2. Інші аналізи
    satisfaction = analyze_satisfaction(dialogue, intent)
    quality_score = analyze_quality_score(dialogue, intent)
    agent_mistakes = analyze_agent_mistakes(dialogue, intent)

    # 3. JSON-ready 
    result = {
        "intent": intent.value,
        "satisfaction": satisfaction.value,
        "quality_score": quality_score,
        "agent_mistakes": [m.value for m in agent_mistakes],
    }

    return result