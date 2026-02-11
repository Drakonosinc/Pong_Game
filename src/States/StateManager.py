class StateManager:
    def __init__(self, state_factory):
        self.stack = []
        self.factory = state_factory
    def change_state(self, state_enum, params=None):
        new_state = self.factory.get_state(state_enum)
        if new_state is None:
            print(f"Error: StateFactory devolvió None para {state_enum}")
            return
        if self.stack:
            previous_state = self.stack.pop()
            previous_state.exit()
        self.stack.append(new_state)
        new_state.enter(params)
    def push_state(self, state_enum, params=None):
        new_state = self.factory.get_state(state_enum)
        if new_state:
            self.stack.append(new_state)
            new_state.enter(params)
    def pop_state(self):
        if self.stack:
            state = self.stack.pop()
            state.exit()
            return state
        return None

    def update(self, dt):
        if self.stack: self.stack[-1].update(dt)
    def draw(self, surface):
        if self.stack: self.stack[-1].draw(surface)
    def handle_event(self, event):
        if self.stack: self.stack[-1].handle_event(event)