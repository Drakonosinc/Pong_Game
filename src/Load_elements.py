import pygame,os,json
from pygame.locals import *
from Genetic_Algorithm import *
class load_elements():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Space Pong")
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.load_config()
        self.define_colors()
        self.load_fonts()
        self.load_sounds()
        self.config_screen()
    def load_config(self):
        try:
            config_path = os.path.join(self.base_dir, "Config")
            with open(os.path.join(config_path,"config.json"), 'r') as file:config = json.load(file)
            self.config_visuals = config["config_visuals"]
            self.config_keys = config["config_keys"]
            self.config_sounds = config["config_sounds"]
            self.config_AI = config["config_AI"]
            self.config_game = config["config_game"]
        except:self.config(alls=True),self.save_config()
    def config(self,visuals=False,keys=False,sounds=False,AI=False,game=False,alls=False):
        if visuals or alls:self.config_visuals={"WIDTH":700,"HEIGHT":400,
                            "image_background":["background1.jpg","background2.jpg","background3.jpg","background4.jpg","background5.jpg","background6.jpg","background7.jpg","background8.jpg"],
                            "value_background":0,
                            "planets":["Mars.png","Mars1.png","meteorite.png","Saturn.png","earth.png"],
                            "value_planet":0,
                            "spacecrafts":["spaceship.png","spaceship2.png","spaceship3.png"],
                            "value_spacecraft1":0,
                            "value_spacecraft2":0}
        if keys or alls:self.config_keys={"UP_W":K_w,"Name_key1":"W",
                        "DOWN_S":K_s,"Name_key2":"S",
                        "UP_ARROW":K_UP,"Name_key3":"↑",
                        "DOWN_ARROW":K_DOWN,"Name_key4":"↓"}
        if sounds or alls:self.config_sounds={"sound_main":True}
        if AI or alls:self.config_AI={"generation_value":100,"population_value":20,"try_for_ai":3,"model_save":False}
        if game or alls:self.config_game={"number_balls":1}
    def save_config(self):
        config_path = os.path.join(self.base_dir, "Config")
        config = {"config_visuals": self.config_visuals,"config_keys": self.config_keys,"config_AI": self.config_AI, "config_sounds": self.config_sounds,"config_game": self.config_game}
        with open(os.path.join(config_path,"config.json"), 'w') as file:json.dump(config, file, indent=4)
    def load_AI(self):
        self.model_path=os.path.join(self.base_dir, "AI/best_model.pth")
        self.model_training = load_model(self.model_path, 6, 2) if os.path.exists(self.model_path) else None
    def config_screen(self):
        self.WIDTH=self.config_visuals["WIDTH"]
        self.HEIGHT=self.config_visuals["HEIGHT"]
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
        self.sound_back.play(loops=-1) if self.config_sounds["sound_main"] else None
        self.sound_back.set_volume(0.2)