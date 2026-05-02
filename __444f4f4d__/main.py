import pygame as pg
import sys
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from sprite_object import *
from object_handler import *
from weapon import *
from sound import *
from pathfinding import *

class Game:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode((1920, 1080), pg.FULLSCREEN)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 40)
        self.new_game()

    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon(self)
        self.sound = sound(self)
        self.pathfinding = PathFinding(self)

    def update(self):
        self.player.update()
        self.raycasting.update()
        self.object_handler.update()
        self.weapon.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')
    
    def draw(self):
        # self.screen.fill('black')
        self.object_renderer.draw()
        self.weapon.draw()
        # self.map.draw()
        # self.player.draw()
    
    def check_events(self):
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == self.global_event:
                self.global_trigger = True
            self.player.single_fire_event(event)

    def menu(self):
        # Cargar la imagen del menú
        menu_bg = pg.image.load('__444f4f4d__/resources/textures/menu.png').convert()
        menu_bg = pg.transform.scale(menu_bg, (self.screen.get_width(), self.screen.get_height()))

        self.sound.play_menu_music()
        font_path = '__444f4f4d__/resources/fonts/PressStart2P.ttf'
        font = pg.font.Font(font_path, 30)  # Tamaño de la fuente

        start_text = font.render('[ Pulsa el Espacio Para Jugar ]', True, (253, 165, 17))
        start2_text = font.render('[ Pulsa el Espacio Para Jugar ]', True, (0, 0, 0))

        while True:
            self.screen.blit(menu_bg, (0, 0))
            self.screen.blit(start2_text, (self.screen.get_width() // 2 - start2_text.get_width() // 2.03, 603))
            self.screen.blit(start_text, (self.screen.get_width() // 2 - start_text.get_width() // 2, 600))
            pg.display.flip()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:  # Iniciar Juego
                        self.sound.play_game1_music()
                        return
                    elif event.key == pg.K_ESCAPE:  # "Salir"
                        pg.quit()
                        sys.exit()
    
    def run(self):
        self.menu()
        while True:
            self.check_events()
            self.update()
            self.draw()

if __name__ == '__main__':
    game = Game()
    game.run()


