# imports several modules used
import math
import pygame
import random
from random import randint

# pygame initializers
pygame.font.init()
pygame.mixer.init()
pygame.init()

color = (255, 255, 255)  # color used for many texts
# creates window
FONT = pygame.font.SysFont('comicsans', 30)  # font used for player points and enemy current HP
FPS = 25  # caps frame rate

# basic pygame window setup
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
cyan = (50, 200, 160)
# initializes clock
clock = pygame.time.Clock()

K = 4000
# custom user events

COOLDOWN = pygame.USEREVENT + 1
pygame.time.set_timer(COOLDOWN, 5000)

SPAWN_EVIL = pygame.USEREVENT + 2
pygame.time.set_timer(SPAWN_EVIL, 5000)

ENEMY_MOVEMENT = pygame.USEREVENT + 3
pygame.time.set_timer(ENEMY_MOVEMENT, 2000)

ENEMY_SHOT = pygame.USEREVENT + 4
pygame.time.set_timer(ENEMY_SHOT, K)

EXPLANATION = pygame.USEREVENT + 5
pygame.time.set_timer(EXPLANATION, 5000)
# sprites
spaceship_sprite = pygame.image.load('think_create_spaceship.png')
spaceship_scaled = pygame.transform.scale(spaceship_sprite, (75, 75))
enemy_sprite = pygame.image.load('think_enemy1.png')
enemy_scaled = pygame.transform.scale(enemy_sprite, (75, 75))
# used to display game rules
explain = ['1']


# algorithm done
# data types done
# 7 functions done
# classes/ objects done

class Player(pygame.sprite.Sprite):  # player template for game
    def __init__(self):
        super(Player, self).__init__()
        self.image = spaceship_scaled
        self.rect = self.image.get_rect()
        self.rect.x = 600 // 2
        self.rect.y = 800 - self.rect.height
        self.speed = 8
        self.hp = 3
        self.points = 0

    def update(self):
        if self.hp <= 0:
            self.kill()


class Enemy(pygame.sprite.Sprite):  # enemy template for game
    def __init__(self):
        super(Enemy, self).__init__()
        self.image = enemy_scaled
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH)
        self.rect.y = 50
        self.speed = 5
        self.hp = 10


player = Player()  # player object
enemy = Enemy()  # enemy object

# sprite group allows for drawing on pygame screen
sprite_group = pygame.sprite.Group()
sprite_group.add(player)
sprite_group.add(enemy)


def draw_screen(player_ammo, enemy_bullet):  # handles screen drawing 
    screen.fill(cyan)  # gives background color
    sprite_group.draw(screen)  # draws all objects to screen

    HP_TEXT = FONT.render("Enemy HP " + str(enemy.hp), 1, color)  # used to render enemy HP
    screen.blit(HP_TEXT, (WIDTH - HP_TEXT.get_width() - 10, 5))

    POINT_COUNT = FONT.render('Points ' + str(player.points), 1, color)  # ticks whenever player gets points
    screen.blit(POINT_COUNT, (225, 5))

    PLAYER_HP = FONT.render('Player HP ' + str(player.hp), 1, color)  # used for to render player HP
    screen.blit(PLAYER_HP, (0, 5))

    for bullet in player_ammo:  # draws all bullet objects by the player on the screen
        pygame.draw.rect(screen, color, bullet)

    for bullet in enemy_bullet:  # draws all bullet objects created by the enemy
        pygame.draw.rect(screen, color, bullet)

    if len(explain) != 0:  # used to display initial instructions for the game
        explanation_font = FONT.render('hit the enemy 10 times to get points', 1, color)
        explanation_2 = FONT.render('the enemy will fire back', 1, color)
        explanation_3 = FONT.render('lose 3 hp and you lose', 1, color)
        screen.blit(explanation_font, (0, 200))
        screen.blit(explanation_2, (0, 300))
        screen.blit(explanation_3, (0, 400))
    pygame.display.update()


def handle_bullets(player_ammo):  # this function handles collision and movement of bullets
    for bullet in player_ammo:
        bullet.y -= 30
        if bullet.y > HEIGHT or bullet.y < 0:
            player_ammo.remove(bullet)


def handle_collision(player_ammo):  # handles all collision
    if player.rect.colliderect(enemy):
        player.hp -= 1
    for bullet in player_ammo:
        if enemy.rect.colliderect(bullet):
            enemy.hp -= 1
            player_ammo.remove(bullet)


def handle_player_movement(keys_pressed,
                           player):  # function allows for game to receive input from the player to create
    if keys_pressed[pygame.K_a]:  # movement
        player.rect.x -= player.speed
    if keys_pressed[pygame.K_d]:
        player.rect.x += player.speed
    if player.rect.x > WIDTH:
        player.rect.x = 0
    if player.rect.x < 0:
        player.rect.x = WIDTH


def handle_enemy_bullet(enemy_bullet):  # used to handle drawing and collision of enemy bullets
    for bullet in enemy_bullet:
        bullet.y += 20
        if bullet.colliderect(player):
            player.hp -= 1
            enemy_bullet.remove(bullet)
        elif bullet.y > HEIGHT:
            enemy_bullet.remove(bullet)


def enemy_movement(enemy, L):  # gives enemy randomized movement
    movement_CD = random.randint(5, 10)
    if movement_CD != 0 or enemy.rect.x - enemy.speed > 0 or enemy.rect.x + enemy.speed < WIDTH:
        if L == 1:
            enemy.rect.x += enemy.speed
        if L == 2:
            enemy.rect.x -= enemy.speed
    if enemy.rect.x + enemy.speed > WIDTH:
        enemy.rect.x = 0
    elif enemy.rect.x - enemy.speed < 0:
        enemy.rect.x = WIDTH - enemy.speed


def end_game(lose_text):  # occurs once player HP equals zero
    END_TEXT = FONT.render(lose_text, 1, color)
    screen.blit(END_TEXT, (WIDTH // 2 - END_TEXT.get_width() // 2, HEIGHT // 2 - END_TEXT.get_width() // 2))
    pygame.display.update()
    pygame.time.delay(5000)


# algorithm
def main(player):  # main game loop
    player_ammo = []  # used to display bullets on screen
    overheat = []  # takes in bullets alongside player ammo to prevent bullet spamming
    enemy_bullet = []
    L = 1
    while True:
        # handles FPS
        clock.tick(FPS)
        # handles events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:  # allows for keyboard input
                if event.key == pygame.K_SPACE and len(overheat) < 5:
                    bullet = pygame.Rect(player.rect.x + 30, player.rect.y + 50 // 2 - 2, 10, 5)
                    player_ammo.append(bullet)
                    overheat.append(bullet)
                    print(player_ammo)

            if event.type == COOLDOWN and len(overheat) != 0:  # resets cooldown
                overheat.clear()

            if event.type == ENEMY_MOVEMENT:
                L = random.randint(0, 2)

            if event.type == ENEMY_SHOT:  # used to allow enemy to shoot
                bullet = pygame.Rect(enemy.rect.x + 30, enemy.rect.y + 50 // 2 - 2, 10, 15)
                enemy_bullet.append(bullet)

            if event.type == EXPLANATION:
                if len(explain) != 0:
                    explain.pop(0)
                else:
                    pass

        if enemy.hp == 0:
            player.points += 1
            enemy.hp = 10

        if player.hp == 0:
            lose_text = "you lose"
            end_game(lose_text)
            break

        keys_pressed = pygame.key.get_pressed()  # allows for holding down on keys
        handle_player_movement(keys_pressed, player)
        handle_bullets(player_ammo)
        handle_collision(player_ammo)  # uses different data types and is looped
        draw_screen(player_ammo, enemy_bullet)
        enemy_movement(enemy, L)
        handle_enemy_bullet(enemy_bullet)


main(player)
