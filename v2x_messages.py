from enum import Enum, auto
from dataclasses import dataclass
from typing import Any, Optional

class MessageType(Enum):
    ANNOUNCE = auto()      # Un véhicule cherche un peloton
    PROPOSE = auto()       # Un peloton propose une adhésion
    ACCEPT = auto()        # Confirmation de fusion
    REJECT = auto()        # Refus
    REQUEST_SLOT = auto()  # Demande de passage à l'intersection
    GRANT_SLOT = auto()    # L'intersection valide le passage

@dataclass
class V2XMessage:
    sender_id: str
    receiver_id: Optional[str]  # None pour un message diffusé à tous (Broadcast)
    msg_type: MessageType
    data: Any