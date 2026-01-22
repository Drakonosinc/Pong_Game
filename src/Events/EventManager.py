from typing import Callable, Type, Dict, List
from collections import defaultdict
class Event: pass
class EventManager:
    def __init__(self): self.listeners: Dict[Type[Event], List[Callable]] = defaultdict(list)
    def subscribe(self, event_type: Type[Event], listener: Callable):
        self.listeners[event_type].append(listener)
