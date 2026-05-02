import pygame as pg

class sound:
    def __init__(self, game):
        self.game = game
        pg.mixer.init()
        self.path = '__444f4f4d__/resources/sound/'
        self.shotgun = pg.mixer.Sound(self.path + 'shotgun.wav')
        self.npc_pain = pg.mixer.Sound(self.path + 'npc_pain.wav')
        self.npc_shot = pg.mixer.Sound(self.path + 'npc_attack.wav')
        self.npc_death = pg.mixer.Sound(self.path + 'npc_death.wav')
        self.player_pain = pg.mixer.Sound(self.path + 'player_pain.wav')
        self.player_death = pg.mixer.Sound(self.path + 'player_death.wav')
        pg.mixer.music.set_volume(0.5)

    def play_menu_music(self):
        pg.mixer.music.load(self.path + 'menu.mp3')
        pg.mixer.music.play()  # Reproduce una vez

    def play_game1_music(self):
        pg.mixer.music.load(self.path + 'e1m1.mp3')
        pg.mixer.music.play(-1)  # Reproduce en bucle

    def play_game2_music(self):
        pg.mixer.music.load(self.path + 'e1m2.mp3')
        pg.mixer.music.play(-1)  # Reproduce en bucle
    
    def play_game3_music(self):
        pg.mixer.music.load(self.path + 'e1m3.mp3')
        pg.mixer.music.play(-1)  # Reproduce en bucle
    
    def play_end_music(self):
        pg.mixer.music.load(self.path + 'end.mp3')
        pg.mixer.music.play(-1)  # Reproduce en bucle