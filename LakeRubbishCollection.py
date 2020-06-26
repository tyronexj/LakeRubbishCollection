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
        width = 600
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

    class Player(pg.sprite.Sprite):
        def __init__(self):
            pg.sprite.Sprite.__init__(self)
            self.image = pg.Surface((30, 30))
            self.image.fill(Colour.green)
            self.rect = self.image.get_rect()
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

    class Rubbish(pg.sprite.Sprite):
        def __init__(self):
            pg.sprite.Sprite.__init__(self)
            self.image = pg.Surface((20, 20))
            self.image.fill(Colour.red)
            self.rect = self.image.get_rect()
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
            self.image = pg.Surface((20, 20))
            self.image.fill(Colour.purple)
            self.rect = self.image.get_rect()
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

        self.all_sprites = pg.sprite.Group()
        self.rubbishes = pg.sprite.Group()
        self.fishes = pg.sprite.Group()
        self.player = Game.Player()

        self.score = 0
        # this game includes 3 states: 'Start', 'Play' and 'Over'
        self.state = 'Start'
        self.start_time: int = 0

    def game_reset(self):
        self.score = 0
        self.state = 'Play'
        self.start_time = pg.time.get_ticks()

        for s in self.all_sprites:
            s.kill()

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

    def show_instruction(self, y: int, text: str):
        self.draw_text(surf=self.screen, text=text, size=24, x=Game.Setting.width // 2, y=y)

    def show_start_info(self):
        self.screen.fill(Colour.blue)
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
        self.show_instruction(text=f'the fish, which is bumping into ', y=instruction_y)
        instruction_y += instruction_y_inc
        self.show_instruction(text=f'them. Remember to keep an eye ', y=instruction_y)
        instruction_y += instruction_y_inc
        self.show_instruction(text=f"on the 'time left' section!", y=instruction_y)
        instruction_y += instruction_y_inc
        instruction_y += instruction_y_inc
        self.draw_text(surf=self.screen, text=f'Click ***SPACE*** to Start!',
                       size=24, x=Game.Setting.width // 2, y=instruction_y)

    def show_game_info(self, time_left_ms):
        self.screen.fill(Colour.blue)
        self.all_sprites.draw(self.screen)
        self.draw_text(surf=self.screen, text=f'Score: {self.score}',
                       size=24, x=100, y=20)
        self.draw_text(surf=self.screen, text=f'Time left: {(time_left_ms / 1000):.3f}',
                       size=24, x=Game.Setting.width - 150, y=20)

    def normal_play(self):
        self.all_sprites.update()

        hits_rubbishes = pg.sprite.spritecollide(sprite=self.player, group=self.rubbishes,
                                                 dokill=True)
        for _ in hits_rubbishes:
            self.score += 5
            r = Game.Rubbish()
            self.all_sprites.add(r)
            self.rubbishes.add(r)

        rubbishes_hits_fishes = pg.sprite.groupcollide(groupa=self.rubbishes, groupb=self.fishes,
                                                       dokilla=False, dokillb=True)
        for _ in rubbishes_hits_fishes:
            self.score -= 1
            f = Game.Fish()
            self.all_sprites.add(f)
            self.fishes.add(f)

        hits_fishes = pg.sprite.spritecollide(sprite=self.player, group=self.fishes,
                                              dokill=False)
        die = True if hits_fishes else False

        time_left_ms = Game.Setting.time_total_ms - (pg.time.get_ticks() - self.start_time)
        if time_left_ms <= 0:
            die = True

        self.show_game_info(time_left_ms)

        if die:
            self.state = 'Over'

    def game_over(self):
        self.screen.fill(Colour.blue)
        self.all_sprites.draw(self.screen)
        self.draw_text(surf=self.screen, text=f'YOU DIED!',
                       size=40, x=Game.Setting.width // 2, y=Game.Setting.height // 2 - 90)
        self.draw_text(surf=self.screen, text=f'Score: {self.score}',
                       size=24, x=Game.Setting.width // 2, y=Game.Setting.height // 2 - 40)
        self.draw_text(surf=self.screen, text=f'Click ***SPACE*** to re-spawn!',
                       size=24, x=Game.Setting.width // 2, y=Game.Setting.height // 2)

    def draw_text(self, surf, text: str, size: int, x: int, y: int, antialias: bool = True):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, antialias, Colour.white)
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