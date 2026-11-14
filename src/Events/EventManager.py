import sys
from typing import Callable, Type, Dict, List
from collections import defaultdict


class Event:
    pass


class EventManager:
    def __init__(self):
        self.listeners: Dict[Type[Event], List[Callable]] = defaultdict(list)

    def subscribe(self, event_type: Type[Event], listener: Callable):
        self.listeners[event_type].append(listener)

    def unsubscribe(self, event_type: Type[Event], listener: Callable):
        if event_type in self.listeners:
            try:
                self.listeners[event_type].remove(listener)
            except ValueError:
                pass

    def post(self, event: Event):
        ev_type = type(event)
        if ev_type in self.listeners:
            for listener in list(self.listeners[ev_type]):
                listener(event)
            return
        ev_name = ev_type.__name__
        for reg_type, callbacks in list(self.listeners.items()):
            if getattr(reg_type, "__name__", None) == ev_name:
                for listener in list(callbacks):
                    listener(event)


sys.modules["Events.EventManager"] = sys.modules[__name__]
sys.modules["src.Events.EventManager"] = sys.modules[__name__]