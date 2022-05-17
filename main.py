import pygame
import os
import predictitAppProject
from urllib.request import urlopen
import requests
import io

pygame.font.init()
pygame.mixer.init()


WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Predictit App")
pygame_icon = pygame.image.load('pygameicon.png')
pygame.display.set_icon(pygame_icon)


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

WhiteRectangle = pygame.Rect(0, 0, WIDTH, HEIGHT)

#BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/Grenade+1.mp3')
#BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/Gun+Silencer.mp3')

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
MARKETVALUEPLACE = 8

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

fadeClock = 0

#create data from predictitAppProject
data = predictitAppProject.Data()
firstValues = data.getData()[0]
marketNumber = 0

image_url = data.getData()[marketNumber][MARKETVALUEPLACE]
image_str = urlopen(image_url).read()
# create a file object (stream)
image_file = io.BytesIO(image_str)
# load the image from a file or stream
image = pygame.image.load(image_file)



def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, marketNumber):

    pygame.draw.rect(WIN, WHITE, WhiteRectangle)


    # draw image, position the image ulc at x=20, y=20
    WIN.blit(image, (20, 20))

    #draw the names of firstValues
    depth = 10
    for text in data.getData()[marketNumber]:
        WIN.blit(HEALTH_FONT.render(str(text), 1, BLACK), (10,depth))
        depth += 40
    WIN.blit(HEALTH_FONT.render("Fade Counter: " + str(fadeClock), 1, BLACK), (10, depth))
    pygame.display.update()



def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True
    
    global fadeClock
    marketNumber = 0
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    #BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    #BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                #BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                #BULLET_HIT_SOUND.play()
            
        fadeClock += 1
        if(fadeClock >= 200):
            marketNumber += 100
            fadeClock = 0

            #get image
            global image
            image_url = data.getData()[marketNumber][MARKETVALUEPLACE]
            image_str = urlopen(image_url).read()
            # create a file object (stream)
            image_file = io.BytesIO(image_str)
            # load the image from a file or stream
            image = pygame.image.load(image_file)

        keys_pressed = pygame.key.get_pressed()


        draw_window(red, yellow, red_bullets, yellow_bullets,
                    red_health, yellow_health, marketNumber)

    main()


if __name__ == "__main__":
    main()