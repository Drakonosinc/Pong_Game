from .State import State
from Utils.States import GameState
from Interface.Menus.Main_Menu import MainMenu
# Importamos los estados siguientes
from .ModeSelectState import ModeSelectState
from .OptionsState import OptionsState

class MenuState(State):
    def __init__(self, game):
        super().__init__(game)
        self.menu = MainMenu(self.game.ui)

    def enter(self, params=None):
        self.game.main = GameState.MENU
        # SOLUCIÓN CRÍTICA: Reiniciar también la variable de la UI para evitar
        # que se dispare el cambio de estado inmediatamente si volvemos a este menú.
        self.game.ui.main = GameState.MENU
        
        self.game.ui.setup_button_factories()
        self.menu.setup_buttons()

    def exit(self):
        pass

    def update(self, dt):
        # SOLUCIÓN: Verificar self.game.ui.main (que es lo que cambian los botones)
        # Usamos getattr por seguridad por si 'main' aún no existe en ui
        ui_main = getattr(self.game.ui, 'main', None)

        if ui_main == GameState.MODE_SELECT:
            self.game.state_manager.change(ModeSelectState(self.game))
        elif ui_main == GameState.OPTIONS:
            self.game.state_manager.change(OptionsState(self.game))

    def draw(self, surface):
        self.menu.render()

    def handle_event(self, event): 
        if self.game.main == GameState.MENU: 
            self.game.events_buttons(event)