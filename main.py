import pygame
import predictitAppProject
from urllib.request import urlopen
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

#stores how many markets you can prev and next to (must be an even number)
TOTALMARKETSSTORED = 30

fadeClock = 0

#used to track prev and next markets
marketIDOrder = []
marketIDOrderPlace = 0

data = predictitAppProject.Data()
marketID = data.getRandomMarketID()
# newMarketID = marketID
marketNumber = data.getIndexOfID(marketID)

WhiteRectangle = pygame.Rect(0, 0, WIDTH, HEIGHT)

#BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/Grenade+1.mp3')
#BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/Gun+Silencer.mp3')

INFO_FONT = pygame.font.SysFont('comicsans', 10)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
gui_font = pygame.font.Font(None,30)

#FPS = 60
FPS = 50
NUMBEROFCOLUMNS = 5
# VEL = 5
# BULLET_VEL = 7
# MAX_BULLETS = 3
# SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
MARKETVALUEPLACE = 8
VALUESLIST=['Market ID','Market Name','Contract ID','Contract Name','PredictIt Yes','bestBuyNoCost','BestSellYesCost','BestSellNoCost','image']


YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
FADERATIO = .33


fadeClockCap = 300
transperency = 0

#initialize image
#create data from predictitAppProject


marketNumber = 0




def draw_window(image, nextButton, backButton):

    global fadeClock
    global marketID

    #value below is the markets with the same id
    markets = data.getMarketsWithID(marketID)

    pygame.draw.rect(WIN, WHITE, WhiteRectangle)


    fade(image, fadeClock)
 
    WIN.blit(image, (WIDTH* .85, HEIGHT*.75))

    #depth and width of text
    depth = 10
    width = 10
    marketName = INFO_FONT.render(str(VALUESLIST[0]) + ": " +str(markets[0][1]), 1, BLACK)
    fade(marketName, fadeClock)
    WIN.blit(marketName, (width, depth))
    depth += 20
    resetdepth = 30

    for i in range(len(markets)):
        for j in range(6):
            # value = data.getData()[marketNumber][index]
            text = INFO_FONT.render(str(VALUESLIST[j+2]) + ": " +str(markets[i][j+2]), 1, BLACK)
            fade(text, fadeClock)
            WIN.blit(text, (width,depth))
            depth += 20
        depth = resetdepth
        width += 150
        if((i+1) % NUMBEROFCOLUMNS == 0):
            width = 10
            resetdepth += 6*20+30
            depth = resetdepth


    #code for the fade counter in the app 
    nextButton.draw()
    backButton.draw()

    WIN.blit(INFO_FONT.render("Fade Timer: " + str(fadeClock), 1, BLACK), (10, 450))
    pygame.display.update()



# def draw_winner(text):
#     draw_text = WINNER_FONT.render(text, 1, WHITE)
#     WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
#                          2, HEIGHT/2 - draw_text.get_height()/2))
#     pygame.display.update()
#     pygame.time.delay(5000)

#fades an object put into it, using the fadeClock to determine how much fade it should have
def fade(fadingValue, fadeClock):
    if(fadeClock < fadeClockCap * FADERATIO):
        fadingValue.set_alpha(int((256*fadeClock/fadeClockCap)*1/FADERATIO))

    elif(fadeClock > fadeClockCap * (1-FADERATIO)):
        fadingValue.set_alpha(int((256*(1-fadeClock/fadeClockCap))*1/FADERATIO)-3)

    else:
        fadingValue.set_alpha(256)


def main():
    # red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    # yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    # red_bullets = []
    # yellow_bullets = []

    # red_health = 10
    # yellow_health = 10

    #track the markets that are being used
    global marketIDOrder
    global marketIDOrderPlace

    clock = pygame.time.Clock()
    run = True
    global fadeClock
    global marketID
    # global newMarketID
    global marketNumber

    newMarketID = marketID
    marketIDOrder.append(newMarketID)
    marketIDOrderPlace += 1

    #initialize image
    image_url = data.getData()[marketNumber][MARKETVALUEPLACE]
    image_str = urlopen(image_url).read()
    # create a file object (stream)
    image_file = io.BytesIO(image_str)
    # load the image from a file or stream
    image = pygame.image.load(image_file)
    image = pygame.transform.smoothscale(image, (100, 100)) 
    # image = pygame.transform.scale(image, (100, 100))

    #button
    nextButton = Button('Next Button',200,40,(WIDTH*.6,HEIGHT*.8),5)
    backButton = Button('Back Button',200,40,(WIDTH*.1,HEIGHT*.8),5)

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
            #         bullet = pygame.Rect(
            #             yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
            #         yellow_bullets.append(bullet)
            #         #BULLET_FIRE_SOUND.play()

            #     if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
            #         bullet = pygame.Rect(
            #             red.x, red.y + red.height//2 - 2, 10, 5)
            #         red_bullets.append(bullet)
            #         #BULLET_FIRE_SOUND.play()

            # if event.type == RED_HIT:
            #     red_health -= 1
            #     #BULLET_HIT_SOUND.play()

            # if event.type == YELLOW_HIT:
            #     yellow_health -= 1
            #     #BULLET_HIT_SOUND.play()
            
        #change the marketnumber if fadeClock >= fadeClockCap
        fadeClock += 1
        if(fadeClock >= fadeClockCap):
            #get a new market
            while(newMarketID == marketID):
                newMarketID = data.getRandomMarketID()
            marketID = newMarketID
            marketNumber = data.getIndexOfID(marketID)
            fadeClock = 0

            marketIDOrder.append(newMarketID)
            marketIDOrderPlace += 1

            #change the image here
            image_url = data.getData()[marketNumber][MARKETVALUEPLACE]
            image_str = urlopen(image_url).read()
            # create a file object (stream)
            image_file = io.BytesIO(image_str)
            # load the image from a file or stream
            image = pygame.image.load(image_file)
            image = pygame.transform.smoothscale(image, (100, 100)) 

        keys_pressed = pygame.key.get_pressed()


        draw_window(image, nextButton, backButton)

        #ensure marketIDOrder isnt too big
        if(len(marketIDOrder) >= TOTALMARKETSSTORED):
            marketIDOrder = marketIDOrder[int(TOTALMARKETSSTORED/2):]
            marketIDOrderPlace = TOTALMARKETSSTORED/2
    main()


class Button:
    def __init__(self,text,width,height,pos,elevation):
        #Core attributes 
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elecation = elevation
        self.original_y_pos = pos[1]

        # top rectangle 
        self.top_rect = pygame.Rect(pos,(width,height))
        self.top_color = '#475F77'

        # bottom rectangle 
        self.bottom_rect = pygame.Rect(pos,(width,height))
        self.bottom_color = '#354B5E'
        #text
        self.text = text
        self.text_surf = gui_font.render(text,True,'#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

    def draw(self):
        # elevation logic 
        self.top_rect.y = self.original_y_pos - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center 

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

        pygame.draw.rect(WIN,self.bottom_color, self.bottom_rect,border_radius = 12)
        pygame.draw.rect(WIN,self.top_color, self.top_rect,border_radius = 12)
        WIN.blit(self.text_surf, self.text_rect)
        self.check_click()	

    def check_click(self):
        global fadeClock
        global marketID
        global marketIDOrder
        global marketIDOrderPlace

        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#D74B4B'
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elecation = 0
                self.pressed = True
            else:
                self.dynamic_elecation = self.elevation
                if self.pressed == True:
                    #next button and back button logic
                    if self.text == 'Next Button':
                        if(len(marketIDOrder) == marketIDOrderPlace):
                            fadeClock = fadeClockCap
                        else:
                            marketID = marketIDOrder[marketIDOrderPlace]
                            marketIDOrderPlace += 1
                            fadeClock = 10
                    if self.text == 'Back Button':
                        if(marketIDOrderPlace == 1):
                            fadeClock = 10
                        else:        
                            marketID = marketIDOrder[marketIDOrderPlace-2]
                            marketIDOrderPlace -= 1
                            fadeClock = 10
                    self.pressed = False
        else:
            self.dynamic_elecation = self.elevation
            self.top_color = '#475F77'



if __name__ == "__main__":
    main()