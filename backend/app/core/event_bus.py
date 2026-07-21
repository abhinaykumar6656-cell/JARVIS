"""
=========================================================
JARVIS Event Bus
=========================================================

The Event Bus is the communication backbone of JARVIS.

Instead of modules calling each other directly,
they publish events.

Other modules subscribe to those events and react
independently.

This keeps the system modular, scalable,
and easy to maintain.

Author: Abhinay Kumar
Project: JARVIS
=========================================================
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Callable
from uuid import uuid4

from app.core.logger import logger


# ==========================================================
# Event
# ==========================================================

@dataclass(slots=True)
class Event:
    """
    Represents a single event travelling through JARVIS.
    """

    event_id: str = field(default_factory=lambda: str(uuid4()))

    name: str = ""

    data: dict[str, Any] = field(default_factory=dict)

    source: str = "unknown"

    priority: int = 0

    timestamp: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    handled: bool = False


# ==========================================================
# Event Bus
# ==========================================================

class EventBus:
    """
    Central communication hub for JARVIS.

    Modules never communicate directly.

    They only publish and subscribe to events.
    """

    def __init__(self) -> None:
        """
        Initialize the Event Bus.
        """

        self._listeners: dict[
            str,
            list[Callable[[Event], None]]
        ] = defaultdict(list)

    # ------------------------------------------------------
    # Subscribe
    # ------------------------------------------------------

    def subscribe(
        self,
        event_name: str,
        listener: Callable[[Event], None],
    ) -> None:
        """
        Register a listener for an event.
        """

        if listener in self._listeners[event_name]:
            return

        self._listeners[event_name].append(listener)

        logger.debug(
            "Subscribed '%s' to '%s'.",
            listener.__name__,
            event_name,
        )

    # ------------------------------------------------------
    # Unsubscribe
    # ------------------------------------------------------

    def unsubscribe(
        self,
        event_name: str,
        listener: Callable[[Event], None],
    ) -> None:
        """
        Remove a listener from an event.
        """

        listeners = self._listeners.get(event_name)

        if not listeners:
            return

        if listener not in listeners:
            return

        listeners.remove(listener)

        logger.debug(
            "Unsubscribed '%s' from '%s'.",
            listener.__name__,
            event_name,
        )

        if not listeners:
            del self._listeners[event_name]

    # ------------------------------------------------------
    # Publish
    # ------------------------------------------------------

    def publish(
        self,
        event: Event,
    ) -> None:
        """
        Publish an event to all registered listeners.
        """

        listeners = self._listeners.get(event.name)

        if not listeners:
            logger.debug(
                "No listeners registered for '%s'.",
                event.name,
            )
            return

        logger.debug(
            "Publishing '%s' to %d listener(s).",
            event.name,
            len(listeners),
        )

        for listener in tuple(listeners):

            try:
                listener(event)

            except Exception:
                logger.exception(
                    "Listener '%s' crashed while handling '%s'.",
                    listener.__name__,
                    event.name,
                )

        event.handled = True

    # ------------------------------------------------------
    # Clear
    # ------------------------------------------------------

    def clear(self) -> None:
        """
        Remove all registered listeners.
        """

        self._listeners.clear()

        logger.debug(
            "All event listeners cleared."
        )

    # ------------------------------------------------------
    # Utilities
    # ------------------------------------------------------

    def listener_count(
        self,
        event_name: str,
    ) -> int:
        """
        Return the number of listeners registered for an event.
        """

        return len(
            self._listeners.get(event_name, [])
        )

    def has_listeners(
        self,
        event_name: str,
    ) -> bool:
        """
        Check whether an event has listeners.
        """

        return bool(
            self._listeners.get(event_name)
        )

    @property
    def registered_events(self) -> tuple[str, ...]:
        """
        Return all registered event names.
        """

        return tuple(
            sorted(self._listeners.keys())
        )

    @property
    def total_listeners(self) -> int:
        """
        Return total number of listeners.
        """

        return sum(
            len(listeners)
            for listeners in self._listeners.values()
        )


# ==========================================================
# Global Singleton
# ==========================================================

event_bus = EventBus()