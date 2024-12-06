from dataclasses import dataclass
from typing import Dict, Union

@dataclass
class ChecklistCallback:
    keyboard_tag: str
    keys_tag: str
    order_id: Union[int, str]

checklist_points: Dict[str, Dict[str, bool]] = {}

checklist_callback_data: Dict[int, ChecklistCallback] = {}