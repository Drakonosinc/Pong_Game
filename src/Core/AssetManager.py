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
        if self.config.config_sounds.get("sound_main", True): self.sound_back.play(loops=-1)
        self.sound_back.set_volume(0.2)
    def _image_direct_path(self, image_key, value_key):
        visuals = self.config.config_visuals
        lista_imagenes = visuals[image_key]
        indice = visuals[value_key]
        return lista_imagenes[indice]
    def load_images(self):
        self.angle = 90
        bg_file = self._image_direct_path("image_background", "value_background")
        self.image = pygame.image.load(os.path.join(self.image_path, bg_file)).convert()
        self.image = pygame.transform.scale(self.image, (self.WIDTH, self.HEIGHT))
        planet_file = self._image_direct_path("planets", "value_planet")
        self.planet = pygame.image.load(os.path.join(self.image_path, planet_file)).convert_alpha()
        self.planet = pygame.transform.scale(self.planet, (40, 40))
        sp1_file = self._image_direct_path("spacecrafts", "value_spacecraft1")
        self.spacecraft = pygame.image.load(os.path.join(self.image_path, sp1_file)).convert_alpha()
        self.spacecraft = pygame.transform.scale(self.spacecraft, (350, 200))
        self.spacecraft = pygame.transform.rotate(self.spacecraft, self.angle)
        sp2_file = self._image_direct_path("spacecrafts", "value_spacecraft2")
        self.spacecraft2 = pygame.image.load(os.path.join(self.image_path, sp2_file)).convert_alpha()
        self.spacecraft2 = pygame.transform.scale(self.spacecraft2, (350, 200))
        self.spacecraft2 = pygame.transform.rotate(self.spacecraft2, self.angle * 3)
    def reload_graphics(self):
        self.WIDTH = self.window_manager.render_width
        self.HEIGHT = self.window_manager.render_height
        self.load_images()