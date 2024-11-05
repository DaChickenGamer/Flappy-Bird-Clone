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

pipeImage = pygame.image.load("images/Among_Us_Impostor_text.png")
pipeImage = pygame.transform.rotate(pipeImage, 180)

playerPosition = playerImage.get_rect()
playerPosition.y = screenHeight/2
playerPosition.x = screenWidth/2
pygame.display.update()
clock = pygame.time.Clock()

running = True

while running:
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

    pygame.display.update()
    clock.tick(60)