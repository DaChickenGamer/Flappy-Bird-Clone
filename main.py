import pygame
from random import randint

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

pipe_list = []

class Pipe:
    def __init__(self):
        gap = 250
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
        if playerPosition.colliderect(self.top_pipe) or playerPosition.colliderect(self.bottom_pipe):
            game_state.change_state("GameOver")

        if self.bottom_pipe.x < screenWidth / 2 and not self.made_next_pipe:
            new_pipe = Pipe()
            pipe_list.append(new_pipe)
            self.made_next_pipe = True

        if self.bottom_pipe.x < 0:
            pipe_list.remove(self)

class GameState:
    def __init__(self):
        self.current_state = "StartMenu"

    def change_state(self, new_state):
        self.current_state = new_state

        if new_state == "StartMenu":
            self.start_menu()
        elif new_state == "GameOver":
            self.game_over()
        elif new_state == "StartGame":
            self.start_game()

    def start_menu(self):
        self.current_state = "StartMenu"
        while self.current_state == "StartMenu":
            screen.fill((0, 0, 0))

            title_text = pygame.font.SysFont('Times New Roman', 60).render("Flappy Bird", True, (255, 255, 255))
            title_rect = title_text.get_rect(center=(screenWidth / 2, screenHeight / 4))
            screen.blit(title_text, title_rect)

            start_text = pygame.font.SysFont('Arial', 40).render("Press ENTER to Start", True, (255, 255, 255))
            start_rect = start_text.get_rect(center=(screenWidth / 2, screenHeight / 2))
            screen.blit(start_text, start_rect)

            quit_text = pygame.font.SysFont('Arial', 40).render("Press ESC to Quit", True, (255, 255, 255))
            quit_rect = quit_text.get_rect(center=(screenWidth / 2, screenHeight * 3 / 4))
            screen.blit(quit_text, quit_rect)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.change_state("StartGame")
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return

    def game_over(self):
        self.current_state = "GameOver"
        pygame.font.init()
        game_over_text = pygame.font.SysFont('Times New Roman', 50).render("GAME OVER", True, (255, 255, 255))

        text_rect = game_over_text.get_rect()
        text_rect.center = (screenWidth / 2, screenHeight / 2)

        screen.fill((0, 0, 0))
        screen.blit(game_over_text, text_rect)

        pygame.display.update()

        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    waiting_for_input = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    waiting_for_input = False

        self.change_state("StartMenu")

    def start_game(self):
        self.current_state = "StartGame"

        global pipe_list
        pipe_list = []

        first_pipe = Pipe()
        first_pipe.make_pipe()

        while self.current_state == "StartGame":
            for event in pygame.event.get():
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
                pipe.move_pipe()

            pygame.display.update()
            clock.tick(60)

game_state = GameState()
game_state.change_state("StartMenu")
