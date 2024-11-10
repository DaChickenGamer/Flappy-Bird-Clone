from random import random, randint

import pygame

screenWidth = 800
screenHeight = 800

pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Flappy Bird')
screen.fill((0, 0, 0))
pygame.display.flip()

playerImage = pygame.image.load('images/amongus.png')
playerImage = pygame.transform.scale(playerImage, (100, 100))

playerPosition = playerImage.get_rect()
playerPosition.y = screenHeight / 2
playerPosition.x = screenWidth / 2
pygame.display.update()
clock = pygame.time.Clock()

running = True
pipe_list = []



class Pipe:
    def __init__(self):
        gap = 200

        random_pipe_length = randint(100, screenHeight - gap - 100)

        pipe_image = pygame.image.load("images/flappybird.png")
        pipe_image = pygame.transform.rotate(pipe_image, 180)

        self.scaled_pipe_image = pygame.transform.scale(pipe_image, (50, random_pipe_length))

        bottom_pipe_height = screenHeight - random_pipe_length - gap
        flipped_pipe_image = pygame.transform.scale(pipe_image, (50, bottom_pipe_height))
        self.flipped_pipe_image = pygame.transform.flip(flipped_pipe_image, False, True)

        self.top_pipe = self.scaled_pipe_image.get_rect()
        self.bottom_pipe = self.flipped_pipe_image.get_rect()

        self.top_pipe.y = 0
        self.bottom_pipe.y = screenHeight - bottom_pipe_height

        self.top_pipe.x = screenWidth
        self.bottom_pipe.x = screenWidth

        self.made_next_pipe = False
    def make_pipe(self):
        pipe_list.append(self)

    def move_pipe(self):
        self.bottom_pipe.x -= 3
        self.top_pipe.x -= 3

        if self.bottom_pipe.x < screenWidth / 2 and not self.made_next_pipe:
            new_pipe = Pipe()
            pipe_list.append(new_pipe)
            self.made_next_pipe = True

        if self.bottom_pipe.x < 0:
            pipe_list.remove(self)

    # def get_pipe_x(self):
    #     if not self.bottom_pipe.x == self.top_pipe.x:
    #         print("Error, Pipe X Doesn't Match")
    #         return
    #
    #     return self.bottom_pipe.x

testPipe = Pipe()
testPipe.make_pipe()

while running:

    for pipe in pipe_list:
        pipe.move_pipe()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_SPACE]:
            playerPosition.y -= 45
        if pressed[pygame.K_ESCAPE]:
            pygame.quit()

    playerPosition.y += 3

    screen.fill((0, 0, 0))

    screen.blit(playerImage, playerPosition)
    for pipe in pipe_list:
        screen.blit(pipe.scaled_pipe_image, pipe.top_pipe)
        screen.blit(pipe.flipped_pipe_image, pipe.bottom_pipe)

    pygame.display.update()
    clock.tick(60)
