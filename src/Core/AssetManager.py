import pygame
import os
class AssetManager:
    def __init__(self, config, window_manager):
        self.config = config
        self.window_manager = window_manager
        self.WIDTH = window_manager.render_width
        self.HEIGHT = window_manager.render_height
        self.image_path = os.path.join(self.config.base_dir, "images")
        self.font_path = os.path.join(self.config.base_dir, "fonts")
        self.sound_path = os.path.join(self.config.base_dir, "sounds")
        self.define_colors()
        self.load_fonts()
        self.load_sounds()
        self.load_images()
    def define_colors(self):
        self.GRAY = (127, 127, 127)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.SKYBLUE = (135, 206, 235)
        self.YELLOW = (255, 255, 0)
        self.RED = (255, 0, 0)
        self.GOLDEN = (255, 199, 51)
        self.background_color = self.GRAY
    def load_fonts(self):
        self.font = pygame.font.Font(None, 25)
        self.font2 = pygame.font.Font(None, 35)
        self.font3_5 = pygame.font.SysFont("times new roman", 30)
        self.font3_8 = pygame.font.SysFont("times new roman", 38)
        self.font4_5 = pygame.font.SysFont("times new roman", 80)
        font_ttf = os.path.join(self.font_path, "8bitOperatorPlusSC-Bold.ttf")
        if os.path.exists(font_ttf):
            self.font2_5 = pygame.font.Font(font_ttf, 30)
            self.font3 = pygame.font.Font(font_ttf, 60)
            self.font4 = pygame.font.Font(font_ttf, 75)
            self.font5 = pygame.font.Font(font_ttf, 20)
        else:
            print(f"Advertencia: No se encontró la fuente en {font_ttf}, usando default.")
            self.font2_5 = self.font2
            self.font3 = self.font2
            self.font4 = self.font2
            self.font5 = self.font
    def load_sounds(self):
        self.sound = pygame.mixer.Sound(os.path.join(self.sound_path, "pong.wav"))
        self.sound_touchletters = pygame.mixer.Sound(os.path.join(self.sound_path, "touchletters.wav"))
        self.sound_exitbutton = pygame.mixer.Sound(os.path.join(self.sound_path, "exitbutton.wav"))
        self.sound_buttonletters = pygame.mixer.Sound(os.path.join(self.sound_path, "buttonletters.mp3"))
        self.sound_back = pygame.mixer.Sound(os.path.join(self.sound_path, "pong_back.mp3"))
