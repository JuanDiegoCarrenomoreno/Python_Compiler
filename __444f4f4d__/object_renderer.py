import pygame as pg
from settings import *

class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()
        self.sky_image = self.get_texture('__444f4f4d__/resources/textures/sky.png', (WIDTH, HALF_HEIGHT))
        self.sky_offset = 0
        self.blood_screen = self.get_texture('__444f4f4d__/resources/textures/blood_screen.png', RES)
        self.digit_size = 90
        self.digit_images = [self.get_texture(f'__444f4f4d__/resources/textures/digits/{i}.png', [self.digit_size] * 2)
                             for i in range(11)]
        self.digits = dict(zip(map(str, range(11)), self.digit_images))
        self.game_over_image = self.get_texture('__444f4f4d__/resources/textures/game_over.png', RES)
        self.win_image = self.get_texture('__444f4f4d__/resources/textures/win.png', RES)
    
    def draw(self):
        self.draw_background()
        self.render_game_objects()
        self.draw_player_health()
    
    def game_over(self):
        self.screen.blit(self.game_over_image, (0, 0))
        self.game.sound.player_death.play()

    def win(self):
        self.screen.blit(self.win_image, (0, 0))
    
    def draw_player_health(self):
        health = str(self.game.player.health)
        for i, char in enumerate(health):
            self.screen.blit(self.digits[char], (i * self.digit_size, 0))
        self.screen.blit(self.digits['10'], ((i + 1) * self.digit_size, 0))

    def player_damage(self):
        self.screen.blit(self.blood_screen, (0, 0))
    
    def draw_background(self):
        self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % WIDTH
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))
        # Suelo
        pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))

    def render_game_objects(self):
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)
    
    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)
    
    def load_wall_textures(self):
        return {
            1: self.get_texture('__444f4f4d__/resources/textures/1.png'),
            2: self.get_texture('__444f4f4d__/resources/textures/2.png'),
            3: self.get_texture('__444f4f4d__/resources/textures/3.png'),
            4: self.get_texture('__444f4f4d__/resources/textures/4.png'),
            5: self.get_texture('__444f4f4d__/resources/textures/5.png'),
            6: self.get_texture('__444f4f4d__/resources/textures/6.png'),
            7: self.get_texture('__444f4f4d__/resources/textures/7.png'),
            8: self.get_texture('__444f4f4d__/resources/textures/8.png'),
            9: self.get_texture('__444f4f4d__/resources/textures/9.png'),
            10: self.get_texture('__444f4f4d__/resources/textures/10.png'),
            11: self.get_texture('__444f4f4d__/resources/textures/11.png'),
            12: self.get_texture('__444f4f4d__/resources/textures/12.png'),
            13: self.get_texture('__444f4f4d__/resources/textures/13.png'),
            14: self.get_texture('__444f4f4d__/resources/textures/14.png'),
            15: self.get_texture('__444f4f4d__/resources/textures/15.png'),
            16: self.get_texture('__444f4f4d__/resources/textures/16.png'),
        }