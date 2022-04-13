from dataclasses import dataclass


@dataclass
class EventContent:
    summary: str
    start_time: str
    end_time: str
