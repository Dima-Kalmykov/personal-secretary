from dataclasses import dataclass


@dataclass
class EventResponse:
    summary: str
    start_time: str
    end_time: str
