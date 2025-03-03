import pygame,os,json
from pygame.locals import *
from Config_Loader import *
from AI.Genetic_Algorithm import *
class load_elements():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Space Pong")
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.config=Config()
        self.config.load_config()
        self.define_colors()
        self.load_fonts()
        self.load_sounds()
        self.config_screen()
    def load_AI(self):
        self.model_path=os.path.join(self.base_dir, "AI/best_model.pth")
        self.model_training = load_model(self.model_path, 6, 2) if os.path.exists(self.model_path) else None
    def config_screen(self):
        self.WIDTH=self.config.config_visuals["WIDTH"]
        self.HEIGHT=self.config.config_visuals["HEIGHT"]
        self.screen=pygame.display.set_mode((self.WIDTH,self.HEIGHT))
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
    def load_images(self):
        self.angle=90
        self.image_path = os.path.join(self.base_dir, "images")
        self.image=pygame.image.load(os.path.join(self.image_path,self.config_visuals["image_background"][self.config_visuals["value_background"]])).convert()
        self.image=pygame.transform.scale(self.image,(self.WIDTH,self.HEIGHT))
        self.planet=pygame.image.load(os.path.join(self.image_path,self.config_visuals["planets"][self.config_visuals["value_planet"]])).convert_alpha()
        self.planet=pygame.transform.scale(self.planet,(40,40))
        self.spacecraft=pygame.image.load(os.path.join(self.image_path,self.config_visuals["spacecrafts"][self.config_visuals["value_spacecraft1"]])).convert_alpha()
        self.spacecraft=pygame.transform.scale(self.spacecraft,(350,200))
        self.spacecraft=pygame.transform.rotate(self.spacecraft,self.angle)
        self.spacecraft2=pygame.image.load(os.path.join(self.image_path,self.config_visuals["spacecrafts"][self.config_visuals["value_spacecraft2"]])).convert_alpha()
        self.spacecraft2=pygame.transform.scale(self.spacecraft2,(350,200))
        self.spacecraft2=pygame.transform.rotate(self.spacecraft2,self.angle*3)
    def load_fonts(self):
        self.font_path = os.path.join(self.base_dir, "fonts")
        self.font=pygame.font.Font(None,25)
        self.font2=pygame.font.Font(None,35)
        self.font2_5=pygame.font.Font(os.path.join(self.font_path,"8bitOperatorPlusSC-Bold.ttf"),30)
        self.font3=pygame.font.Font(os.path.join(self.font_path,"8bitOperatorPlusSC-Bold.ttf"),60)
        self.font3_5=pygame.font.SysFont("times new roman", 30)
        self.font3_8=pygame.font.SysFont("times new roman", 38)
        self.font4=pygame.font.Font(os.path.join(self.font_path,"8bitOperatorPlusSC-Bold.ttf"),75)
        self.font4_5=pygame.font.SysFont("times new roman", 80)
        self.font5=pygame.font.Font(os.path.join(self.font_path,"8bitOperatorPlusSC-Bold.ttf"),20)
    def load_sounds(self):
        self.sound_path = os.path.join(self.base_dir, "sounds")
        self.sound=pygame.mixer.Sound(os.path.join(self.sound_path,"pong.wav"))
        self.sound_touchletters=pygame.mixer.Sound(os.path.join(self.sound_path,"touchletters.wav"))
        self.sound_exitbutton=pygame.mixer.Sound(os.path.join(self.sound_path,"exitbutton.wav"))
        self.sound_buttonletters=pygame.mixer.Sound(os.path.join(self.sound_path,"buttonletters.mp3"))
        self.sound_back=pygame.mixer.Sound(os.path.join(self.sound_path,"pong_back.mp3"))
        self.sound_back.play(loops=-1) if self.config.config_sounds["sound_main"] else None
        self.sound_back.set_volume(0.2)