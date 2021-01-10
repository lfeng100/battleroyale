import pygame
import random
import parallax
# This module was taken of the internet and is used to implement scrolling backgrounds
from spritesheet import SpriteSheet
# This module was created to use spritesheets (Take parts of an image out of a larger one)

pygame.mixer.pre_init()
pygame.init()
# Initiates pygame module and mixer add-on for music

fontOneSmall = pygame.font.Font("font\gameFont.ttf", 35)
fontOneMedium = pygame.font.Font("font\gameFont.ttf", 50)
fontOneLarge = pygame.font.Font("font\gameFont.ttf", 80)
fontTwoTiny = pygame.font.Font("font\gameFont2.ttf", 20)
fontTwoSmall = pygame.font.Font("font\gameFont2.ttf", 35)
fontTwoMedium = pygame.font.Font("font\gameFont2.ttf", 50)
fontTwoLarge = pygame.font.Font("font\gameFont2.ttf", 70)
# game fonts

bgOne = pygame.image.load("bg\gameOne.jpg")
bgTwo = pygame.image.load("bg\gameTwo.jpg")
bgThree = pygame.image.load("bg\gameThree.png")
bgOne = pygame.transform.scale(bgOne, [800, 640])
bgTwo = pygame.transform.scale(bgTwo, [800, 640])
bgThree = pygame.transform.scale(bgThree, [800, 640])
# game backgrounds

pygame.display.set_caption("Battle Royale")
# Window name

black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
turq = (0, 204, 204)
yellow = (255, 255, 0)
grey = (100, 100, 100)
# Colour varaibles

winWidth = 800
winHeight = 640

winSize = (winWidth, winHeight)
screen = pygame.display.set_mode(winSize)
# Creating the window

pygame.mixer.music.load("music\menu.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)
musicOn = False
# Starting music

oneLeftAttack = 0
twoLeftAttack = 0
oneRightCrouch = 0
twoCrouching = False
oneCrouching = False
oneCrouchTime = 0
twoCrouchTime = 0
oneAttackTime = 0
twoAttackTime = 0
playerOneHealth = 100
playerTwoHealth = 100
twoPreviousAttack = 0
onePreviousAttack = 0
twoPreviousHit = 0
onePreviousHit = 0
pause = False
twoDamage = 0
twoY = 0
twoX = 0
oneDamage = 0
oneY = 0
oneX = 0
oneWin = False
twoWin = False
# Constants used to determine positioning and actions.

class PlayerOne(pygame.sprite.Sprite):
    def __init__(self):
    # Will initiate once when called

        super().__init__()
        self.change_x = 0
        self.change_y = 0
        self.move = False
        # Player is not moving at start

        self.walking_frames_l = []
        self.walking_frames_r = []

        self.jumping_frames_l = []
        self.jumping_frames_r = []

        self.attacking_frames_l = []
        self.attacking_frames_r = []

        self.crouching_frames_l = []
        self.crouching_frames_r = []

        self.hit_frames_l = []
        self.hit_frames_r = []
        # Lists of all the sprites used

        self.level = None

        sprite_sheet = SpriteSheet("char\guy3\GuyThree.png")
        global oneVictorys
        global oneDefeat
        oneVictorys = sprite_sheet.get_image(120, 240, 55, 90)
        oneDefeat = sprite_sheet.get_image(0, 190, 75, 80)

        image = sprite_sheet.get_image(0, 0, 30, 80)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(60, 0, 40, 80)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(120, 0, 40, 80)
        self.walking_frames_r.append(image)

        image = sprite_sheet.get_image(0, 0, 30, 80)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(60, 0, 40, 80)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(120, 0, 40, 80)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)

        image = sprite_sheet.get_image(240, 0, 30, 90)
        self.jumping_frames_r.append(image)

        image = sprite_sheet.get_image(240, 0, 30, 90)
        image = pygame.transform.flip(image, True, False)
        self.jumping_frames_l.append(image)

        image = sprite_sheet.get_image(0, 110, 65, 74)
        self.attacking_frames_l.append(image)

        image = sprite_sheet.get_image(0, 110, 65, 74)
        image = pygame.transform.flip(image, True, False)
        self.attacking_frames_r.append(image)

        image = sprite_sheet.get_image(120, 93, 50, 80)
        self.crouching_frames_l.append(image)

        image = sprite_sheet.get_image(120, 93, 50, 80)
        image = pygame.transform.flip(image, True, False)
        self.crouching_frames_r.append(image)

        image = sprite_sheet.get_image(180, 70, 60, 100)
        self.hit_frames_l.append(image)
        image = sprite_sheet.get_image(300, 75, 60, 90)
        self.hit_frames_l.append(image)

        image = sprite_sheet.get_image(180, 70, 60, 100)
        image = pygame.transform.flip(image, True, False)
        self.hit_frames_r.append(image)
        image = sprite_sheet.get_image(300, 75, 60, 90)
        image = pygame.transform.flip(image, True, False)
        self.hit_frames_r.append(image)
        # Locates sprites one the sprite sheet I created and adds the images to respective lists
        # There are 2 versions of each sprite, one facing left and one facing right depending on character direction (Some images are flipped for this reason)

        self.image = self.walking_frames_l[0]
        # Starting sprite

        self.rect = self.image.get_rect()
        # Creates rectangle around sprite and gets dimensions/positioning

        self.attacking = False
        self.crouching = False
        self.oneHit = False
        self.time = 0
        # Sets up some variables for later (sprite/keyboard interactions)

        self.health = 100
        self.direction = "L"
        # Starting Health and Direction

    def update(self):
        self.gravity()
        # Implements gravity function (below)

        self.rect.x += self.change_x
        # Updates character's x-position each frame

        pos = self.rect.x
        # Used to create walking animation

        if self.rect.y < 470:
            if self.direction == "R":
                self.image = self.jumping_frames_r[0]
            else:
                self.image = self.jumping_frames_l[0]
            # If sprite is in the air, change to jumping sprite


            if self.crouching == True:
                if self.rect.y < 460:
                    self.rect.y += 10
            # If crouching in the air, move down to the ground faster

        else:
            if self.direction == "R":
                frame = (pos // 25) % len(self.walking_frames_r)
                self.image = self.walking_frames_r[frame]
            else:
                frame = (pos // 25) % len(self.walking_frames_l)
                self.image = self.walking_frames_l[frame]
            # Creates walking animation using 3 sprites, changes depending on 'pos' variable which measures distance
            # (basically changes sprite after player moves a certain distance)

            if self.move == False:
                if self.direction == "R":
                    self.image = self.walking_frames_r[0]
                else:
                    self.image = self.walking_frames_l[0]
            # If player is not moving, revert to default standing sprite

        if self.attacking == True:
            if self.direction == "R":
                self.image = self.attacking_frames_r[0]
            else:
                global oneLeftAttack
                if oneLeftAttack == 0 and self.crouching == False:
                    self.rect.x -= 30
                    oneLeftAttack += 1
                # Used to position sprite correctly because flipped image is off-centered

                self.image = self.attacking_frames_l[0]
            # Changes sprite when attacking
        if self.crouching == True:
            if self.direction == "R":
                global oneRightCrouch
                if oneRightCrouch == 0:
                    self.rect.x -= 20
                    oneRightCrouch += 1
                # Again, used to position sprite correctly because flipped image is off-centered
                self.image = self.crouching_frames_r[0]
            else:
                self.image = self.crouching_frames_l[0]
            # Changes sprite when crouching

        if self.oneHit == True:
            if self.rect.y < 470:
                if self.direction == "R":
                    self.image = self.hit_frames_r[0]
                    self.change_x -= 0.75
                else:
                    self.image = self.hit_frames_l[0]
                    self.change_x += 0.75
            # When player is hit, spritesprite falls to the ground

            if self.move == False and self.rect.y > 460:
                self.change_x = 0
                global oneDamage
                oneDamage = 0
                if self.direction == "R":
                    self.image = self.hit_frames_r[1]
                else:
                    self.image = self.hit_frames_l[1]
                if gameTime > self.time:
                    self.oneHit = False
            # Resets variables when player is not moving
                    
        if self.health <= 0:
            global twoWin
            twoWin = True
            global playerOneHealth
            playerOneHealth = 0
        # If player is below 0 health, game ends

        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                self.rect.left = block.rect.right
        # If player sprite is touching a platform's x-position, it stays in the position (doesn't move)

        self.rect.y += self.change_y
        # updates player y-position

        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)

        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
            self.change_y = 0
        # If player sprite is touching a platform's y-position, it stays in the position (doesn't move)

    def jump(self):
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2
        if len(platform_hit_list) > 0 or self.rect.bottom >= winHeight:
            self.change_y = -8
    # First checks if player is able to jump by quickly changing it's y-position and detecting collision.
    # If the player is not hitting anything, they jump (change y-change variable)

    def gravity(self):
        if self.change_y == 0:
            self.change_y = 2
        else:
            self.change_y += .65
        # If character on the ground, they stay there, else, they fall down at 0.65 pixels per frame
        if self.rect.y >= winWidth - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = winHeight - self.rect.height
        # Checks if character is on the ground, if so, their y-position does not change

    def go_left(self):
        if self.crouching == True:
            pass
        else:
            self.move = True
            self.change_x = -6
            self.direction = "L"
        # When player presses key, this function is called. Player moves 6 pixels left each frame.
        # Player direction is set to left so appropriate sprite is used; Cannot move while crouching.

    def go_right(self):
        if self.crouching == True:
            pass
        else:
            self.move = True
            self.change_x = 6
            self.direction = "R"
        # When player presses a key, this function is called. Player moves 6 pixels right each frame.
        # Player direction is set to right so appropriate sprite is usedCannot move while crouching.

    def stop(self):
        self.change_x = 0
        self.move = False
        # When player stops pressing movement key, their x-change is zero

    def attack(self):
        global onePreviousAttack
        global oneLeftAttack
        onePreviousAttack = pygame.time.get_ticks() + 500
        self.attacking = True
        oneLeftAttack = 0
        # The previous attack timer allows player to attack only every 500 milliseconds
        # Creates variable attacking so sprite is changed

    def stop_attack(self):
        global oneLeftAttack
        self.attacking = False
        if oneLeftAttack == 1:
            self.rect.x += 30
            oneLeftAttack = 0
        # When player is no longer attacking, the sprite reverts to the original image.
        # The oneLeftAttack variable is to reposition the sprite because it is off centre (Everytime function is called it's x-position is changed).

    def crouch(self):
        global oneRightCrouch
        global oneCrouching
        self.crouching = True
        oneRightCrouch = 0
        oneCrouching = True
        # Uses variable to change sprite to crouching/blocking position
        # oneRightCrouch is used to reposition again

    def uncrouch(self):
        global oneRightCrouch
        global oneCrouching
        self.crouching = False
        if oneRightCrouch == 1:
            self.rect.x += 20
            oneRightCrouch = 0
        oneCrouching = False
        # When player is no longer pressing crouch key, the sprite reverts to the original image.

    def hit(self):
        global onePreviousHit
        global playerOneHealth
        global oneDamage
        global oneX
        global oneY
        onePreviousHit = pygame.time.get_ticks() + 500
        self.oneHit = True
        self.rect.y -= 50
        if self.direction == "R":
            self.rect.x -= 20
        else:
            self.rect.x += 20
        # Player sprite is hit up into air  and back so x and y positions are changed
        self.time = pygame.time.get_ticks() + 500
        oneDamage = random.randint(3, 5)
        critical = random.randint(1, 8)
        if critical == 8:
            oneDamage *= 2
        self.health -= oneDamage
        # Generates a damage amount from 3-5, 1 in 8 chance for critical hit or double damage.
        # Global variables are used to display damage amounts on the screen
        playerOneHealth = self.health
        # Sets global player health
        oneX = self.rect.x
        oneY = self.rect.y
        # These global variables are used to determine where the damage coutner should be displayed

class PlayerTwo(pygame.sprite.Sprite):
    # Identical to Player One Class (except for some positioning due to varying sprite sizes). Refer PlayerOne function.

    def __init__(self):
        super().__init__()
        self.move = False
        self.change_x = 0
        self.change_y = 0

        self.walking_frames_l = []
        self.walking_frames_r = []

        self.jumping_frames_l = []
        self.jumping_frames_r = []

        self.attacking_frames_l = []
        self.attacking_frames_r = []

        self.crouching_frames_l = []
        self.crouching_frames_r = []

        self.hit_frames_l = []
        self.hit_frames_r = []

        self.level = None

        sprite_sheet = SpriteSheet("char\guy4\guyFour.png")
        global twoVictorys
        global twoDefeat
        twoVictorys = sprite_sheet.get_image(120, 240, 50, 100)
        twoDefeat = sprite_sheet.get_image(0, 190, 75, 80)

        image = sprite_sheet.get_image(0, 0, 50, 75)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(60, 0, 50, 75)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(120, 0, 50, 75)
        self.walking_frames_r.append(image)

        image = sprite_sheet.get_image(0, 0, 50, 75)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(60, 0, 50, 75)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(120, 0, 50, 75)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)

        image = sprite_sheet.get_image(240, 0, 45, 65)
        self.jumping_frames_r.append(image)

        image = sprite_sheet.get_image(240, 0, 45, 65)
        image = pygame.transform.flip(image, True, False)
        self.jumping_frames_l.append(image)

        image = sprite_sheet.get_image(0, 110, 80, 75)
        self.attacking_frames_r.append(image)

        image = sprite_sheet.get_image(0, 110, 80, 75)
        image = pygame.transform.flip(image, True, False)
        self.attacking_frames_l.append(image)

        image = sprite_sheet.get_image(180, 100, 50, 78)
        self.crouching_frames_r.append(image)

        image = sprite_sheet.get_image(180, 100, 50, 78)
        image = pygame.transform.flip(image, True, False)
        self.crouching_frames_l.append(image)

        image = sprite_sheet.get_image(240, 90, 65, 80)
        self.hit_frames_l.append(image)
        image = sprite_sheet.get_image(360, 90, 45, 85)
        image = pygame.transform.flip(image, True, False)
        self.hit_frames_l.append(image)

        image = sprite_sheet.get_image(240, 90, 65, 80)
        image = pygame.transform.flip(image, True, False)
        self.hit_frames_r.append(image)
        image = sprite_sheet.get_image(360, 90, 45, 85)
        self.hit_frames_r.append(image)

        self.image = self.walking_frames_l[0]

        self.rect = self.image.get_rect()

        self.attacking = False
        self.crouching = False
        self.twoHit = False
        self.time = 0

        self.health = 100

        self.direction = "R"

    def update(self):
        self.gravity()

        self.rect.x += self.change_x
        pos = self.rect.x

        if self.rect.y < 470:
            if self.direction == "R":
                self.image = self.jumping_frames_r[0]
            else:
                self.image = self.jumping_frames_l[0]
            if self.crouching == True:
                if self.rect.y < 460:
                    self.rect.y += 10
        else:
            if self.direction == "R":
                frame = (pos // 25) % len(self.walking_frames_r)
                self.image = self.walking_frames_r[frame]
            else:
                frame = (pos // 25) % len(self.walking_frames_l)
                self.image = self.walking_frames_l[frame]
            if self.move == False:
                if self.direction == "R":
                    self.image = self.walking_frames_r[0]
                else:
                    self.image = self.walking_frames_l[0]
        if self.attacking == True:
            if self.direction == "R":
                self.image = self.attacking_frames_r[0]
            else:
                global twoLeftAttack
                if twoLeftAttack == 0 and self.crouching == False:
                    self.rect.x -= 30
                    twoLeftAttack += 1
                self.image = self.attacking_frames_l[0]
        if self.crouching == True:
            if self.direction == "R":
                self.image = self.crouching_frames_r[0]
            else:
                self.image = self.crouching_frames_l[0]
        if self.twoHit == True:
            if self.rect.y < 470:
                if self.direction == "R":
                    self.image = self.hit_frames_r[0]
                    self.change_x -= 0.75
                else:
                    self.image = self.hit_frames_l[0]
                    self.change_x += 0.75
            if self.move == False and self.rect.y > 460:
                self.change_x = 0
                global twoDamage
                twoDamage = 0
                if self.direction == "R":
                    self.image = self.hit_frames_r[1]
                else:
                    self.image = self.hit_frames_l[1]
                if gameTime > self.time:
                    self.twoHit = False
        if self.health <= 0:
            global oneWin
            oneWin = True
            global playerTwoHealth
            playerTwoHealth = 0

        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                self.rect.left = block.rect.right

        self.rect.y += self.change_y

        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
            self.change_y = 0

    def jump(self):
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2
        if len(platform_hit_list) > 0 or self.rect.bottom >= winHeight:
            self.change_y = -8

    def gravity(self):
        if self.change_y == 0:
            self.change_y = 2
        else:
            self.change_y += .65
        if self.rect.y >= winWidth - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = winHeight - self.rect.height

    def go_left(self):
        if self.crouching == True:
            pass
        else:
            self.move = True
            self.change_x = -6
            self.direction = "L"

    def go_right(self):
        if self.crouching == True:
            pass
        else:
            self.move = True
            self.change_x = 6
            self.direction = "R"

    def stop(self):
        self.move = False
        self.change_x = 0

    def attack(self):
        global twoPreviousAttack
        twoPreviousAttack = pygame.time.get_ticks() + 500
        global twoLeftAttack
        twoLeftAttack = 0
        self.attacking = True

    def stop_attack(self):
        self.attacking = False
        global twoLeftAttack
        if twoLeftAttack == 1:
            self.rect.x += 30
            twoLeftAttack = 0

    def crouch(self):
        global twoCrouching
        self.crouching = True
        twoCrouching = True

    def uncrouch(self):
        self.crouching = False
        global twoCrouching
        twoCrouching = False

    def hit(self):
        global twoPreviousHit
        global playerTwoHealth
        global twoDamage
        global twoX
        global twoY
        twoPreviousHit = pygame.time.get_ticks() + 500
        twoDamage = random.randint(3, 5)
        critical = random.randint(1,8)
        if critical == 8:
            twoDamage *= 2
        self.health -= twoDamage
        playerTwoHealth = self.health
        self.twoHit = True
        twoX = self.rect.x
        twoY = self.rect.y
        self.rect.y -= 50
        self.time = pygame.time.get_ticks() + 500
        if self.direction == "R":
            self.rect.x -= 20
        else:
            self.rect.x += 20

class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        # Sets up platform image variable

        self.rect = self.image.get_rect()
        # Sets up a rectangle (for positioning) for platform image

class Level(object):
    def __init__(self, player):
        self.platform_list = pygame.sprite.Group()
        # Creates a sprite group for platforms

        self.player = player
        # Identifies player variable

        self.background = None

    def update(self):
        self.platform_list.update()
        # Refreshes platform list

    def draw(self, screen):
        self.platform_list.draw(screen)
        screen.blit(background, [0,0])
        # Uses random background out of three
        pygame.draw.rect(screen, grey, [295, 575, 200, 50])
        button(295, 575, 200, 50, green, action="back")
        centerText("BACK", red, 280, "twoMedium")
        # Back button

        pygame.draw.rect(screen, black, [330, 20, 140, 30])
        button(330, 20, 140, 30, green, action="pause")
        centerText("PAUSE", white, -280, "oneSmall")
        # Pause button

        pygame.draw.rect(screen, black, [20, 20, 300, 30])
        pygame.draw.rect(screen, red, [20, 20, playerOneHealth*3 , 30])
        text("P1", white, -285, -350, "twoSmall")
        # Player Two Health Bar

        pygame.draw.rect(screen, black, [480, 20, 300, 30])
        pygame.draw.rect(screen, red, [480, 20, playerTwoHealth * 3, 30])
        text("P2", white, -285, 350, "twoSmall")
        # Player One Health Bar

        global twoDamage
        if twoDamage > 0 and twoDamage < 6:
            twoDamage = str(twoDamage)
            damageText(twoDamage, red, twoX, twoY, "oneSmall")
            twoDamage = int(twoDamage)
        elif twoDamage > 5:
            damageText('CRITICAL', red, twoX, twoY, "oneSmall")
        # Displays damage inflicted for Player One's attacks

        global oneDamage
        if oneDamage > 0 and oneDamage < 6:
            oneDamage = str(oneDamage)
            damageText(oneDamage, red, oneX, oneY, "oneSmall")
            oneDamage = int(oneDamage)
        elif oneDamage > 5:
            damageText('CRITICAL', red, twoX, twoY, "oneSmall")
        # Displays damage inflicted for Player Two's attacks

        if oneWin == True:
            oneVictory()
        # Goes to Player One victory screen

        if twoWin == True:
            twoVictory()
        # Goes to Player Two victory screen

class Map(Level):
    def __init__(self, player):
        Level.__init__(self, player)
        level = [[900, 700, 0, 550]]

        # Sets up the platform position and size

        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

        # This loop is used to implement each platform into a list which will be used later

def gameplay():
    global musicOn
    musicOn = True

    pygame.mixer.music.load("music\game.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

    pause = False

    hit = pygame.mixer.Sound('sounds\hit.wav')
    # Sound files used within the game

    clock = pygame.time.Clock()
    # Sets up game clock

    screen = pygame.display.set_mode([winWidth, winHeight])
    # Creates screen

    playerOne = PlayerOne()
    playerTwo = PlayerTwo()
    # Refers these two variables to repective player classes

    global playerOneHealth
    global playerTwoHealth
    playerOneHealth = 100
    playerTwoHealth = 100

    global oneWin
    global twoWin
    oneWin = False
    twoWin= False

    global oneDamage
    oneDamage = 0
    global twoDamage
    twoDamage = 0

    # These variables are redefined each time this function is called (If game is played again in same session)

    # Associates theese variables with respective player classes

    current_level = (Map(playerOne))
    # Loads the Level (Map)

    active_sprite_list = pygame.sprite.Group()
    playerOne.level = current_level
    playerTwo.level = current_level

    playerTwo.rect.x = 50
    playerOne.rect.x = 700
    # Starting position

    playerTwo.rect.y = winHeight - playerTwo.rect.height
    playerOne.rect.y = winHeight - playerOne.rect.height
    # Defines height of character rectangle

    active_sprite_list.add(playerOne)
    active_sprite_list.add(playerTwo)

    done = False
    while not done:
        global gameTime
        gameTime = pygame.time.get_ticks()
        col = pygame.sprite.collide_rect(playerOne, playerTwo)
        # Detects sprite collision
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerOne.go_left()
                if event.key == pygame.K_RIGHT:
                    playerOne.go_right()
                if event.key == pygame.K_UP:
                    playerOne.jump()
                if event.key == pygame.K_DOWN:
                    global oneCrouchTime
                    # This timer is used so player cannot block repeatedly.
                    oneCrouchTime = pygame.time.get_ticks() + 1000
                    playerOne.crouch()
                if event.key == pygame.K_m:
                    global oneAttackTime
                    oneAttackTime = pygame.time.get_ticks() + 150
                    if onePreviousAttack <= gameTime:
                        playerOne.attack()
                if event.key == pygame.K_m and col == True and twoCrouching == False and oneCrouching == False:
                    global twoPreviousHit
                    # This timer is used so player cannot attack repeatedly.
                    if twoPreviousHit <= gameTime:
                        hit.play(loops=0)
                        playerTwo.hit()
                    # If player one attacks and their sprites are touching and both players are not crouching/blocking, player two gets hit.
                # Player One movement/Interactions
                if event.key == pygame.K_a:
                    playerTwo.go_left()
                if event.key == pygame.K_d:
                    playerTwo.go_right()
                if event.key == pygame.K_w:
                    playerTwo.jump()
                if event.key == pygame.K_s:
                    global twoCrouchTime
                    # This timer is used so player cannot block repeatedly.
                    twoCrouchTime = pygame.time.get_ticks() + 1000
                    # Sets a timer so you can only crouch/block for 1.5 seconds for Player Two.
                    playerTwo.crouch()
                if event.key == pygame.K_c:
                    global twoAttackTime
                    twoAttackTime = pygame.time.get_ticks() + 150
                    if twoPreviousAttack <= gameTime:
                        playerTwo.attack()
                if event.key == pygame.K_c and col == True and oneCrouching == False and twoCrouching == False:
                    global onePreviousHit
                    if onePreviousHit <= gameTime:
                        hit.play(loops=0)
                        playerOne.hit()
                    # If player two attacks and their sprites are touching and both players are not crouching/blocking, player one gets hit.
                # Player Two movement/Interactions

                if event.key == pygame.K_p:
                    pygame.mixer.music.pause()
                    pauseScreen()
                if event.key == pygame.K_t:
                    pygame.mixer.music.pause()
                    pauseScreen()
                # Pause game function

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and playerOne.change_x < 0:
                    playerOne.stop()
                if event.key == pygame.K_RIGHT and playerOne.change_x > 0:
                    playerOne.stop()
                if event.key == pygame.K_DOWN:
                    playerOne.uncrouch()
                if event.key == pygame.K_a and playerTwo.change_x < 0:
                    playerTwo.stop()
                if event.key == pygame.K_d and playerTwo.change_x > 0:
                    playerTwo.stop()
                if event.key == pygame.K_m:
                    playerOne.stop_attack()
                if event.key == pygame.K_c:
                    playerTwo.stop_attack()
                if event.key == pygame.K_s:
                    playerTwo.uncrouch()
            # Player key-up interactions (Ends attack, crouch, and walking animations)

        if gameTime < oneCrouchTime:
            pass
        else:
            playerOne.uncrouch()

        if gameTime < twoCrouchTime:
            pass
        else:
            playerTwo.uncrouch()
        # Player can only crouch for certain amount of time (If it exceeds that time they uncrouch)

        if gameTime < oneAttackTime:
            pass
        else:
            playerOne.stop_attack()

        if gameTime < twoAttackTime:
            pass
        else:
            playerTwo.stop_attack()
        # Attack animation is only a certain time long

        active_sprite_list.update()
        current_level.update()
        # Updates current sprites and platforms

        if playerOne.rect.right > winWidth:
            playerOne.rect.right = winWidth
        if playerOne.rect.left < 0:
            playerOne.rect.left = 0

        if playerTwo.rect.right > winWidth:
            playerTwo.rect.right = winWidth
        if playerTwo.rect.left < 0:
            playerTwo.rect.left = 0
        # If player is touching the edges of the window, they do not move.

        current_level.draw(screen)
        active_sprite_list.draw(screen)
        pygame.display.update()
        clock.tick(30)

def oneVictory():
    playerOneVictory = pygame.mixer.Sound('oneWin.wav')
    playerOneVictory.play(loops=0)

    # Player One Victory Voice Line

    pygame.mixer.music.load("victory.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
    clock = pygame.time.Clock()

    # Victory music

    end = False
    while not end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.blit(oneVictorys, [280, 460])
        screen.blit(twoDefeat, [440, 470])

        # Displays sprites in victory/defeat positions

        centerText("PLAYER ONE", red, -80, "twoLarge")
        centerText("VICTORY", turq, 0, "oneLarge")

        # Victory text

        pygame.draw.rect(screen, grey, [282, 575, 232, 50])
        button(282, 575, 232, 50, green, action="play")
        centerText("Restart", red, 280, "twoMedium")

        # Allows user to play again

        pygame.draw.rect(screen, black, [273, 375, 253, 50])
        button(273, 375, 253, 50, green, action="back")
        centerText("Main Menu", red, 80, "twoSmall")

        # Allows user to return to main menu

        pygame.display.update()
        clock.tick(30)

def twoVictory():
    # Same as oneVictory, refer to oneVictory() function

    playerTwoVictory = pygame.mixer.Sound('twoWin.wav')
    playerTwoVictory.play(loops=0)

    pygame.mixer.music.load("victory.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
    clock = pygame.time.Clock()

    end = False
    while not end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.blit(twoVictorys, [280, 470])
        screen.blit(oneDefeat, [440, 470])

        centerText("PLAYER TWO", red, -80, "twoLarge")
        centerText("VICTORY", turq, 0, "oneLarge")

        pygame.draw.rect(screen, grey, [282, 575, 232, 50])
        button(282, 575, 232, 50, green, action="play")
        centerText("Restart", red, 280, "twoMedium")

        pygame.draw.rect(screen, black, [273, 375, 253, 50])
        button(273, 375, 253, 50, green, action="back")
        centerText("Main Menu", red, 80, "twoSmall")

        pygame.display.update()
        clock.tick(30)

# Instructions page
def instructions():
    clock = pygame.time.Clock()

    bgScreen = pygame.display.set_mode((800, 512), pygame.DOUBLEBUF)
    bg = parallax.ParallaxSurface((800, 512), pygame.RLEACCEL)
    bg.add("bg\instructions.jpg", 5)
    bgSpeed = 10
    t_ref = 0
    orientation = "horizontal"
    # sets up scrolling background from parallax module
    back = pygame.image.load('back.png')
    back = pygame.transform.scale(back, (50,50))
    instruction = pygame.image.load('bg\instructions.png')
    # Loads all images

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        bg.scroll(bgSpeed, orientation)
        t = pygame.time.get_ticks()
        if (t - t_ref) > 60:
            bg.draw(bgScreen)
            centerText("Instructions", white, -260, "oneLarge")
            # title
            pygame.draw.rect(screen, turq, [50, 350, 250, 50])
            button(50, 350, 250, 50, green, action="back")
            text("BACK", red, 55, -180, "twoMedium")
            screen.blit(back, (70,350))
            # back button
            rect = pygame.Surface((250, 200))
            rect.set_alpha(200)
            rect.fill((100, 100, 100))
            screen.blit(rect,[50,110])
            # Creates translucent rectangle for text to be displayed in
            screen.blit(fontTwoTiny.render('RULES:', True, (255, 0, 0)), (55, 115))
            screen.blit(fontTwoTiny.render('The objective of', True, (255, 0, 0)), (55, 135))
            screen.blit(fontTwoTiny.render('this game is to', True, (255, 0, 0)), (55, 155))
            screen.blit(fontTwoTiny.render('defeat your foe', True, (255, 0, 0)), (55, 175))
            screen.blit(fontTwoTiny.render('in a 1v1 duel. Use', True, (255, 0, 0)), (55, 195))
            screen.blit(fontTwoTiny.render('the Controls on', True, (255, 0, 0)), (55, 215))
            screen.blit(fontTwoTiny.render('the right to move', True, (255, 0, 0)), (55, 235))
            screen.blit(fontTwoTiny.render('and attack with', True, (255, 0, 0)), (55, 255))
            screen.blit(fontTwoTiny.render('your character.', True, (255, 0, 0)), (55, 275))
            # Displays all the text of isntructions page
            rect2 = pygame.Surface((440, 300))
            rect2.set_alpha(200)
            rect2.fill((100, 100, 100))
            screen.blit(rect2, [325, 110])
            # Creates another translucent rectangle for controls to be displayed in
            screen.blit(instruction, [0,0])
            # Displays image of the controls which is a graphic I made

        pygame.display.update()

        clock.tick(30)

# Beginning main menu of the game.
def introLoop():
    if musicOn == True:
        pygame.mixer.music.load("music\menu.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

    pygame.mixer.music.unpause()
    clock = pygame.time.Clock()

    bgScreen = pygame.display.set_mode((800, 640), pygame.DOUBLEBUF)
    bg = parallax.ParallaxSurface((800, 640), pygame.RLEACCEL)
    bg.add("bg\gameTitle.png", 5)
    bgSpeed = 30
    t_ref = 0
    orientation = "vertical"

    end = False

    while not end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        bg.scroll(bgSpeed, orientation)
        t = pygame.time.get_ticks()
        if (t - t_ref) > 60:
            bg.draw(bgScreen)
            centerText("Welcome to:", red, -285, "twoMedium")
            centerText("BATTLE", turq, -200, "oneLarge")
            centerText("ROYALE", green, -100, "oneLarge")
            pygame.draw.rect(screen, red, [300, 300, 200, 50])
            button(300, 300, 200, 50, green, action="play")
            pygame.draw.rect(screen, red, [238, 400, 325, 50])
            button(238, 400, 325, 50, green, action="instructions")
            pygame.draw.rect(screen, red, [300, 500, 200, 50])
            button(300, 500, 200, 50, green, action="quit")
            centerText("PLAY", white, 5, "twoMedium")
            centerText("Instructions", white, 105, "twoSmall")
            centerText("Quit", white, 205, "twoMedium")

        pygame.display.update()

        clock.tick(30)

# When pause button or key is pressed, game goes into this loop
def pauseScreen():
    clock = pygame.time.Clock()
    end = False
    while not end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                pygame.mixer.music.unpause()
                end = True
            # When any key is pressed, this pause loop is exited

        centerText("Press Any Key to Unpause", blue, 5, "oneSmall")
        pygame.display.update()
        clock.tick(30)
    # Puts program in an neverending loop unless a key is pressed to unpause the game.

def centerText(msg, color, yDisplace=0, size="small"):
    textSurf, textRect = textObjects(msg, color, size)
    textRect.center = (winWidth/2), (winHeight/2 + yDisplace)
    screen.blit(textSurf, textRect)

def text(msg, color, yDisplace = 0, xDisplace = 0, size="small"):
    textSurf, textRect = textObjects(msg, color, size)
    textRect.center = (winWidth/2 + xDisplace), (winHeight/2 + yDisplace)
    screen.blit(textSurf, textRect)

def damageText(msg, color, x = 0, y = 0, size="small"):
    textSurf, textRect = textObjects(msg, color, size)
    textRect.center =  x, y
    screen.blit(textSurf, textRect)

# centerText, damageText, and text are all the same except have different capabilities in positioning. They all create variables for the message, colour of text, and x/y positions
# One is centered on the y axis, and the others can have text anywhere, but the x and y variables are referring to different locations which are implemented for practicality

# Button function used for all clickable entities
def button(x, y, width, height, fill, action = None):
    global background
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + width > cur[0] > x and y + height > cur[1] > y:
        global musicOn
        pygame.draw.rect(screen, fill, (x, y, width, height))
        # The following defines what a button does when associated with these keywords
        if click[0] == 1 and action != None:
            if action == "quit":
                pygame.quit()
                quit()
            # Leaves game
            elif action == "play":
                backgrounds = [bgOne, bgTwo, bgThree]
                num = random.randint(0, 2)
                background = backgrounds[num]
                # Puts three backgrounds (defined earlier) into a list and chooses one
                pygame.mixer.music.pause()
                musicOn = False
                gameplay()
            # Starts gameplay function
            elif action == "instructions":
                musicOn = False
                instructions()
            # Goes to instructions screen
            elif action == "back":
                introLoop()
            # Returns to main menu
            elif action == "pause":
                pygame.mixer.music.pause()
                pauseScreen()
            # Goes to pause screen function

# Defines what centerText, damageText, and text do.
def textObjects(text, color, size):
    if size == "oneSmall":
        textSurface = fontOneSmall.render(text, True, color)
    elif size == "oneMedium":
        textSurface = fontOneMedium.render(text, True, color)
    elif size == "oneLarge":
        textSurface = fontOneLarge.render(text, True, color)
    elif size == "twoSmall":
        textSurface = fontTwoSmall.render(text, True, color)
    elif size == "twoMedium":
        textSurface = fontTwoMedium.render(text, True, color)
    elif size == "twoLarge":
        textSurface = fontTwoLarge.render(text, True, color)
    # This associates these keywords with the correlating font (defined previously) and their font sizes
    return textSurface, textSurface.get_rect()
    # Returns the selected font

introLoop()
# Starts game at introLoop after reading all functions

pygame.mixer.quit()
pygame.quit()
quit()