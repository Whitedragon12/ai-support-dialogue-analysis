from enum import Enum
class Intent(str, Enum):

    PAYMENT_PROBLEM = "payment_problem"
    TECHNICAL_ERROR = "technical_error"
    ACCOUNT_ACCESS = "account_access"
    TARIFF_QUESTION = "tariff_question" 
    REFUND = "refund"
    OTHER = "other"

    @classmethod
    def allowed_values(cls):
        return [ intent.value for intent in cls ]
    
    @classmethod
    def llm_helper(cls): #better format for LLM
        return "\n".join(
            f"- {value}" for value in cls.allowed_values())
    
class Satisfaction(str, Enum):

    SATISFIED = "satisfied"
    NEUTRAL = "neutral" # unclear customer satisfaction
    UNSATISFIED = "unsatisfied"

    @classmethod
    def allowed_values(cls):
        return [ satisfaction.value for satisfaction in cls]
    
    @classmethod
    def llm_helper(cls):
        return "\n".join(
            f"- {value}" for value in cls.allowed_values())

class AgentMistake(str, Enum):

    IGNORED_QUESTION = "ignored_question"
    INCORRECT_INFO = "incorrect_info"
    RUDE_TONE = "rude_tone"
    NO_RESOLUTION = "no_resolution"
    UNNECESSARY_ESCALATION = "unnecessary_escalation"
    NONE = "none" # no detectable agent mistakes

    @classmethod
    def allowed_values(cls):
        return [ v.value for v in cls]
    
    @classmethod
    def llm_helper(cls):
        return "\n".join(
            f"- {value}" for value in cls.allowed_values())