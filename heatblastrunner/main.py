import pygame as pg
from random import randint, choice

class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        player_walk_1 = pg.image.load("graphics/player/run/1.png").convert_alpha()
        player_walk_2 = pg.image.load("graphics/player/run/2.png").convert_alpha()
        player_walk_3 = pg.image.load("graphics/player/run/3.png").convert_alpha()
        player_walk_4 = pg.image.load("graphics/player/run/4.png").convert_alpha()
        player_walk_5 = pg.image.load("graphics/player/run/5.png").convert_alpha()
        player_walk_6 = pg.image.load("graphics/player/run/6.png").convert_alpha()
        
        self.player_walk = [player_walk_1, player_walk_2, player_walk_3, player_walk_4, player_walk_5, player_walk_6]
        self.player_index = 0
        self.player_jump = pg.image.load("graphics/player/jump/jump.png").convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect(midbottom = (80, 340))
        self.coll_rect = pg.Rect(self.rect.x + 10, self.rect.y, self.image.get_width() - 25, self.image.get_height())
        self.gravity = 0

        self.jump_sound = pg.mixer.Sound('sounds/jump.mp3')

    def player_input(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE] and self.rect.bottom >= 340:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.bottom += self.gravity
        self.coll_rect.bottom += self.gravity
        if self.rect.bottom >= 340:
            self.rect.bottom = 340
            self.coll_rect.bottom = 340

    def animation(self):
        if self.rect.bottom < 340 :
            self.image = self.player_jump
            self.mask = pg.mask.from_surface(self.image)
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]
            self.mask = pg.mask.from_surface(self.image)

    def update(self):
        self.player_input()
        # screen.blit(self.mask.to_surface(), self.rect)
        self.animation()
        # pg.draw.rect(screen, "blue", self.rect, 2)
        self.apply_gravity()

class Obstacle(pg.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == "drone":
            drone_frame_1 = pg.image.load("graphics/drones/1.png").convert_alpha()
            drone_frame_2 = pg.image.load("graphics/drones/2.png").convert_alpha()
            drone_frame_3 = pg.image.load("graphics/drones/3.png").convert_alpha()
            self.frames = [drone_frame_1, drone_frame_2, drone_frame_3]
            y_pos = 210
        else:
            red_frame_1 = pg.image.load("graphics/mechadroid/mech1.png").convert_alpha()
            red_frame_2 = pg.image.load("graphics/mechadroid/mech2.png").convert_alpha()
            red_frame_3 = pg.image.load("graphics/mechadroid/mech3.png").convert_alpha()
            self.frames = [red_frame_1, red_frame_2, red_frame_3]
            y_pos = 340

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.surf = self.frames[2]
        self.mask = pg.mask.from_surface(self.surf)
        self.rect = self.surf.get_rect(midbottom = (randint(900, 1100), y_pos))
    
    def animation_state(self):
        if self.rect.x > 700:
            animation_index = 0
            self.image = self.frames[animation_index]

        if self.rect.x < 700 and self.rect.x > 600:
            animation_index = 1
            self.image = self.frames[animation_index]

        if self.rect.x < 600:
            animation_index = 2
            self.image = self.frames[animation_index]
            self.mask = pg.mask.from_surface(self.image)
    
    def update(self):
        self.rect.x -= 6
        # screen.blit(self.mask.to_surface(), self.rect)
        self.animation_state()
        # pg.draw.rect(screen, "red", self.rect, 2)
        self.destroy()
    
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def display_score():    
    time = pg.time.get_ticks()//1000 - start_time
    score = font.render(f'score: {time}', False, "orangered2")
    score_rect = score.get_rect(midright = (800, 50))
    screen.blit(score, score_rect)
    return time

def collision_sprite():
    if pg.sprite.spritecollide(player.sprite, obstacle_group, False):
        print("rectangles collided")
        if pg.sprite.spritecollide(player.sprite, obstacle_group, False, pg.sprite.collide_mask):
            print("masks collided")
            pg.time.delay(1400)
            obstacle_group.empty()
            return False
        else:
            return True
    else:
        return True

pg.init()
# SETTINGS #######
FPS = 60
width = 800
height = 400
game_active = False
start_time = 0
score = 0
bg_music = pg.mixer.Sound("sounds/Ben_10.mp3")
bg_music.set_volume(0.5)
bg_music.play(loops = -1)
##################
screen = pg.display.set_mode((width, height), vsync = 1)
pg.display.set_caption("heatblast runner")

clock = pg.time.Clock()
font = pg.font.Font("font/technology.ttf", 50)
font2 = pg.font.Font("font/technology.ttf", 32)
font3 = pg.font.Font("font/technology.ttf", 20)
#################
# SURFACES #############################################
player = pg.sprite.GroupSingle()
player.add(Player())
obstacle_group = pg.sprite.Group()

background = pg.image.load("graphics/background.png").convert()
ground = pg.image.load("graphics/ground.jpg").convert()
game_over = pg.image.load("graphics/game_over.jpg").convert()

text = font.render('heatblast runner', False, 'red')
text_rect = text.get_rect(center = (width/2, 50))

credit = font3.render('sprites by : subvercetti from spriters resource', False, 'black')
credit_rect = credit.get_rect(midright = (800, 370))

# intro screen
player_stand = pg.image.load("graphics/player/idle/stance2.png").convert_alpha()
player_stand = pg.transform.rotozoom(player_stand, 0, 2.5)
player_stand_rect = player_stand.get_rect(center = (400, 200))

title = font.render("heatblast runner", True, 'green')
title_rect = title.get_rect(center = (400, 50))

ins = font2.render("press space to start", True, 'green')
ins_rect = ins.get_rect(midbottom = (400, 390))
#########################################################
# timer
obstacle_timer = pg.USEREVENT + 1
pg.time.set_timer(obstacle_timer, 1500)

#main loop
run = True
while run:
    for event in pg.event.get():
        if (event.type == pg.QUIT) or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            run = False
            # sys.exit()

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(["drone", 'robot', 'robot', 'robot'])))
        else:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    game_active = True
                    start_time = pg.time.get_ticks()//1000
                
    if game_active:
        screen.blit(background, (0, 0))
        screen.blit(ground, (0, 340))
        screen.blit(text, text_rect)
        screen.blit(credit, credit_rect)
        score = display_score()
        
        # Collision
        game_active = collision_sprite()
        
        # update
        player.update()
        obstacle_group.update()

        # draw
        player.draw(screen)
        obstacle_group.draw(screen)
        
    else:
        screen.blit(game_over, (0,0))
        screen.blit(title, title_rect)
        screen.blit(player_stand, player_stand_rect)

        score_surf = font2.render(f'score:{score}', True, 'green')
        score_surf_rect = score_surf.get_rect(midbottom = (400, 390))

        if score == 0:
            screen.blit(ins, ins_rect)
        else:
            screen.blit(score_surf, score_surf_rect)

    pg.display.update()
    clock.tick(FPS)

pg.quit()
quit()
