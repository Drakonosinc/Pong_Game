class StateManager:
    def __init__(self):
        self.stack = []
    def push(self, state, params=None):
        self.stack.append(state)
        state.enter(params)
    def pop(self):
        if self.stack:
            state = self.stack.pop()
            state.exit()
            return state
        return None
    def change(self, state, params=None):
        if self.stack: self.pop()
        self.push(state, params)
    def update(self, dt):
        if self.stack: self.stack[-1].update(dt)
