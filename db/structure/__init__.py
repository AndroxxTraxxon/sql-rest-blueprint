from enum import Enum
class KeyType(Enum):
    NONE = 0
    PRIMARY = 1
    FOREIGN = 2
    COMPOSITE_PRIMARY = 3
    COMPOSITE_PRIMARY_FOREIGN = 5