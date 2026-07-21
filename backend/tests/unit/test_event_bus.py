"""
Unit tests for the JARVIS Event Bus.
"""

from app.core.event_bus import Event, event_bus


def test_subscribe():
    event_bus.clear()

    def listener(event: Event):
        pass

    event_bus.subscribe("voice.command", listener)

    assert event_bus.listener_count("voice.command") == 1


def test_duplicate_subscribe():
    event_bus.clear()

    def listener(event: Event):
        pass

    event_bus.subscribe("voice.command", listener)
    event_bus.subscribe("voice.command", listener)

    assert event_bus.listener_count("voice.command") == 1


def test_publish():
    event_bus.clear()

    received = []

    def listener(event: Event):
        received.append(event.data["text"])

    event_bus.subscribe("voice.command", listener)

    event = Event(
        name="voice.command",
        data={"text": "Open YouTube"},
    )

    event_bus.publish(event)

    assert received == ["Open YouTube"]
    assert event.handled is True


def test_unsubscribe():
    event_bus.clear()

    def listener(event: Event):
        pass

    event_bus.subscribe("voice.command", listener)

    event_bus.unsubscribe("voice.command", listener)

    assert event_bus.listener_count("voice.command") == 0


def test_clear():
    event_bus.clear()

    def listener(event: Event):
        pass

    event_bus.subscribe("voice.command", listener)

    event_bus.clear()

    assert event_bus.total_listeners == 0


def test_registered_events():
    event_bus.clear()

    def listener(event: Event):
        pass

    event_bus.subscribe("voice.command", listener)
    event_bus.subscribe("memory.saved", listener)

    events = event_bus.registered_events

    assert "voice.command" in events
    assert "memory.saved" in events


def test_has_listeners():
    event_bus.clear()

    def listener(event: Event):
        pass

    event_bus.subscribe("voice.command", listener)

    assert event_bus.has_listeners("voice.command") is True
    assert event_bus.has_listeners("unknown") is False


def test_listener_exception():
    event_bus.clear()

    called = []

    def bad_listener(event: Event):
        raise RuntimeError("Boom")

    def good_listener(event: Event):
        called.append(True)

    event_bus.subscribe("voice.command", bad_listener)
    event_bus.subscribe("voice.command", good_listener)

    event = Event(name="voice.command")

    event_bus.publish(event)

    assert called == [True]


if __name__ == "__main__":

    test_subscribe()
    test_duplicate_subscribe()
    test_publish()
    test_unsubscribe()
    test_clear()
    test_registered_events()
    test_has_listeners()
    test_listener_exception()

    print("All Event Bus tests passed successfully!")