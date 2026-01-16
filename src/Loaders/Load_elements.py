import pygame,os
from pygame.locals import *
from .Config_Loader import *
from Type_Training import *
from Core import *
class load_elements():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Space Pong")
        self.config=Config()
        self.config.load_config()
        self.define_colors()
        self.load_fonts()
        self.load_sounds()
        self.config_screen()
    def load_AI(self):
        self.model_path=os.path.join(self.config.base_dir, "AI/best_model.pth")
        nn_cfg = self.config.config_AI.get("nn", {"hidden_layers": 2, "neurons_per_layer": 6})
        arch = [nn_cfg.get("neurons_per_layer", 6)] * nn_cfg.get("hidden_layers", 2)
        type_training = next(k for k, v in self.config.config_AI["type_training"].items() if v)
        type_model = next(k for k, v in self.config.config_AI["type_model"].items() if v)
        if type_training == "Genetic": self.model_training = load_genetic_model(self.model_path, type_model, 6, 2, hidden_sizes=arch) if os.path.exists(self.model_path) else None
        elif type_training == "Q-learning": self.model_training = load_qlearning_model(self.model_path, type_model, 6, 2, hidden_sizes=arch) if os.path.exists(self.model_path) else None
    def config_screen(self):
        self.window = WindowManager("Space Pong AI", self.config.config_visuals["WIDTH"], self.config.config_visuals["HEIGHT"])
        self.WIDTH = self.window.render_width
        self.HEIGHT = self.window.render_height
        self.load_images()
    def define_colors(self):
        self.GRAY=(127,127,127)
        self.WHITE=(255,255,255)
        self.BLACK=(0,0,0)
        self.GREEN=(0,255,0)
        self.BLUE=(0,0,255)
        self.SKYBLUE=(135,206,235)
        self.YELLOW=(255,255,0)
        self.RED=(255,0,0)
        self.GOLDEN=(255,199,51)
        self.background=self.GRAY
    def image_direct_path(self,image,value): return self.config.config_visuals[image][self.config.config_visuals[value]]
    def load_images(self):
        self.angle=90
        self.image_path = os.path.join(self.config.base_dir, "images")
        self.image=pygame.image.load(os.path.join(self.image_path,self.image_direct_path("image_background","value_background"))).convert()
        self.image=pygame.transform.scale(self.image,(self.WIDTH,self.HEIGHT))
        self.planet=pygame.image.load(os.path.join(self.image_path,self.image_direct_path("planets","value_planet"))).convert_alpha()
        self.planet=pygame.transform.scale(self.planet,(40,40))
        self.spacecraft=pygame.image.load(os.path.join(self.image_path,self.image_direct_path("spacecrafts","value_spacecraft1"))).convert_alpha()
        self.spacecraft=pygame.transform.scale(self.spacecraft,(350,200))
        self.spacecraft=pygame.transform.rotate(self.spacecraft,self.angle)
        self.spacecraft2=pygame.image.load(os.path.join(self.image_path,self.image_direct_path("spacecrafts","value_spacecraft2"))).convert_alpha()
        self.spacecraft2=pygame.transform.scale(self.spacecraft2,(350,200))
        self.spacecraft2=pygame.transform.rotate(self.spacecraft2,self.angle*3)
    def load_fonts(self):
        self.font_path = os.path.join(self.config.base_dir, "fonts")
        self.font = pygame.font.Font(None,25)
        self.font2 = pygame.font.Font(None,35)
        self.font2_5 = pygame.font.Font(os.path.join(self.font_path,"8bitOperatorPlusSC-Bold.ttf"),30)
        self.font3 = pygame.font.Font(os.path.join(self.font_path,"8bitOperatorPlusSC-Bold.ttf"),60)
        self.font3_5 = pygame.font.SysFont("times new roman", 30)
        self.font3_8 = pygame.font.SysFont("times new roman", 38)
        self.font4 = pygame.font.Font(os.path.join(self.font_path,"8bitOperatorPlusSC-Bold.ttf"),75)
        self.font4_5 = pygame.font.SysFont("times new roman", 80)
        self.font5 = pygame.font.Font(os.path.join(self.font_path,"8bitOperatorPlusSC-Bold.ttf"),20)
    def load_sounds(self):
        self.sound_path = os.path.join(self.config.base_dir, "sounds")
        self.sound = pygame.mixer.Sound(os.path.join(self.sound_path,"pong.wav"))
        self.sound_touchletters = pygame.mixer.Sound(os.path.join(self.sound_path,"touchletters.wav"))
        self.sound_exitbutton = pygame.mixer.Sound(os.path.join(self.sound_path,"exitbutton.wav"))
        self.sound_buttonletters = pygame.mixer.Sound(os.path.join(self.sound_path,"buttonletters.mp3"))
        self.sound_back = pygame.mixer.Sound(os.path.join(self.sound_path,"pong_back.mp3"))
        self.sound_back.play(loops=-1) if self.config.config_sounds["sound_main"] else None
        self.sound_back.set_volume(0.2)