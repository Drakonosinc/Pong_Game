import pygame,os,json
from pygame.locals import *
from Genetic_Algorithm import *
class load_elements():
    def __init__(self,width=0, height=0):
        pygame.init()
        pygame.display.set_caption("Space Pong")
        self.load_config()
    def load_config(self):
        try:
            config_path = os.path.join(os.path.dirname(__file__), "Config")
            with open(os.path.join(config_path,"config.json"), 'r') as file:config = json.load(file)
            self.config_visuals = config["config_visuals"]
            self.config_keys = config["config_keys"]
        except:self.config(alls=True)
    def config(self,visuals=False,keys=False,alls=False):
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
    def save_config(self):
        config_path = os.path.join(os.path.dirname(__file__), "Config")
        config = {"config_visuals": self.config_visuals,"config_keys": self.config_keys}
        with open(os.path.join(config_path,"config.json"), 'w') as file:json.dump(config, file, indent=4)
    def load_AI(self):
        self.model_path=os.path.join(os.path.dirname(__file__), "AI/best_model.pth")
        self.model_training = load_model(self.model_path, 6, 2) if os.path.exists(self.model_path) else None