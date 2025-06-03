class BaseMenu:
    def __init__(interface=None):
        self.interface = interface
    def execute_buttons(self,*args):
        for button in args:button.draw()
    def filt(self,number):
        background=pygame.Surface((self.WIDTH,self.HEIGHT),pygame.SRCALPHA)
        background.fill((0,0,0,number))
        self.screen.blit(background,(0,0))