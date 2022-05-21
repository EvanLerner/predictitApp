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

marketNumber = data.getIndexOfID(marketID)

WhiteRectangle = pygame.Rect(0, 0, WIDTH, HEIGHT)

INFO_FONT = pygame.font.SysFont('comicsans', 10)
gui_font = pygame.font.Font(None,30)

FPS = 50
NUMBEROFCOLUMNS = 5
MARKETVALUEPLACE = 8
VALUESLIST=['Market ID','Market Name','Contract ID','Contract Name','PredictIt Yes','bestBuyNoCost','BestSellYesCost','BestSellNoCost','image']


FADERATIO = .33



pause = False
fadeClockCap = 300
transperency = 0

marketNumber = 0

def draw_window(image, nextButton, backButton, pauseButton):
    global fadeClock
    global marketID
    global pause
    #check if paused
    if pause:
        fadeClock = int(fadeClockCap/2)
    
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
            text = INFO_FONT.render(str(VALUESLIST[j+2]) + ": " +str(markets[i][j+2]), 1, BLACK)
            fade(text, fadeClock)
            WIN.blit(text, (width,depth))
            depth += 20
        depth = resetdepth
        width += 150
        if(i+1) >= 10:
            break
        if((i+1) % NUMBEROFCOLUMNS == 0):
            width = 10
            resetdepth += 6*20+30
            depth = resetdepth
        


    #code for the fade counter in the app 
    nextButton.draw()
    backButton.draw()
    pauseButton.draw()

    WIN.blit(INFO_FONT.render("Fade Timer: " + str(fadeClock), 1, BLACK), (10, 450))
    pygame.display.update()

#fades an object put into it, using the fadeClock to determine how much fade it should have
def fade(fadingValue, fadeClock):
    if(fadeClock < fadeClockCap * FADERATIO):
        fadingValue.set_alpha(int((256*fadeClock/fadeClockCap)*1/FADERATIO))
    elif(fadeClock > fadeClockCap * (1-FADERATIO)):
        fadingValue.set_alpha(int((256*(1-fadeClock/fadeClockCap))*1/FADERATIO)-3)
    else:
        fadingValue.set_alpha(256)


def changeImage(marketNumber):
    image_url = data.getData()[marketNumber][MARKETVALUEPLACE]
    image_str = urlopen(image_url).read()
    # create a file object (stream)
    image_file = io.BytesIO(image_str)
    # load the image from a file or stream
    image = pygame.image.load(image_file)
    image = pygame.transform.smoothscale(image, (100, 100)) 
    return image

def main():
    #track the markets that are being used

    global marketIDOrder
    global marketIDOrderPlace
    global fadeClock
    global marketID
    global marketNumber

    clock = pygame.time.Clock()
    run = True

    newMarketID = marketID
    marketIDOrder.append(newMarketID)
    marketIDOrderPlace += 1

    image = changeImage(marketNumber)


    #initialize button
    nextButton = Button('Next Button',200,40,(WIDTH*.6,HEIGHT*.8),5)
    backButton = Button('Back Button',200,40,(WIDTH*.1,HEIGHT*.8),5)
    pauseButton = Button('Pause',70,40,(WIDTH*.41,HEIGHT*.8),5)

    while run:
        clock.tick(FPS)


        #Button logic
        global pause
        if(nextButton.buttonPressed()):
            if(len(marketIDOrder) == marketIDOrderPlace):
                    fadeClock = fadeClockCap
                    pause = False
            else:
                marketID = marketIDOrder[marketIDOrderPlace]
                marketIDOrderPlace += 1
                fadeClock = 10
                pause = False
            marketNumber = data.getIndexOfID(marketID)
            image = changeImage(marketNumber)
            nextButton.switchButton()

        if(backButton.buttonPressed()):
            if(marketIDOrderPlace == 1):
                fadeClock = 10
                pause = False
            else:        
                marketID = marketIDOrder[int(marketIDOrderPlace-2)]
                marketIDOrderPlace -= 1
                fadeClock = 10
                pause = False
            marketNumber = data.getIndexOfID(marketID)
            image = changeImage(marketNumber)
            backButton.switchButton()

        if(pauseButton.buttonPressed()):
            pause = not pause
            pauseButton.switchButton()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        #change the marketnumber if fadeClock >= fadeClockCap
        fadeClock += 1

        #check for pause

        if(fadeClock >= fadeClockCap):
            #get a new market
            while(newMarketID == marketID):
                newMarketID = data.getRandomMarketID()
            marketID = newMarketID
            marketNumber = data.getIndexOfID(marketID)
            fadeClock = 0

            marketIDOrder.append(newMarketID)
            marketIDOrderPlace += 1

            # #change the image here
            # image_url = data.getData()[marketNumber][MARKETVALUEPLACE]
            # image_str = urlopen(image_url).read()
            # # create a file object (stream)
            # image_file = io.BytesIO(image_str)
            # # load the image from a file or stream
            # image = pygame.image.load(image_file)
            # image = pygame.transform.smoothscale(image, (100, 100))
            image = changeImage(marketNumber)

        keys_pressed = pygame.key.get_pressed()


        draw_window(image, nextButton, backButton, pauseButton)

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
        
        self.startEvent = False

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
        global pause

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
                    self.startEvent = True
                    self.pressed = False
        else:
            self.dynamic_elecation = self.elevation
            self.top_color = '#475F77'

    #input: 0 for nextbutton, 1 for back button, 2 for pausebutton
    #output true if button is pressed
    def buttonPressed(self):
        return self.startEvent

    #same input and output as func above, but instead switched the button pressed from true to false
    def switchButton(self):
        self.startEvent = not self.startEvent


if __name__ == "__main__":
    main()