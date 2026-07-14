"""
JARVIS Event Bus

The Event Bus is the communication backbone of JARVIS.

Instead of modules calling each other directly,
they publish events.

Other modules subscribe to those events and react
independently.

This keeps the system modular, scalable, and easy to maintain.

Author: Abhinay Kumar
Project: JARVIS
"""

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Callable


# --------------------------------------------------
# Event Object
# --------------------------------------------------

@dataclass(slots=True)
class Event:
    """
    Represents a single event flowing through JARVIS.
    """

    name: str
    data: dict[str, Any] = field(default_factory=dict)
    