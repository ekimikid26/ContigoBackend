import enum

class RiskLevel(str, enum.Enum):
    NORMAL = "NORMAL"
    MILD = "MILD"
    MODERATE = "MODERATE"
    SEVERE = "SEVERE"

class Alert:
    pass
