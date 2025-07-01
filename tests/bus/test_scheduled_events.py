import asyncio
from datetime import datetime, timedelta
from llmgine.bus.bus import MessageBus
from llmgine.messages.events import ScheduledEvent, Event

# Handler that prints when called, accepts base Event type
def scheduled_event_handler(event: Event):
    if isinstance(event, ScheduledEvent):
        print(f"Handled scheduled event at {datetime.now().isoformat()} with scheduled_time={event.scheduled_time}")

def regular_event_handler(event: Event):
    print(f"Handled regular event at {datetime.now().isoformat()}")

async def test_scheduled_events_are_processed():
    bus = MessageBus()
    await bus.start()

    # Register the handler for ScheduledEvent
    bus.register_event_handler(ScheduledEvent, scheduled_event_handler)

    # Schedule two events 10 seconds in the future
    scheduled_time = datetime.now() + timedelta(seconds=5)
    event1 = ScheduledEvent(scheduled_time=scheduled_time)
    event2 = ScheduledEvent(scheduled_time=scheduled_time)

    await bus.publish(event1)
    await bus.publish(event2)

    # Wait 11 seconds to ensure events are processed
    await asyncio.sleep(6)
    await bus.stop()

async def test_scheduled_events_and_regular_events_are_processed():
    bus = MessageBus()
    await bus.start()

    # Register the handler for ScheduledEvent and regular events
    bus.register_event_handler(ScheduledEvent, scheduled_event_handler)
    bus.register_event_handler(Event, regular_event_handler)
    
    # Schedule two events 10 seconds in the future
    event1 = ScheduledEvent(scheduled_time=datetime.now() + timedelta(seconds=3))
    event2 = Event()
    event3 = ScheduledEvent(scheduled_time=datetime.now() + timedelta(seconds=5))
    event4 = Event()

    await bus.publish(event1)
    await bus.publish(event2)
    await bus.publish(event3)
    await bus.publish(event4)

    await asyncio.sleep(6)
    await bus.ensure_events_processed()
    await bus.stop()

if __name__ == "__main__":
    asyncio.run(test_scheduled_events_and_regular_events_are_processed())
