class BaseMenu:
    def __init__(interface=None):
        self.interface = interface
    def execute_buttons(self,*args):
        for button in args:button.draw()
    