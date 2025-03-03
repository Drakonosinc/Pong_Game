import json,os
class Config():
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