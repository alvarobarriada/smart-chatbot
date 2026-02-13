from dataclasses import asdict, dataclass  #, field

# from datetime import datetime
from typing import Literal

# Definimos los roles permitidos como un tipo literal
RoleType = Literal["user", "assistant", "system"]

@dataclass(frozen=True)
class Message:
    """
    Data Transfer Object (DTO) que representa un mensaje.
    Principio: Estructura de Datos (solo guarda datos, sin lógica).
    """
    role: RoleType
    content: str
    # timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict:
        """Serializo el objeto para guardarlo en JSON."""
        return asdict(self)
