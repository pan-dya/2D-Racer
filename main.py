# Libraries needed
import pygame
import math

# Image scaler to resize images easily
def scaleImage(img,factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img,size)

# importing the images into the game
BACKGROUND = scaleImage(pygame.image.load("images/Background.png"), 1.2)
TRACK = scaleImage(pygame.image.load("images/Track.png"), 1.2)

FINISH = scaleImage(pygame.image.load("images/Finish.png"), 0.15)
FINISHLINE_MASK = pygame.mask.from_surface(FINISH)
TRACKBORDER = scaleImage(pygame.image.load("images/Track-Border.png"), 1.2)
MASK = pygame.mask.from_surface(TRACKBORDER)

PLAYER1CAR = scaleImage(pygame.image.load("images/redCar.png"), 0.07)
PLAYER2CAR = scaleImage(pygame.image.load("images/whiteCar.png"), 0.07)

CONTROLS = scaleImage(pygame.image.load("images/controls.png"), 0.5)

# setting the size of the game
WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cool Racing Game!")

# fonts in the game
pygame.font.init()
FONT = pygame.font.SysFont("Arial", 56, True)
FONT2 = pygame.font.SysFont("Harlowsolid", 44)
FONT3 = pygame.font.SysFont("Hightowertext", 25)

# ------------------
# -----CLASSES------
# ------------------

class Car:
    def __init__(self, maxSpeed, turnSpeed):
        self.maxSpeed = maxSpeed
        self.turnSpeed = turnSpeed
        self.acceleration = 0.005
        self.image = self.IMAGE
        self.x, self.y = self.POSITION
        self.speed = 0
        self.direction = 180
    
    # rotation function for turning the cars
    def rotation (self, turn = 0):
        if turn == 1:
            self.direction += self.turnSpeed
        elif turn == -1:
            self.direction -= self.turnSpeed

    # move function using the radians of the car's angle
    def move(self):
        radians = math.radians(self.direction)
        self.x -= self.speed*math.sin(radians)
        self.y -= self.speed*math.cos(radians)

    # moving functions to move forward and backward
    def moving(self):
         if self.speed >= self.maxSpeed:
            self.speed == self.maxSpeed
            self.move()
        if self.speed < self.maxSpeed:
            self.speed += self.acceleration
            self.move()
    
    def movingBack(self):
        self.speed = max(self.speed - self.acceleration, -self.maxSpeed/2)
        self.move()

    # creating a new image that has rotated the old image 
    def blitRotate(self, disp, topLeft):
        rotated_image = pygame.transform.rotate(self.image, self.direction)
        new_rect = rotated_image.get_rect(center = self.image.get_rect(topleft= topLeft).center)
        disp.blit(rotated_image, new_rect)

    # draw function
    def drawCar(self, disp):
        self.blitRotate(disp, (self.x, self.y))

    # checking the mask if it intersects with the car(s)
    def collide(self, mask, x=0, y =0):
        car_mask = pygame.mask.from_surface(self.image)
        offset = (int(self.x - x), int(self.y - y))
        intersect = mask.overlap(car_mask, offset)
        return intersect

    # car bounce function
    def bounce (self):
        self.speed = -self.speed
        self.move()

# PLAYER CAR CLASSES 
class Player1(Car):
    IMAGE = PLAYER1CAR
    POSITION = (1320,320)

class Player2(Car):
    IMAGE = PLAYER2CAR
    POSITION = (1350,320)

# Game class, game info and such
class game:
    def __init__(self, winner = None, player1w = 0, player2w = 0 ):
        self.start = False # if True, then the game can start
        self.player1w = player1w
        self.player2w = player2w
        self.winner = winner
    
    # a function to start the game by simply changing game.start to True
    def gameStart(self):
        self.start = True
    
    # Counter function for the winner of each race
    def player1wins(self):
        self.player1w +=1 
    
    def player2wins(self):
        self.player2w += 1
    
    def gameFinish(self):
        if self.player1w == 5:
            self.winner = "Player 1"
            return self.winner, self.player1w == 5 #return the winner name and condition for the winner
    # When player 1 number of races win is 5, then the winner will be player 1, same for the other way round
        elif self.player2w == 5:
            self.winner = "Player 2"
            return self.winner, self.player2w == 5

    def reset(self):
        self.start = False
        self.player1w = 0
        self.player2w = 0
    
    def nextRace(self):
        self.start = False

# --------------
# ----EXTRAS----
# --------------

# Reset
def reset():
    player_car.x, player_car.y = (1320,320)
    player_car.direction = 180
    player_car.speed = 0
    player_car2.x, player_car2.y = (1350,320)
    player_car2.direction = 180
    player_car2.speed = 0

# draw function to blit the images onto the game
def draw(disp, images, player_car, player_car2, Game):
    for img,pos in images:
        disp.blit(img, pos)

    player1win = (FONT3.render(f"player 1 win(s): {Game.player1w}", 1, (255,255,255)))
    disp.blit(player1win, (15,10))

    player2win = (FONT3.render(f"player 2 win(s): {Game.player2w}", 1, (255,255,255)))
    disp.blit(player2win, (15,40))

    player_car.drawCar(disp)
    player_car2.drawCar(disp)
    pygame.display.update()

# Calling the classes
player_car = Player1(0.7, 1)
player_car2 = Player2(0.7, 1)
Game = game()

gameRun = True
images= [(BACKGROUND, (0,0)),(TRACK, (0,0)), (FINISH, (1300, 280)), (TRACKBORDER, (0,0))]

# -----------------
# ----MAIN LOOP----
# -----------------

while gameRun:
    
    # blitting the images
    draw(WIN, images, player_car, player_car2, Game)
    pygame.display.update()

    # Start the race
    while Game.start == False:
        render = FONT.render("Press any button to start the race!", 1 , (255,255,255))
        WIN.blit(render, (450,380))
        WIN.blit(CONTROLS, (400,0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
        # pressing any button will start the race
            if event.type == pygame.KEYDOWN:
                Game.gameStart()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameRun = False
            break
    
    # -----KEYS-----

    keysPressed = pygame.key.get_pressed()
    
    # player 1's keys
    if keysPressed[pygame.K_a]:
        player_car.rotation(turn = 1)
    if keysPressed[pygame.K_d]:
        player_car.rotation(turn = -1)
    if keysPressed[pygame.K_w]:
        player_car.moving()
    if keysPressed[pygame.K_s]:
        player_car.movingBack()

    # player 2's keys
    if keysPressed[pygame.K_LEFT]:
        player_car2.rotation(turn = 1)
    if keysPressed[pygame.K_RIGHT]:
        player_car2.rotation(turn = -1)
    if keysPressed[pygame.K_UP]:
        player_car2.moving()
    if keysPressed[pygame.K_DOWN]:
        player_car2.movingBack()

    if player_car.collide(MASK):
        player_car.bounce()
    if player_car2.collide(MASK):
        player_car2.bounce()

    # -----HANDLE CONDIIIONS------
    
    # to stop players  from cheating and finishing the game early
    intersection = player_car.collide(FINISHLINE_MASK, 1300,300)
    if intersection:
        player_car.bounce()
    # If the player touches the finich line from the other side
    elif player_car.collide(FINISHLINE_MASK, 1300,295):
        reset() #position resets
        Game.nextRace() #start a new race
        Game.player1wins() #add 1 win to the player

    intersection2 = player_car2.collide(FINISHLINE_MASK, 1300,300)
    if intersection2:
        player_car2.bounce()
    elif player_car2.collide(FINISHLINE_MASK, 1300,295):
        reset()
        Game.nextRace()
        Game.player2wins()

    # If game finished, 
    if Game.gameFinish():
        winText = FONT2.render(f"{Game.winner} won the game!", 1 , (255,255,255))
        WIN.blit(winText, (550,380)) # bllit the text onto the screen
        pygame.display.update()
        pygame.time.delay(5000) #wait 5 sec
        # new game
        reset() 
        Game.reset()

pygame.quit()
