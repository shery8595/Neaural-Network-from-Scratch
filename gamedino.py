import pygame
import os
import random

pygame.init()

SH, SW = 700, 600
global game_speed, x_pos_bg, y_pos_bg, points, obstacles, game_over

game_speed = 14
x_pos_bg = 0
y_pos_bg = 480
points = 0
font = pygame.font.Font(r'D:\arial.ttf', 20)
obstacles = []
game_over = False

SCREEN = pygame.display.set_mode((SW, SH))

# Load Images
RUNNING = [pygame.image.load(r'D:\DinoRun1.png'),
           pygame.image.load(r'D:\DinoRun2.png')]

JUMPING = pygame.image.load(r'D:\DinoJump.png')

DUCKING = [pygame.image.load(r'D:\DinoDuck1.png'),
           pygame.image.load(r'D:\DinoDuck2.png')]

SMALL_CACTUS = [pygame.image.load(r'D:\SmallCactus1.png'),
                pygame.image.load(r'D:\SmallCactus2.png'),
                pygame.image.load(r'D:\SmallCactus3.png')]
LARGE_CACTUS = [pygame.image.load(r'D:\LargeCactus1.png'),
                pygame.image.load(r'D:\LargeCactus1.png'),
                pygame.image.load(r'D:\LargeCactus1.png')]

BIRD = [pygame.image.load(r'D:\Bird-1.png'),
        pygame.image.load(r'D:\Bird-2.png')]

CLOUD = pygame.image.load(r'D:\Cloud.png')

BG = pygame.image.load(r'D:\Track.png')

class Dinosaur():
    X_Pos = 80
    Y_Pos = 410
    Y_POS_DUCK = 440
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.jump_start_y = self.Y_Pos  # Store the starting Y position
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_Pos
        self.dino_rect.y = self.Y_Pos

    def update(self):
        # Perform actions based on the current state
        if self.dino_duck:
            self.duck()
        elif self.dino_jump:
            self.jump()
        else:
            self.run()

        if self.step_index >= 10:
            self.step_index = 0

    def run(self):
        if self.step_index >= 10:
            self.step_index = 0
        self.image = self.run_img[self.step_index // 5]
        self.step_index += 1
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_Pos
        self.dino_rect.y = self.Y_Pos

    def duck(self):
        if self.step_index >= 10:
            self.step_index = 0
        self.image = self.duck_img[self.step_index // 5]
        self.step_index += 1
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_Pos
        self.dino_rect.y = self.Y_POS_DUCK

    def jump(self):
        if self.dino_jump:
            if self.jump_vel >= -self.JUMP_VEL:
                self.dino_rect.y -= self.jump_vel * 4
                self.jump_vel -= 0.8
            else:
                self.dino_jump = False
                self.jump_vel = self.JUMP_VEL
        else:
            # Ensure the dinosaur returns to the original position
            if self.dino_rect.y < self.jump_start_y:
                self.dino_rect.y += self.jump_vel * 4
                self.jump_vel += 0.8
                # Clamp the velocity and position to ensure it doesn't go below the original
                if self.jump_vel > self.JUMP_VEL:
                    self.jump_vel = self.JUMP_VEL
                if self.dino_rect.y > self.jump_start_y:
                    self.dino_rect.y = self.jump_start_y
            else:
                self.dino_rect.y = self.jump_start_y
                self.image = self.run_img[0]  # Reset to running image when not jumping

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


class Cloud():

     def __init__(self):
        self.x = SW + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

     def update(self):
        self.x -= game_speed
        if self.x < 0:
            self.x = SW + random.randint(800, 1000)
            self.y = random.randint(0, 100)

     def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))    

class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SW

    def update(self):
        self.rect.x -= game_speed
        

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)
          
class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 420


class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 400


class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 350
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1



