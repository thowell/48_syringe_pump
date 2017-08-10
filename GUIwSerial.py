# Taylor Howell 2015
# 4.0 Includes Serial Commuication with PySerialArduino 2.0
# 8-13-2015

import pygame
import time
import timeit
import math as m
#import serial

### Serial Setup ###
usbport = 'COM8' # defines the serial port location
    # Assign Arduino's serial port address
    #   Windows example
    #     usbport = 'COM3'
    #   Linux example
    #     usbport = '/dev/ttyACM0'
    #   MacOSX example
    #     usbport = '/dev/tty.usbserial-FTALLOK2'

#ser = serial.Serial(usbport,9600,timeout=1) # set up Serial communication
#ser.flushInput() # clears serial inputs
#ser.flushOutput()# clears serial outputs

### Pygame Setup ###
pygame.init() # initialize Pygame
#pygame.mouse.set_visible(False) # hides mouse pointer

display_width = 320 # screen width
display_height = 240 # screen height
black = (0,0,0) 
white = (245,245,245) 
grayblue = (32,178,170)
red = (255,165,0)
green = (127,255,0)
red_bright = (255,140,0)
green_bright = (50,205,50)

gameDisplay = pygame.display.set_mode((display_width,display_height)) # Add pygame.FULLSCREEN to make display take over entire window;define the screen size
pygame.display.set_caption('pumpGUI') # sets window tab name
clock = pygame.time.Clock() # frame buffer setup

smallText = pygame.font.SysFont(None,18)
mediumText = pygame.font.SysFont(None,20)
largeText = pygame.font.SysFont(None,30)

### Motor Setup ###
motorFullSteps = 200*5.2 #gear ratio motor 5.2:1
microstepping = 8.0 #1,2,8,16
lead = 1.25 # mm 
steps = motorFullSteps*microstepping # total number of steps per revolution due to microstepping
displacementPerStep = lead/steps # mm

### Tables ###
#volumeDisplay = 0 
volumeFlowDisplay = 0 # Flow volume toggle button index
volumeFlushDisplay = 0 # Flush volume toggle button index
volumeWithdrawDisplay = 0 # Withdraw volume toggle button index
volumeSym = ['mL','uL'] # Volume toggle button values
volumeConvert = [10**3,1] # Volume conversion to uL, dependent on volume___Display
#flowrateDisplay = 0 # Flow rate toggle button index
flowrateFlowDisplay = 0 # Flow flowrate toggle button index
flowrateFlushDisplay = 0 # Flush flowrate toggle button index
flowrateWithdrawDisplay = 0 # Withdraw flowrate toggle button index
flowrate = ['mL/min','mL/hr','uL/min','uL/hr'] # flowrate toggle button values
flowrateConvert = [100.0/6,1.0/3.6,1.0/60,1.0/3600] # flowrate conversion to uL/second, dependent on flowrate___Display
materialDisplay = 0 # syringe material index
material = ['plastic','glass','metal'] # syringe material values
brandDisplay = 0 # syringe brand index
brand = ['BD','CUSTOM'] # syringe brand values
syringeDisplay = 0 # syring size index
syringe = ['1','3','5','10'] # syringe size values
diameter = [4.7,8.59,11.99,14.48] # syring size corresponding internal diameters in mm
previousScreen = '' # string containing the function name of the previous display screen

### Volumes and Rates ###
flowVolume = '---' # flow volume stored as string
flowRate = '---' # flow flowrate stored as string
flushVolume = '---' # flush volume stored as string
flushRate = '---' # flush flowrate stored as string
withdrawVolume = '---' # withdraw volume stored as string
calc = '' # current input from the numberpad
ID = '---' # current input for internal diameter in mm
entry = [flowVolume,flowRate,flushVolume,flushRate,withdrawVolume,ID] # matrix of values to store the entered numberpad value
numLocation = None # index for storing numberpad value in entry matrix 
decimal = False # determines if numberpad input has a decimal
pause = False # determines if process is paused

### Motor Functions ###

def up():
    """ Up Function:
    Pauses between calls before serially writing message to Arduino"""
    time.sleep(.1)
    #ser.write(b"up,1,1,")
    #ser.flushOutput()
    print('Up')

def down():
    """ Down Function:
    Pauses between calls before serially writing message to Arduino"""
    time.sleep(.1)
    #ser.write(b"down,1,1,")
    #ser.flushOutput()
    print('Down')
    
### GUI functions ###

def pausing():
    """ Pausing:
    returns pause variable as true and calls pause function"""
    global pause
    pause = True
    paused()
    
def unpause():
    print("unpause")
    """ Unpausing:
    returns pause variable as false and serially writes message to Arduino"""
    global pause
    pause = False
    #ser.write('u'.encode())
    time.sleep(.1)
    #ser.flushOutput()
    
def canceling():
    print("canceling")
    """Canceling:
    serially writes message to Arduino before returning to homescreen"""
    #ser.write('s'.encode())
    time.sleep(.3)
    #ser.flushOutput()
    homescreen()
    
def paused():
    global TIC,totalTime
    print("paused")
    """Pause Screen:
    serially writes message to Arduino before pausing until instructed """
    #ser.write('p'.encode())
    time.sleep(.3)
    #ser.flushOutput()
    while pause:
        pygame.event.get()
        gameDisplay.fill(black)
        TextSurface, TextRectangle = text_objects("PAUSED",largeText,white)
        TextRectangle.center = ((display_width/2),(2*display_height/5))
        gameDisplay.blit(TextSurface,TextRectangle)
        circleButton("RESUME",100,175,30,green,green,green,3,unpause)
        circleButton("CANCEL", 220, 175,30, red,red, red,3,canceling)
        pygame.display.update()
        clock.tick(60)
    time.sleep(.3)
    TIC = timeit.default_timer()
    totalTime = totalTime - .7
    
def materialToggle():
    print("material toggle")
    global materialDisplay

    if materialDisplay == 0:
        i = 1
    if materialDisplay == 1:
        i = 2
    if materialDisplay == 2:
        i = 0
    
    materialDisplay = i
    time.sleep(.3)
    
def brandToggle():
    print("brand toggle")
    global brandDisplay

    if brandDisplay == 0:
        i = 1
    if brandDisplay == 1:
        i = 0
        
    brandDisplay = i
    time.sleep(.3)

def syringeToggle():
    print("syringe toggle")
    global syringeDisplay

    if syringeDisplay == 0:
        i = 1
    if syringeDisplay == 1:
        i = 2
    if syringeDisplay == 2:
        i = 3
    if syringeDisplay == 3:
        i = 0
        
    syringeDisplay = i
    time.sleep(.3)

def quitProgram():
    pygame.quit()
    quit()

def text_objects(text, font, color):
    textSurface = font.render(text,True,color)
    return textSurface,textSurface.get_rect()

def text_locations(x,y,message,font,color):
    textSurf, textRect = text_objects(message,font,color)
    textRect.center = ((x ,y))
    gameDisplay.blit(textSurf,textRect)

def rectButton(message,x,y,width,height,textColor,inactiveColor,activeColor,thickness,action=None):
    mouse = pygame.mouse.get_pos() # mouse positions as input
    click = pygame.mouse.get_pressed() # mouse clicks for right,left, middle button
    
    if x + width > mouse[0] > x   and y + height > mouse[1] > y and click != (0,0,0):
        pygame.draw.rect(gameDisplay, activeColor, (x,y,width,height),thickness)
        textSurf, textRect = text_objects(message,smallText,activeColor)
        textRect.center = ((x + (width/2),y + (height/2)))
        gameDisplay.blit(textSurf,textRect)
        if action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, inactiveColor, (x,y,width,height), thickness) 
        textSurf, textRect = text_objects(message,smallText,textColor)
        textRect.center = ((x + (width/2),y + (height/2)))
        gameDisplay.blit(textSurf,textRect)

def numEntryButton(message,x,y,width,height,textColor,inactiveColor,activeColor,thickness,location,action=None):
    mouse = pygame.mouse.get_pos() # mouse positions as input
    click = pygame.mouse.get_pressed() # mouse clicks for right,left, middle button
    global numLocation
    numLocation = location
    
    if x + width > mouse[0] > x   and y + height > mouse[1] > y and click != (0,0,0):
        pygame.draw.rect(gameDisplay, activeColor, (x,y,width,height),thickness)
        textSurf, textRect = text_objects(message,smallText,activeColor)
        textRect.center = ((x + (width/2),y + (height/2)))
        gameDisplay.blit(textSurf,textRect)
        if action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, inactiveColor, (x,y,width,height), thickness) 
        textSurf, textRect = text_objects(message,smallText,textColor)
        textRect.center = ((x + (width/2),y + (height/2)))
        gameDisplay.blit(textSurf,textRect)
        
'''def circleButton(message,x,y,radius, textColor, inactiveColor,activeColor,thickness,action=None):
    mouse = pygame.mouse.get_pos() # mouse positions as input
    click = pygame.mouse.get_pressed() # mouse clicks for right,left, middle button
    
    if x + radius > mouse[0] > x - radius and y + radius > mouse[1] > y - radius:
        pygame.draw.circle(gameDisplay, activeColor, (x,y),radius,thickness)
        textSurf, textRect = text_objects(message,smallText,activeColor)
        textRect.center = ((x,y))
        gameDisplay.blit(textSurf,textRect)
        if click != (0,0,0) and action != None:
            action()       
    else:
        pygame.draw.circle(gameDisplay, inactiveColor, (x,y), radius, thickness) 
        textSurf, textRect = text_objects(message,smallText,textColor)
        textRect.center = ((x,y))
        gameDisplay.blit(textSurf,textRect)'''

def circleButton(message,x,y,radius, textColor, inactiveColor,activeColor,thickness,action=None):
    mouse = pygame.mouse.get_pos() # mouse positions as input
    click = pygame.mouse.get_pressed() # mouse clicks for right,left, middle button
    
    if x + radius > mouse[0] > x - radius and y + radius > mouse[1] > y - radius and click != (0,0,0):
        pygame.draw.circle(gameDisplay, activeColor, (x,y),radius,thickness)
        textSurf, textRect = text_objects(message,smallText,activeColor)
        textRect.center = ((x,y))
        gameDisplay.blit(textSurf,textRect)
        if action != None:
            action()       
    else:
        pygame.draw.circle(gameDisplay, inactiveColor, (x,y), radius, thickness) 
        textSurf, textRect = text_objects(message,smallText,textColor)
        textRect.center = ((x,y))
        gameDisplay.blit(textSurf,textRect)
    

def numberButton(number,location,message,x,y,radius, textColor, inactiveColor,activeColor,thickness,action=None):
    mouse = pygame.mouse.get_pos() # mouse positions as input
    click = pygame.mouse.get_pressed() # mouse clicks for right,left, middle button
    global calc
    if x + 1*radius > mouse[0] > x - 1*radius and y + 1*radius > mouse[1] > y - 1*radius and click != (0,0,0):
        pygame.draw.circle(gameDisplay, activeColor, (x,y),radius,thickness)
        textSurf, textRect = text_objects(message,mediumText,activeColor)
        textRect.center = ((x,y))
        gameDisplay.blit(textSurf,textRect)
        if click != (0,0,0) and message != '.':
            calc = calc + message
            if action !=None:
                action()
            time.sleep(.1)
        elif click != (0,0,0) and message == '.' and decimal == False:
            calc = calc + message
            if action !=None:
                decimalRestrict()
            time.sleep(.1)
    else:
        pygame.draw.circle(gameDisplay, inactiveColor, (x,y), radius, thickness) 
        textSurf, textRect = text_objects(message,mediumText,textColor)
        textRect.center = ((x,y))
        gameDisplay.blit(textSurf,textRect)
    
    time.sleep(.005)
    
def decimalRestrict():
    global decimal
    decimal = True
    
def enterButton():
    print("enter button")
    global flowVolume,flowRate,flushVolume,flushRate,withdrawVolume,calc,decimal,previousScreen,ID
    if calc == '':
        numberpad()
    if calc == '.':
        numberpad()
    
    decimal = False
    x = float(calc)
    calc = ''
    if numLocation == 0:
        flowVolume = x
        flowScreen()
    if numLocation == 1:
        flowRate = x
        flowScreen()
    if numLocation == 2:
        flushVolume = x
        flushScreen()
    if numLocation == 3:
        flushRate = x
        flushScreen()
    if numLocation == 4:
        withdrawVolume = x
        withdrawScreen()
    if numLocation == 5:
        ID = x
        previousScreen()
        
    
def backspaceButton():
    print("backspace button")
    global calc,decimal
    
    if calc == '':
        numberpad()
    if calc[-1] == '.':
        decimal = False
    if calc == '':
        numberpad()
    else:
        x = calc[:-1]
        calc = x
        
    time.sleep(.2)
    
def volumeFlowToggle():
    print("volume flow toggle")
    global volumeFlowDisplay
    
    if volumeFlowDisplay == 0:
        i = 1
    elif volumeFlowDisplay == 1:
        i = 0
        
    volumeFlowDisplay = i
    time.sleep(.3)
    
def volumeWithdrawToggle():
    print("volume withdraw toggle")
    global volumeWithdrawDisplay
    
    if volumeWithdrawDisplay == 0:
        i = 1
    elif volumeWithdrawDisplay == 1:
        i = 0
        
    volumeWithdrawDisplay = i
    time.sleep(.3)
    
def volumeFlushToggle():
    print("volume flush toggle")
    global volumeFlushDisplay
    
    if volumeFlushDisplay == 0:
        i = 1
    elif volumeFlushDisplay == 1:
        i = 0
        
    volumeFlushDisplay = i
    time.sleep(.3)

def flowrateFlowToggle():
    print("flowrate flow toggle")
    global flowrateFlowDisplay

    if flowrateFlowDisplay == 0:
        i = 1
    if flowrateFlowDisplay == 1:
        i = 2
    if flowrateFlowDisplay == 2:
        i = 3
    if flowrateFlowDisplay == 3:
        i =  0
        
    flowrateFlowDisplay = i
    time.sleep(.3)

def flowrateFlushToggle():
    print("flowrate flush toggle")
    global flowrateFlushDisplay

    if flowrateFlushDisplay == 0:
        i = 1
    if flowrateFlushDisplay == 1:
        i = 2
    if flowrateFlushDisplay == 2:
        i = 3
    if flowrateFlushDisplay == 3:
        i =  0
        
    flowrateFlushDisplay = i
    time.sleep(.3)

def flowrateWithdrawToggle():
    print("flowrate withdraw toggle")
    global flowrateWithdrawDisplay

    if flowrateWithdrawDisplay == 0:
        i = 1
    if flowrateWithdrawDisplay == 1:
        i = 2
    if flowrateWithdrawDisplay == 2:
        i = 3
    if flowrateWithdrawDisplay == 3:
        i =  0
        
    flowrateWithdrawDisplay = i
    time.sleep(.3)

### SCREENS ###
def homescreen():
    print("homescreen")
    #ser.flushOutput()
    time.sleep(.3)
    global previousScreen
    previousScreen = homescreen
    while not False:

        pygame.event.get()
        gameDisplay.fill(black) # creates background
        circleButton("UP DOWN",100,70,40,white,white,grayblue,3,updownScreen)
        circleButton("FLOW",100,240-70,40,white,white,grayblue,3,flowScreen)
        circleButton('WITHDRAW',320-100,70,40,white,white,grayblue,3,withdrawScreen)
        circleButton("FLUSH",320- 100,240-70,40,white,white,grayblue,3,flushScreen)
        circleButton("QUIT", 320-30,240-30,20,red,red,red,3,quitProgram)
        text_locations(display_width/2,230,'TAYLOR HOWELL 2015',smallText,white)
        pygame.display.update() # updates entire surface, giving input will only update input
        clock.tick(60) # frames per second
        
def updownScreen():
    time.sleep(.3)
    global previousScreen
    previousScreen = updownScreen
    while not False:

        pygame.event.get()
        gameDisplay.fill(black) # creates background
        circleButton("UP",160,70,40,white,white,grayblue,3,up)
        circleButton("DOWN",160,240-70,40,white,white,grayblue,3,down)
        circleButton("HOME",320-40,240-40,30,red,red,red,3,homescreen)

        pygame.display.update() # updates entire surface, giving input will only update input
        clock.tick(60) # frames per second

def flowScreen():
    print("flowscreen")
    global previousScreen
    previousScreen = flowScreen
    time.sleep(.3)
    while not False:

        pygame.event.get()
        gameDisplay.fill(black) # creates background
        circleButton("HOME",320-40,240-40,30,red,red,red,3,homescreen)
        rectButton(brand[brandDisplay],25,192,60,25,white,white,grayblue,3,brandToggle)
        rectButton(material[materialDisplay],100,192,60,25,white,white,grayblue,3,materialToggle)
        rectButton(syringe[syringeDisplay] + "cc",175,192,60,25,white,white,grayblue,3,syringeToggle)
        circleButton(volumeSym[volumeFlowDisplay],170,42,30,white,white,grayblue,3,volumeFlowToggle)
        circleButton(flowrate[flowrateFlowDisplay],170,117,30,white,white,grayblue,3,flowrateFlowToggle)
        circleButton("RUN", 320-65, 75, 40,green,green,green,3,flowRunScreen)
        numEntryButton(str(flowVolume),25,25,100,35,white,white,grayblue,3,0,numberpad)
        numEntryButton(str(flowRate),25,100,100,35,white,white,grayblue,3,1,numberpad)
        if brand[brandDisplay] == 'CUSTOM':
            numEntryButton('CUSTOM ID: ' + str(ID) + ' mm',25,157,210,25,grayblue,grayblue,grayblue,3,5,numberpad)
        pygame.display.update() # updates entire surface, giving input will only update input
        clock.tick(60) # frames per second

def withdrawScreen():
    print("withdrawscreen")
    time.sleep(.3)
    global previousScreen
    previousScreen = withdrawScreen
    while not False:

        pygame.event.get()
        gameDisplay.fill(black) # creates background
        circleButton("HOME",320-40,240-40,30,red,red,red,3,homescreen)
        rectButton(brand[brandDisplay],25,192,60,25,white,white,grayblue,3,brandToggle)
        rectButton(material[materialDisplay],100,192,60,25,white,white,grayblue,3,materialToggle)
        rectButton(syringe[syringeDisplay] + "cc",175,192,60,25,white,white,grayblue,3,syringeToggle)
        circleButton(volumeSym[volumeWithdrawDisplay],170,75,30,white,white,grayblue,3,volumeWithdrawToggle)
        circleButton("WITHDRAW", 320-65, 75, 40,green,green,green,3,withdrawRunScreen)
        numEntryButton(str(withdrawVolume),25,57,100,35,white,white,grayblue,3,4,numberpad)
        if brand[brandDisplay] == 'CUSTOM':
            numEntryButton('CUSTOM ID: ' + str(ID) + ' mm',25,157,210,25,grayblue,grayblue,grayblue,3,5,numberpad)
        pygame.display.update() # updates entire surface, giving input will only update input
        clock.tick(60) # frames per second

def flushScreen():
    print("flushscreen")
    time.sleep(.3)
    global previousScreen
    previousScreen = flushScreen
    while not False:

        pygame.event.get()
        gameDisplay.fill(black) # creates background
        circleButton("HOME",320-40,240-40,30,red,red,red,3,homescreen)
        numEntryButton(str(flushVolume),25,25,100,35,white,white,grayblue,3,2,numberpad)
        numEntryButton(str(flushRate),25,100,100,35,white,white,grayblue,3,3,numberpad)
        rectButton(brand[brandDisplay],25,192,60,25,white,white,grayblue,3,brandToggle)
        rectButton(material[materialDisplay],100,192,60,25,white,white,grayblue,3,materialToggle)
        rectButton(syringe[syringeDisplay] + "cc",175,192,60,25,white,white,grayblue,3,syringeToggle)
        circleButton(volumeSym[volumeFlushDisplay],170,42,30,white,white,grayblue,3,volumeFlushToggle)
        circleButton(flowrate[flowrateFlushDisplay],170,117,30,white,white,grayblue,3,flowrateFlushToggle)
        if brand[brandDisplay] == 'CUSTOM':
            numEntryButton('CUSTOM ID: ' + str(ID) + ' mm',25,157,210,25,grayblue,grayblue,grayblue,3,5,numberpad)
        circleButton("RUN", 320-65, 75, 40,green,green,green,3,flushRunScreen)
        pygame.display.update() # updates entire surface, giving input will only update input
        clock.tick(60) # frames per second
        
def numberpad():
    print("numberpad")
    time.sleep(.3)
    while not False:

        pygame.event.get()
        gameDisplay.fill(black) # creates background
        circleButton("RETURN",320-40,240-40,30,red,red,red,3,previousScreen)
        numberButton(1,None,"1",35,85,25,white,white,grayblue,3,None)
        numberButton(2,None,"2",95,85,25,white,white,grayblue,3,None)
        numberButton(3,None,"3",155,85,25,white,white,grayblue,3,None)
        numberButton(4,None,"4",35,145,25,white,white,grayblue,3,None)
        numberButton(5,None,"5",95,145,25,white,white,grayblue,3,None)
        numberButton(6,None,"6",155,145,25,white,white,grayblue,3,None)
        numberButton(7,None,"7",35,205,25,white,white,grayblue,3,None)
        numberButton(8,None,"8",95,205,25,white,white,grayblue,3,None)
        numberButton(9,None,"9",155,205,25,white,white,grayblue,3,None)
        numberButton(0,None,"0",215,85,25,white,white,grayblue,3,None)
        numberButton(None, None,".",215,145,25,white,white,grayblue,3,decimalRestrict)
        circleButton("<-",215,205,25,white,white,red,3,backspaceButton)
        circleButton("ENTER",280,40, 30, green,green,green, 3, enterButton)
        rectButton(str(calc),10,10,230,40,white,white,white,3,None)
        pygame.display.update() # updates entire surface, giving input will only update input
        clock.tick(60) # frames per second
        
def volumeHighScreen():
    print("volume high screen")
    time.sleep(.3)
    while True:
        pygame.event.get()
        gameDisplay.fill(black)
        text_locations(display_width/2,display_height*2/7,'Volume Excedes Syringe Size',mediumText,white)
        text_locations(display_width/2,display_height*3/7,'Reduce volume or modify syringe selection',mediumText,white)
        circleButton("RETURN",160,200,30,red,red,red,3,previousScreen)
        pygame.display.update()
        clock.tick(60)

def flowHighScreen():
    print("flow high screen")
    time.sleep(.3)
    while True:
        pygame.event.get()
        gameDisplay.fill(black)
        text_locations(display_width/2,display_height*2/7,'Flowrate Beyond Operating Speed',mediumText,white)
        text_locations(display_width/2,display_height*3/7,'Modify flowrate or syringe selection',mediumText,white)
        circleButton("RETURN",160,200,30,red,red,red,3,previousScreen)
        pygame.display.update()
        clock.tick(60)
    
def flowRunScreen():
    print("flowrunscreen")
    time.sleep(.3)
    global totalTime,TIC,ID,displacementPerStep,volumeFlowDisplay,flowrateFlowDisplay,flowrate,flowVolume,flowRate,volumeConvert,flowrateConvert,diameter,syringeDisplay
    if type(flowVolume) == str or type(flowRate) == str or flowVolume == 0.0 or flowRate == 0.0:
        flowScreen()
    if brand[brandDisplay] == 'CUSTOM' and type(ID) == str:
       flowScreen()
    if brand[brandDisplay] == 'CUSTOM' and type(ID) != str:
        area = ((ID/2)**2)*m.pi
    else:
        area = ((diameter[syringeDisplay]/2)**2)*m.pi
    volume = flowVolume*volumeConvert[volumeFlowDisplay]
    rate = flowRate*flowrateConvert[flowrateFlowDisplay] 
    verticalDistance = volume/area # mm
    numberSteps = verticalDistance/displacementPerStep
    totalTime = (volume/rate) # seconds
    timeStep = ((totalTime/numberSteps)/2)*10**6 # Microseconds
    
    if volume/1000 > float(syringe[syringeDisplay]) and brand[brandDisplay] != 'CUSTOM':
        volumeHighScreen()
    currentSteps = 0
    if timeStep < 50 or timeStep > 10*10**7:
        flowHighScreen()
   
    var = "flow,%i," % numberSteps
    var += "%i," % timeStep
    print(var)
    #ser.write(var.encode())
    time.sleep(.2)
    #ser.flushOutput()
    
    print('Flow Volume: ' + str(volume))
    print('Flow Rate: ' + str(rate))
    print('Number of Steps: ' + str(numberSteps))
    print('Total Time: ' + str(totalTime))
    print('Time Step: ' + str(timeStep))
    print('Area: ' + str(area))
    
    tic = timeit.default_timer()
    t = 0
    while t < totalTime:
        TIC = timeit.default_timer()
        pygame.event.get()
        gameDisplay.fill(black) # creates background
        circleButton('PAUSE',160,205,28, red, red,red,3,pausing)
        pygame.draw.rect(gameDisplay, white, (25,130,270,20),3)
        pygame.draw.rect(gameDisplay, green, (31,136,258*t/totalTime,8),0)
        text_locations(display_width/2,20,'FLOWING',mediumText,green)
        textSurf, textRect = text_objects(volumeSym[volumeFlowDisplay],mediumText,white)
        textRect.center = ((218,60))
        gameDisplay.blit(textSurf,textRect)
        textSurf, textRect = text_objects(flowrate[flowrateFlowDisplay],mediumText,white)
        textRect.center = ((218,90))
        gameDisplay.blit(textSurf,textRect)
        textSurf, textRect = text_objects(str(flowVolume),mediumText,white)
        textRect.center = ((106,60))
        gameDisplay.blit(textSurf,textRect)
        textSurf, textRect = text_objects(str(flowRate),mediumText,white)
        textRect.center = ((106,90))
        gameDisplay.blit(textSurf,textRect)
        pygame.display.update()
        TOC = timeit.default_timer()
        t = t + TOC - TIC
    toc = timeit.default_timer()
    print('Run time: ' + str(toc -tic))
    print('Time Error: ' + str(totalTime -toc + tic))
    print('Complete')
    completeScreen()
    
def flushRunScreen():
    print("flushrunscreen")
    time.sleep(.3)
    global TIC,totalTime,ID,displacementPerStep,volumeFlushDisplay,flowrateFlushDisplay,flowrate,flushVolume,flushRate,volumeConvert,flowrateConvert,diameter,syringeDisplay
    if type(flushVolume) == str or type(flushRate) == str or flushVolume == 0.0 or flushRate == 0.0:
        flushScreen()
    if brand[brandDisplay] == 'CUSTOM' and type(ID) == str:
        flushScreen()
    if brand[brandDisplay] == 'CUSTOM' and type(ID) != str:
        area = ((ID/2)**2)*m.pi
    else:
        area = ((diameter[syringeDisplay]/2)**2)*m.pi
    
    volume = flushVolume*volumeConvert[volumeFlushDisplay]
    rate = flushRate*flowrateConvert[flowrateFlushDisplay]
    verticalDistance = volume/area # mm
    numberSteps = verticalDistance/displacementPerStep
    totalTime = (volume/rate) # seconds
    timeStep = ((totalTime/numberSteps)/2)*10**6 # Microseconds

    if volume/1000 > float(syringe[syringeDisplay]) and brand[brandDisplay] != 'CUSTOM':
        volumeHighScreen()
    currentSteps = 0
    if timeStep < 50 or timeStep > 10*10**7:
        flowHighScreen()
        
    currentSteps = 0

    var = "flow,%i," % numberSteps
    var += "%i," % timeStep
    print(var)
    #ser.write(var.encode())
    time.sleep(.2)
    #ser.flushOutput()
    
    print('Flush Volume: ' + str(volume))
    print('Flush Rate: ' + str(rate))
    print('Number of Steps: ' + str(numberSteps))
    print('Total Time: ' + str(totalTime))
    print('Time Step: ' + str(timeStep))
    print('Area: ' + str(area))
    
    tic = timeit.default_timer()
    t = 0
   
    while t < totalTime:
        TIC = timeit.default_timer()
        pygame.event.get()
        gameDisplay.fill(black) # creates background
        circleButton('PAUSE',160,205,28, red, red,red,3,pausing)
        pygame.draw.rect(gameDisplay, white, (25,130,270,20),3)
        pygame.draw.rect(gameDisplay, green, (31,136,258*t/totalTime,8),0)
        text_locations(display_width/2,20,'FLUSHING',mediumText,green)
        textSurf, textRect = text_objects(volumeSym[volumeFlushDisplay],mediumText,white)
        textRect.center = ((218,60))
        gameDisplay.blit(textSurf,textRect)
        textSurf, textRect = text_objects(flowrate[flowrateFlushDisplay],mediumText,white)
        textRect.center = ((218,90))
        gameDisplay.blit(textSurf,textRect)
        textSurf, textRect = text_objects(str(flushVolume),mediumText,white)
        textRect.center = ((106,60))
        gameDisplay.blit(textSurf,textRect)
        textSurf, textRect = text_objects(str(flushRate),mediumText,white)
        textRect.center = ((106,90))
        gameDisplay.blit(textSurf,textRect)
        pygame.display.update()
        TOC = timeit.default_timer()
        t = t + TOC - TIC
    toc = timeit.default_timer()
    print('Run time ' + str(toc -tic))
    print('Complete')
    completeScreen()
    print('Run time: ' + str(toc - tic))
    print('Time Error: ' + str(totalTime -toc + tic))
    print('Complete')
    completeScreen()
    
def withdrawRunScreen():
    print("flush run screen")
    time.sleep(.3)
    global TIC, totalTime,ID,pause,displacementPerStep,volumeWithdrawDisplay,volumeSym,flowrateDisplay,flowrate,flowVolume,flowRate,volumeConvert,flowrateConvert,diameter,syringeDisplay,withdrawVolume
    if type(withdrawVolume) == str or withdrawVolume == 0:
        withdrawScreen()
    if brand[brandDisplay] == 'CUSTOM' and type(ID) == str:
       withdrawScreen() 
    if brand[brandDisplay] == 'CUSTOM' and type(ID) != str:
        area = ((ID/2)**2)*m.pi
    else:
        area = ((diameter[syringeDisplay]/2)**2)*m.pi
        
    volume = withdrawVolume*volumeConvert[volumeWithdrawDisplay]
    rate = 10 # uL/s       
    verticalDistance = volume/area # mm
    numberSteps = verticalDistance/displacementPerStep
    totalTime = (volume/rate) # seconds
    timeStep = ((totalTime/numberSteps)/2)*10**6 # Microseconds

    if volume/1000 > float(syringe[syringeDisplay]) and brand[brandDisplay] != 'CUSTOM':
        volumeHighScreen()
    currentSteps = 0
    if timeStep < 50 or timeStep > 10*10**7:
        flowHighScreen()   
    currentSteps = 0
    
    var = "with,%i," % numberSteps
    var += "%i," % timeStep
    print(var)
    ser.write(var.encode())
    time.sleep(.2)
    ser.flushOutput()
    
    print('Withdraw Volume: ' + str(volume))
    print('Withdraw Rate: ' + str(rate))
    print('Number of Steps: ' + str(numberSteps))
    print('Total Time: ' + str(totalTime))
    print('Time Step: ' + str(timeStep))
    print('Area: ' + str(area))
    
    tic = timeit.default_timer()
    t = 0
 
    while t < totalTime:
        TIC = timeit.default_timer()
        pygame.event.get()
        gameDisplay.fill(black) # creates background
        circleButton('PAUSE',160,205,28, red, red,red,3,pausing)
        pygame.draw.rect(gameDisplay, white, (25,130,270,20),3)
        pygame.draw.rect(gameDisplay, green, (31,136,258*t/totalTime,8),0)
        text_locations(display_width/2,20,'WITHDRAWING',mediumText,green)
        textSurf, textRect = text_objects(volumeSym[volumeWithdrawDisplay],mediumText,white)
        textRect.center = ((218,60))
        gameDisplay.blit(textSurf,textRect)
        textSurf, textRect = text_objects(str(withdrawVolume),mediumText,white)
        textRect.center = ((106,60))
        gameDisplay.blit(textSurf,textRect)
        pygame.display.update()
        TOC = timeit.default_timer()
        t = t + TOC - TIC
    toc = timeit.default_timer()
    print('Run time ' + str(toc -tic))
    print('Time Error: ' + str(totalTime -toc + tic))
    print('Complete')
    completeScreen()
          
def completeScreen():
    print("complete screen")
    gameDisplay.fill(black) # creates background
    text_locations(display_width/2,display_height/2,'COMPLETE',largeText,white)
    pygame.display.update()
    time.sleep(3)
    
    homescreen()
###
        
#Loop
print("Bootup...")
homescreen()
