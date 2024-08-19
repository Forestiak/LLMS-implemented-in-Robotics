
from enum import Enum, auto

class HighLevelRoboticArmCommands(Enum):
    LOCATE_OBJECT = auto()
    MOVE_TO_OBJECT = auto()
    GRASP_OBJECT = auto()
    LIFT_OBJECT = auto()
    MOVE_TO_LOCATION = auto()
    RELEASE_OBJECT = auto()
    SCAN_AREA = auto()
    ADJUST_GRIP = auto()
    VERIFY_OBJECT_GRASP = auto()
    POSITION_ABOVE_OBJECT = auto()
    LOWER_OBJECT = auto()
    CHECK_OBJECT_PRESENCE = auto()
    ALIGN_WITH_OBJECT = auto()
    RETRACT_ARM = auto()
    EXTEND_ARM = auto()
    PAN_VIEW_LEFT = auto()
    PAN_VIEW_RIGHT = auto()
    TILT_VIEW_UP = auto()
    TILT_VIEW_DOWN = auto()
    RESET_POSITION = auto()
