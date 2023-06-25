from enum import Enum


class EventStatus(str, Enum):
    MONEY_COLLECTING = "Сумма для проведения ивента собирается"
    MONEY_COLLECTED = "Сумма для проведения ивента собрана"
    EVENT_COMPLETED = "Ивент завершился"
    EVENT_CANCELLED = "Ивент отменен"
