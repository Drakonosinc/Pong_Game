import os
import pygame
from pyforgefx import Animator, SpriteFXGenerator, SpriteSheet


class AssetManager:
    def __init__(self, config, window_manager):
        self.config = config
        self.window_manager = window_manager
        self.WIDTH = window_manager.render_width
        self.HEIGHT = window_manager.render_height
        self.image_path = os.path.join(self.config.base_dir, "images")
        self.spritesheet_dir = os.path.join(self.image_path, "spritesheets")
        self.font_path = os.path.join(self.config.base_dir, "fonts")
        self.sound_path = os.path.join(self.config.base_dir, "sounds")
        os.makedirs(self.spritesheet_dir, exist_ok=True)
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
        if self.config.config_sounds.get("sound_main", True):
            self.sound_back.play(loops=-1)
        self.sound_back.set_volume(0.2)

    def _image_direct_path(self, image_key, value_key):
        visuals = self.config.config_visuals
        lista_imagenes = visuals[image_key]
        indice = visuals[value_key]
        return lista_imagenes[indice]

    def _build_ship_animator(
        self,
        base_surface: pygame.Surface,
        sheet_prefix: str,
        thruster_color: tuple[int, int, int],
        shield_color: tuple[int, int, int],
    ) -> Animator:
        idle_path = os.path.join(self.spritesheet_dir, f"{sheet_prefix}_idle_strip8.png")
        thrust_path = os.path.join(self.spritesheet_dir, f"{sheet_prefix}_thrust_strip8.png")
        hit_path = os.path.join(self.spritesheet_dir, f"{sheet_prefix}_hit_strip6.png")

        if os.path.exists(idle_path) and os.path.exists(thrust_path) and os.path.exists(hit_path):
            idle_sheet = SpriteSheet(idle_path)
            thrust_sheet = SpriteSheet(thrust_path)
            hit_sheet = SpriteSheet(hit_path)
        else:
            idle_sheet = SpriteFXGenerator.generate_bobbing_strip(
                base_surface,
                num_frames=8,
                amplitude_px=2,
                glow_color=None,
            )
            thrust_sheet = SpriteFXGenerator.generate_thruster_strip(
                base_surface,
                num_frames=8,
                flame_color_outer=thruster_color,
                nozzle_side="both",
            )
            hit_sheet = SpriteFXGenerator.generate_shield_hit_strip(
                base_surface,
                num_frames=6,
                shield_color=shield_color,
            )
            idle_sheet.save(idle_path)
            thrust_sheet.save(thrust_path)
            hit_sheet.save(hit_path)

        return (
            Animator(default_state="idle")
            .add_clip("idle", idle_sheet.slice_strip(8), fps=10.0, loop=True)
            .add_clip("thrust", thrust_sheet.slice_strip(8), fps=16.0, loop=True)
            .add_clip("hit", hit_sheet.slice_strip(6), fps=18.0, loop=False)
        )

    def _build_planet_animator(self, planet_surface: pygame.Surface, planet_file: str) -> Animator:
        stem = os.path.splitext(os.path.basename(planet_file))[0]
        rot_path = os.path.join(self.spritesheet_dir, f"{stem}_spin_strip12.png")
        if os.path.exists(rot_path):
            rot_sheet = SpriteSheet(rot_path)
        else:
            rot_sheet = SpriteFXGenerator.generate_rotation_strip(
                planet_surface,
                num_frames=12,
                aura_color=(255, 140, 50),
            )
            rot_sheet.save(rot_path)
        return Animator(default_state="spin").add_clip("spin", rot_sheet.slice_strip(12), fps=14.0, loop=True)

    def load_images(self):
        self.angle = 90
        bg_file = self._image_direct_path("image_background", "value_background")
        bg_raw = pygame.image.load(os.path.join(self.image_path, bg_file))
        self.image = bg_raw.convert() if pygame.display.get_surface() else bg_raw
        self.image = pygame.transform.scale(self.image, (self.WIDTH, self.HEIGHT))

        planet_file = self._image_direct_path("planets", "value_planet")
        planet_raw = pygame.image.load(os.path.join(self.image_path, planet_file))
        self.planet = planet_raw.convert_alpha() if pygame.display.get_surface() else planet_raw
        self.planet = pygame.transform.scale(self.planet, (40, 40))

        sp1_file = self._image_direct_path("spacecrafts", "value_spacecraft1")
        sp1_raw = pygame.image.load(os.path.join(self.image_path, sp1_file))
        self.spacecraft = sp1_raw.convert_alpha() if pygame.display.get_surface() else sp1_raw
        self.spacecraft = pygame.transform.scale(self.spacecraft, (350, 200))
        self.spacecraft = pygame.transform.rotate(self.spacecraft, self.angle)

        sp2_file = self._image_direct_path("spacecrafts", "value_spacecraft2")
        sp2_raw = pygame.image.load(os.path.join(self.image_path, sp2_file))
        self.spacecraft2 = sp2_raw.convert_alpha() if pygame.display.get_surface() else sp2_raw
        self.spacecraft2 = pygame.transform.scale(self.spacecraft2, (350, 200))
        self.spacecraft2 = pygame.transform.rotate(self.spacecraft2, self.angle * 3)

        sp1_stem = os.path.splitext(os.path.basename(sp1_file))[0]
        sp2_stem = os.path.splitext(os.path.basename(sp2_file))[0]
        self.p1_animator = self._build_ship_animator(
            self.spacecraft,
            sheet_prefix=f"p1_{sp1_stem}",
            thruster_color=(0, 180, 255),
            shield_color=(56, 189, 248),
        )
        self.p2_animator = self._build_ship_animator(
            self.spacecraft2,
            sheet_prefix=f"p2_{sp2_stem}",
            thruster_color=(255, 110, 40),
            shield_color=(249, 115, 22),
        )
        self.planet_animator = self._build_planet_animator(self.planet, planet_file)

    def reload_graphics(self):
        self.WIDTH = self.window_manager.render_width
        self.HEIGHT = self.window_manager.render_height
        self.load_images()
