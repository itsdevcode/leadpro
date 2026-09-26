import enum
class LeadStatus(str, enum.Enum):
    NEW = "NEW"
    CONTACTED = "CONTACTED"
    QUALIFIED = "QUALIFIED"
    LOST = "LOST"
    WON = "WON"
    CONVERTED = "CONVERTED"

class LeadPriority(str, enum.Enum):
    HIGH="HIGH"
    MEDIUM="MEDIUM"
    LOW="LOW"