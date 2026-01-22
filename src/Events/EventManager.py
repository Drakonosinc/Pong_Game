from typing import Callable, Type, Dict, List
from collections import defaultdict
class Event: pass
class EventManager:
    def __init__(self): self.listeners: Dict[Type[Event], List[Callable]] = defaultdict(list)
    def subscribe(self, event_type: Type[Event], listener: Callable):
        self.listeners[event_type].append(listener)
    def unsubscribe(self, event_type: Type[Event], listener: Callable):
        if event_type in self.listeners:
            try: self.listeners[event_type].remove(listener)
            except ValueError: pass
    def post(self, event: Event):
        if type(event) in self.listeners:
            for listener in self.listeners[type(event)]: listener(event)