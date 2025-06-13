# === TypedDict ===
from .dicts import (
    ActivateQrCodeResult,
    EventCreatedResult,
    LoginUserResult,
    UserRegistrationResult,
)

# === Protocol ===
from .protocols.protocol_event import ManagementEventsProtocol
from .protocols.protocol_ticket import ManagementTicketsProtocol
from .protocols.protocol_ticket_types import ManagementTicketTypeProtocol
from .protocols.protocol_user import ManagementUsersProtocol

# === Pydantic ===
from .pydantics.routers.event import (
    AllElementsResponseDTO,
    CreateEventDTO,
    CreateEventResponseDTO,
    EditEventDTO,
    EditEventResponseDTO,
)
from .pydantics.routers.ticket_types import (
    CreateTicketTypeDTO,
    CreateTicketTypeResponseDTO,
    EditTicketTypeDTO,
    EditTicketTypeResponseDTO,
    GetTicketTypesResponseDTO,
)
from .pydantics.routers.tickets import (
    ActivateQrCodeResponseDTO,
    AllActiveTicketsEventResponseDTO,
    AllTicketsEventResponseDTO,
    TicketCreateDTO,
    TicketCreateResponseDTO,
)
from .pydantics.routers.user import (
    CreateUserDTO,
    CreateUserResponseDTO,
    GetUserInfoResponseDTO,
    LoginUserDTO,
    LoginUserResponseDTO,
)

# === NewType ===
from .types.types_event import (
    IntEventCreatorId,
    StrEventAddress,
    StrEventDescription,
    StrEventTitle,
)
from .types.types_user import IntUserId, StrUserLogin, StrUserName, StrUserPassword

__all__ = [
    "UserRegistrationResult",
    "EventCreatedResult",
    "LoginUserResult",
    "LoginUserDTO",
    "CreateUserDTO",
    "CreateEventDTO",
    "EditEventDTO",
    "IntUserId",
    "StrUserName",
    "StrUserLogin",
    "StrUserPassword",
    "IntEventCreatorId",
    "StrEventAddress",
    "StrEventDescription",
    "StrEventTitle",
    "ManagementEventsProtocol",
    "ManagementUsersProtocol",
    "ManagementTicketTypeProtocol",
    "CreateTicketTypeDTO",
    "EditTicketTypeDTO",
    "CreateTicketTypeResponseDTO",
    "EditTicketTypeResponseDTO",
    "TicketCreateDTO",
    "TicketCreateResponseDTO",
    "ManagementTicketsProtocol",
    "GetUserInfoResponseDTO",
    "LoginUserResponseDTO",
    "CreateUserResponseDTO",
    "AllElementsResponseDTO",
    "CreateEventResponseDTO",
    "EditEventResponseDTO",
    "GetTicketTypesResponseDTO",
    "AllTicketsEventResponseDTO",
    "AllActiveTicketsEventResponseDTO",
    "ActivateQrCodeResult",
    "ActivateQrCodeResponseDTO",
]
