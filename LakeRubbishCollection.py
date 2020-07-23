# Background music is from Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3

import os
import pygame as pg
import random as rd


class Colour:
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    yellow = (255, 255, 0)
    cyan = (0, 255, 255)
    purple = (255, 0, 255)


class Game:
    class Setting:
        name = 'Rubbish Collecting Game'
        font_name = 'consolas'
        width = 480
        height = 600
        fps = 30
        time_total_ms = 30 * 1000
        player_speed = 6
        screen_board = 10
        fish_screen_board = 20
        rubbish_max_speed = 4
        rubbish_min_speed = 2
        fish_max_speed = 4
        fish_min_speed = 2
        num_of_rubbishes = 3
        num_of_fishes = 5
        player_width = 100
        player_height = 50
        rubbish_width = 35
        rubbish_height = 35
        fish_width = 35
        fish_height = 35

        img_dir = os.path.join(os.path.dirname(__file__), 'img')
        snd_dir = os.path.join(os.path.dirname(__file__), 'snd')

    class Player(pg.sprite.Sprite):
        def __init__(self):
            pg.sprite.Sprite.__init__(self)
            self.player_img = pg.image.load(os.path.join(Game.Setting.img_dir, 'diver.png')).convert()
            self.player_img = pg.transform.scale(self.player_img,
                                                 (Game.Setting.player_width, Game.Setting.player_height))
            self.image = self.player_img
            self.image.set_colorkey(Colour.blue)
            # self.image = pg.Surface((50, 38))
            # self.image.fill(Colour.green)
            self.rect = self.image.get_rect()

            # self.radius = self.rect.width * 0.7 // 2
            # pg.draw.circle(self.image, Colour.red, self.rect.center, self.radius

            self.mask = pg.mask.from_surface(self.image)

            self.rect.centerx = Game.Setting.width // 2
            self.rect.bottom = Game.Setting.height - Game.Setting.screen_board
            self.speed_x = 0
            self.speed_y = 0

        def update(self):
            self.speed_x = 0
            self.speed_y = 0
            key_state: list = pg.key.get_pressed()
            if key_state[pg.K_UP]:
                self.speed_y = -Game.Setting.player_speed
            if key_state[pg.K_DOWN]:
                self.speed_y = Game.Setting.player_speed
            if key_state[pg.K_LEFT]:
                self.speed_x = -Game.Setting.player_speed
            if key_state[pg.K_RIGHT]:
                self.speed_x = Game.Setting.player_speed
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            if self.rect.right > Game.Setting.width - Game.Setting.screen_board:
                self.rect.right = Game.Setting.width - Game.Setting.screen_board
            if self.rect.left < Game.Setting.screen_board:
                self.rect.left = Game.Setting.screen_board
            if self.rect.bottom > Game.Setting.height - Game.Setting.screen_board:
                self.rect.bottom = Game.Setting.height - Game.Setting.screen_board
            if self.rect.top < Game.Setting.screen_board:
                self.rect.top = Game.Setting.screen_board
            # Flip player if swim backwards
            if self.speed_x < 0:
                self.image = pg.transform.flip(self.player_img, True, False)
            elif self.speed_x > 0:
                self.image = pg.transform.flip(self.player_img, False, False)
            self.mask = pg.mask.from_surface(self.image)

    class Rubbish(pg.sprite.Sprite):
        def __init__(self):
            pg.sprite.Sprite.__init__(self)
            rubbish_img = pg.image.load(os.path.join(Game.Setting.img_dir, 'rubbish.png')).convert()
            self.image = pg.transform.scale(rubbish_img, (Game.Setting.rubbish_width,
                                                          Game.Setting.rubbish_height))
            self.image.set_colorkey(Colour.blue)
            # self.image = pg.Surface((20, 20))
            # self.image.fill(Colour.red)
            self.rect = self.image.get_rect()

            # self.radius = self.rect.width * 0.65 // 2
            # pg.draw.circle(self.image, Colour.purple, self.rect.center, self.radius)

            self.mask = pg.mask.from_surface(self.image)

            self.rect.x = rd.randint(0, Game.Setting.width - self.rect.width)
            self.rect.y = 0
            self.speed_x = 0
            self.speed_y = rd.randint(Game.Setting.rubbish_min_speed, Game.Setting.rubbish_max_speed)

        def update(self):
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            if self.rect.bottom > Game.Setting.height - Game.Setting.screen_board:
                self.rect.bottom = Game.Setting.height - Game.Setting.screen_board

    class Fish(pg.sprite.Sprite):
        def __init__(self):
            pg.sprite.Sprite.__init__(self)
            fish_img = pg.image.load(os.path.join(Game.Setting.img_dir, 'fish.png')).convert()
            self.image = pg.transform.scale(fish_img, (Game.Setting.fish_width,
                                                       Game.Setting.fish_height))
            self.image.set_colorkey(Colour.blue)
            # self.image = pg.Surface((20, 20))
            # self.image.fill(Colour.purple)
            self.rect = self.image.get_rect()

            # self.radius = self.rect.width * 0.5 // 2
            # pg.draw.circle(self.image, Colour.cyan, self.rect.center, self.radius)

            self.mask = pg.mask.from_surface(self.image)

            self.speed_x = 0
            self.speed_y = 0
            self.init_position_speed()

        def update(self):
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            if self.rect.right < -Game.Setting.fish_screen_board:
                self.init_position_speed()

        def init_position_speed(self):
            self.rect.left = Game.Setting.width + Game.Setting.fish_screen_board
            self.rect.y = rd.randint(Game.Setting.fish_screen_board,
                                     Game.Setting.height - Game.Setting.fish_screen_board)
            self.speed_x = rd.randint(-Game.Setting.fish_max_speed, -Game.Setting.fish_min_speed)
            self.speed_y = 0

    def __init__(self):
        self.screen = pg.display.set_mode((Game.Setting.width, Game.Setting.height))
        pg.display.set_caption(Game.Setting.name)
        self.clock = pg.time.Clock()
        self.font_name = pg.font.match_font(Game.Setting.font_name)
        self.background_img = pg.image.load(os.path.join(Game.Setting.img_dir, 'lake.png')).convert()
        self.score_snd = pg.mixer.Sound(os.path.join(Game.Setting.snd_dir, 'pow4.wav'))
        self.game_over_snd = pg.mixer.Sound(os.path.join(Game.Setting.snd_dir, 'expl6.wav'))
        pg.mixer.music.load(os.path.join(Game.Setting.snd_dir, 'SeamlessLoop.ogg'))
        pg.mixer.music.set_volume(0.3)

        self.all_sprites = pg.sprite.Group()
        self.rubbishes = pg.sprite.Group()
        self.fishes = pg.sprite.Group()
        self.player = Game.Player()

        self.score = 0
        # this game includes 3 states: 'Start', 'Play' and 'Over'
        self.state = 'Start'
        self.start_time = 0

        self.game_over_reason = ''

    def game_reset(self):
        self.score = 0
        self.state = 'Play'
        self.start_time = pg.time.get_ticks()

        for sprite in self.all_sprites:
            sprite.kill()

        self.player = Game.Player()
        self.all_sprites.add(self.player)

        for i in range(Game.Setting.num_of_rubbishes):
            rubbish = Game.Rubbish()
            self.rubbishes.add(rubbish)
            self.all_sprites.add(rubbish)

        for i in range(Game.Setting.num_of_fishes):
            fish = Game.Fish()
            self.fishes.add(fish)
            self.all_sprites.add(fish)

    def game_loop(self):
        pg.mixer.music.play(loops=-1)
        running = True
        while running:
            self.clock.tick(Game.Setting.fps)
            for event in pg.event.get():
                # pg.QUIT is a common event
                if event.type == pg.QUIT:
                    running = False
                if self.state == 'Start':
                    self.show_start_info_event_handler(event)
                elif self.state == 'Play':
                    self.normal_play_event_handler(event)
                elif self.state == 'Over':
                    self.game_over_event_handler(event)

            if self.state == 'Start':
                self.show_start_info()
            elif self.state == 'Play':
                self.normal_play()
            elif self.state == 'Over':
                self.game_over()

            pg.display.flip()

    def show_start_info_event_handler(self, event: pg.event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                self.game_reset()

    def normal_play_event_handler(self, event: pg.event):
        pass

    def game_over_event_handler(self, event: pg.event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                self.game_reset()

    def show_instruction(self, y: int, text: str, size=24):
        self.draw_text(surf=self.screen, text=text, size=size, x=Game.Setting.width // 2, y=y, colour=Colour.white)

    def show_start_info(self):
        # self.screen.fill(Colour.blue)
        self.screen.blit(self.background_img, self.background_img.get_rect())
        self.all_sprites.draw(self.screen)
        instruction_y = 100
        instruction_y_inc = 30
        self.show_instruction(text=f"Instruction: There's too much ", y=instruction_y)
        instruction_y += instruction_y_inc
        self.show_instruction(text=f'rubbish in the lake, which is ', y=instruction_y)
        instruction_y += instruction_y_inc
        self.show_instruction(text=f'harmful to either ecosystem ', y=instruction_y)
        instruction_y += instruction_y_inc
        self.show_instruction(text=f'and the environment. Your ', y=instruction_y)
        instruction_y += instruction_y_inc
        self.show_instruction(text=f'mission is to collect rubbish ', y=instruction_y)
        instruction_y += instruction_y_inc
        self.show_instruction(text=f'as much as possible in 30 ', y=instruction_y)
        instruction_y += instruction_y_inc
        self.show_instruction(text=f'seconds without interrupting ', y=instruction_y)
        instruction_y += instruction_y_inc
        self.show_instruction(text=f"the fish (in other words, don't ", y=instruction_y)
        instruction_y += instruction_y_inc
        self.show_instruction(text=f'bump into them) Remember to keep ', y=instruction_y)
        instruction_y += instruction_y_inc
        self.show_instruction(text=f"an eye on the 'time left' section! ", y=instruction_y)
        instruction_y += instruction_y_inc
        instruction_y += instruction_y_inc
        self.draw_text(surf=self.screen, text=f'Click ***SPACE*** to Start!',
                       size=24, x=Game.Setting.width // 2, y=instruction_y)

    def show_game_info(self, time_left_ms):
        # self.screen.fill(Colour.blue)
        self.screen.blit(self.background_img, self.background_img.get_rect())
        self.all_sprites.draw(self.screen)
        self.draw_text(surf=self.screen, text=f'Score: {self.score}',
                       size=24, x=100, y=20)
        self.draw_text(surf=self.screen, text=f'Time left: {(time_left_ms / 1000):.3f}',
                       size=24, x=Game.Setting.width - 150, y=20)

    def normal_play(self):
        self.all_sprites.update()

        hits_rubbishes = pg.sprite.spritecollide(self.player, self.rubbishes, True)
        for _ in hits_rubbishes:
            self.score += 5
            rubbish = Game.Rubbish()
            self.all_sprites.add(rubbish)
            self.rubbishes.add(rubbish)
            self.score_snd.play()

        rubbishes_hits_fishes = pg.sprite.groupcollide(self.rubbishes, self.fishes, False, True,
                                                       pg.sprite.collide_mask)
        for _ in rubbishes_hits_fishes:
            self.score -= 2
            if self.score < 0:
                self.score = 0
            fish = Game.Fish()
            self.all_sprites.add(fish)
            self.fishes.add(fish)

        hits_fishes = pg.sprite.spritecollide(self.player, self.fishes, False, pg.sprite.collide_mask)
        if hits_fishes:
            die = True
            self.game_over_snd.play()
            self.game_over_reason = 'Interrupting a fish'
        else:
            die = False

        time_left_ms = Game.Setting.time_total_ms - (pg.time.get_ticks() - self.start_time)
        if time_left_ms <= 0:
            die = True
            self.game_over_reason = 'Timeout'

        self.show_game_info(time_left_ms)

        if die:
            self.state = 'Over'

    def game_over(self):
        # self.screen.fill(Colour.blue)
        self.screen.blit(self.background_img, self.background_img.get_rect())
        self.all_sprites.draw(self.screen)

        if self.score >= 100:
            game_over_msg = "YOU'RE REALLY GOOD AT THIS!"
        elif 80 <= self.score < 100:
            game_over_msg = 'A FEW MORE POINTS TO GO...'
        else:
            game_over_msg = 'GAME OVER'

        if game_over_msg == 'GAME OVER':
            self.draw_text(surf=self.screen, text=game_over_msg,
                           size=40, x=Game.Setting.width // 2, y=Game.Setting.height // 2 - 90)
        else:
            self.draw_text(surf=self.screen, text=game_over_msg,
                           size=30, x=Game.Setting.width // 2, y=Game.Setting.height // 2 - 90)

        self.draw_text(surf=self.screen, text=f'Final score: {self.score}',
                       size=24, x=Game.Setting.width // 2, y=Game.Setting.height // 2 - 40)
        self.draw_text(surf=self.screen, text=f'Click ***SPACE*** to re-spawn!',
                       size=24, x=Game.Setting.width // 2, y=Game.Setting.height // 2)
        self.draw_text(surf=self.screen, text='Reason: %s' % self.game_over_reason,
                       size=18, x=Game.Setting.width // 2, y=Game.Setting.height // 2 + 60)

    def draw_text(self, surf, text: str, size: int, x: int, y: int, antialias: bool = True,
                  colour: tuple = Colour.black):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, antialias, colour)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surf.blit(text_surface, text_rect)


def main():
    pg.init()
    pg.mixer.init()  # init sound mixer

    g = Game()
    g.game_loop()

    pg.quit()
    return


if __name__ == '__main__':
    main()
