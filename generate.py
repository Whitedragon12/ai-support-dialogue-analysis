from enum import Enum
from dataclasses import dataclass
from schema.definitions import Intent
from llm.client import ask_llm
import random
# deterministic dataset generation
random.seed(42)
class ClientAttitude(str, Enum):
    # Emotional state of the customer in the dialogue.
    CALM = "calm"
    ANGRY = "angry"
    CONFUSED = "confused"
    FRUSTRATED = "frustrated"

    @classmethod
    def values(cls):
        return [v.value for v in cls]
    
class AgentBehaviorProfile(str, Enum):
    # How the support agent behaves during the conversation.
    PROFESSIONAL = "professional"
    POLITE_BUT_UNHELPFUL = "polite_but_unhelpful"
    SLOW_RESPONSE = "slow_response"
    RUDE = "rude"
    ESCALATES_UNNECESSARILY = "escalates_unnecessarily"

    @classmethod
    def values(cls):
        return [v.value for v in cls]
    
class CaseOutcomeType(str, Enum):

    RESOLVED = "resolved"
    PARTIALLY_RESOLVED = "partially_resolved"
    UNRESOLVED = "unresolved"

    @classmethod
    def values(cls):
        return [v.value for v in cls]

@dataclass
class DialogueScenario:
    intent: Intent
    client_attitude: ClientAttitude
    agent_behavior: AgentBehaviorProfile
    outcome: CaseOutcomeType

def coverage_scenarios() -> list[DialogueScenario]:
    scenarios = []

    # кожен intent хоча б раз
    for intent in Intent:
        scenarios.append(
            DialogueScenario(
                intent=intent,
                client_attitude=random.choice(list(ClientAttitude)),
                agent_behavior=random.choice(list(AgentBehaviorProfile)),
                outcome=random.choice(list(CaseOutcomeType)),
            )
        )

    # кожна поведінка агента хоча б раз
    for behavior in AgentBehaviorProfile:
        scenarios.append(
            DialogueScenario(
                intent=random.choice(list(Intent)),
                client_attitude=random.choice(list(ClientAttitude)),
                agent_behavior=behavior,
                outcome=random.choice(list(CaseOutcomeType)),
            )
        )

    return scenarios

def build_generation_prompt(scenario: DialogueScenario) -> str:
    prompt = f"""
You are an AI system that generates realistic customer support conversations.

Generate a dialogue between a CUSTOMER and a SUPPORT AGENT.
Add small natural variations in wording between dialogues.
Avoid repeating identical phrasing.

Scenario requirements:

Customer intent:
{scenario.intent.value}

Customer attitude:
{scenario.client_attitude.value}

Agent behavior:
{scenario.agent_behavior.value}

Case outcome:
{scenario.outcome.value}

Rules:
- The dialogue must look realistic.
- Include multiple turns (at least 4 messages).
- Clearly reflect the customer attitude.
- The agent behavior must match the description.
- The outcome must naturally appear by the end of the conversation.
- Use format:

Customer: ...
Agent: ...

Return ONLY the dialogue text.
Do NOT add explanations.

"""
    return prompt

def random_scenario() -> DialogueScenario:

    return DialogueScenario(
        intent=random.choice(list(Intent)),
        client_attitude=random.choice(list(ClientAttitude)),
        agent_behavior=random.choice(list(AgentBehaviorProfile)),
        outcome=random.choice(list(CaseOutcomeType)),
    )

def generate_dialogue(scenario: DialogueScenario) -> str:

    prompt = build_generation_prompt(scenario)
    dialogue = ask_llm(prompt)
    return dialogue

def generate_dataset(size: int) -> list[dict]:

    scenarios = coverage_scenarios()

    # добиваємо випадковими до потрібного розміру
    while len(scenarios) < size:
        scenarios.append(random_scenario())

    random.shuffle(scenarios)

    dataset = []

    for i, scenario in enumerate(scenarios[:size]):
        dialogue = generate_dialogue(scenario)

        dataset.append({
            "id": i,
            "dialogue": dialogue,
            "ground_truth": {
                "intent": scenario.intent.value,
                "client_attitude": scenario.client_attitude.value,
                "agent_behavior": scenario.agent_behavior.value,
                "outcome": scenario.outcome.value,
            }
        })
        
    return dataset