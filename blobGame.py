"""
blobGame.py
Izabele Bauzyte
4/28/2019

This game has a player move around the screen
to capture food particles, and once they have
captured all food, they reach final form and
have to capture the enemies
"""

"""
Attributions:
    
All art by Izabele Bauzyte

Babylon.ogg [Modified]
    "Babylon" Kevin MacLeod (incompetech.com)
    Licensed under Creative Commons: By Attribution 3.0 License
    http://creativecommons.org/licenses/by/3.0/
Ringing_Ambient_Background.ogg [Modified]
    Youtube Audio Library
Soft_Blossom.ogg [Modified]
    Youtube Audio Library
    Ann Annie
Splat.ogg [Modified]
    soundbible.com/1728-Spit-Splat-2.html
    Mike Koenig
    02/09/11
"""


#import and initialize
import pygame, random, time
pygame.init()

screen = pygame.display.set_mode((600, 600))

class Player(pygame.sprite.Sprite):
    """
    The central blob character
    stays in the middle of the screen
    """

    def __init__(self):

        pygame.sprite.Sprite.__init__(self)
        #img and rect
        self.scale = 30
        self.imgSrc = "player.png"
        self.image = pygame.transform.scale(pygame.image.load(self.imgSrc).convert_alpha(), (self.scale, self.scale))
        self.rect = self.image.get_rect()
        self.rect.centerx = screen.get_width() / 2
        self.rect.centery = screen.get_height() / 2
        
        # for animation of rotation
        self.degrees = 0
        
        self.finalForm = False
        
    def rotate(self):
        """
        Animates image
        """
        
        if (self.degrees + 1 > 360):
            
            self.degrees = 0
            
        else:
            
            self.degrees += 1
        
        self.image = pygame.transform.rotate(
                        pygame.transform.scale(
                                pygame.image.load(self.imgSrc).convert_alpha(), (self.scale, self.scale)), self.degrees)
        
    def update(self):
        
        self.rotate()

    def Feed(self, increase = 2):
        """
        Increases player size
        """

        self.scale += increase
        self.image = pygame.transform.scale(pygame.image.load(self.imgSrc), (self.scale, self.scale))
        self.rect = self.image.get_rect()
        self.rect.centerx = screen.get_width() / 2
        self.rect.centery = screen.get_height() / 2
        
        pygame.mixer.Sound("Splat.ogg").play()

    def FinalForm(self):
        """
        Changes player image
        """
        
        self.imgSrc = "playerOP.png"
        self.image = pygame.transform.scale(pygame.image.load(self.imgSrc).convert_alpha(), (self.scale, self.scale))
        self.finalForm = True
        
        pygame.mixer.Sound("Ringing_Ambient_Background.ogg").play()

class Food(pygame.sprite.Sprite):
    """
    Randomly generated food particles
    """

    def __init__(self, xStart, xEnd, yStart, yEnd):

        pygame.sprite.Sprite.__init__(self)
        
        self.imgSrc = "food.png"
        self.image = pygame.image.load(self.imgSrc).convert_alpha()
        self.image = pygame.transform.rotate(self.image, random.randint(0, 360))
        self.rect = self.image.get_rect()
        
        # area in which food can spawn due to borders
        self.xStart = xStart
        self.xEnd = xEnd
        self.yStart = yStart
        self.yEnd = yEnd
        
        self.rect.centerx = random.randint(self.xStart, self.xEnd)
        self.rect.centery = random.randint(self.yStart, self.yEnd)
        
        # x and y movement on screen
        self.maxMove = 5
        
        # rotation animation
        self.rotationSpeed = random.randint(0, 5)
        self.degrees = 0

    def moveVert(self, speed):
        """
        Moves food when player moves vertically
        """

        self.rect.centery += speed

    def moveHor(self, speed):
        """
        Moves food when player moves hor
        """

        self.rect.centerx += speed
        
    def rotate(self):
        
                
        if (self.degrees + self.rotationSpeed > 360):
            
            self.degrees = 0
            
        else:
            
            self.degrees += self.rotationSpeed
        
        self.image = pygame.transform.rotate(
                                pygame.image.load(self.imgSrc).convert_alpha(), self.degrees)

    def update(self):
        """
        Random movement contained inside moveable area
        TODO : still occasionally spawns/moves outside of playeable area
        
            All food particles spawn inside play area but are able to move outside
            so the problem is in this function.
            Discrepancy between the moveHor/moveVert functions and this one?
        """
        
        self.rotate()

        if (self.rect.centerx - self.maxMove > self.xStart) or (self.rect.centerx + self.maxMove < self.xEnd):

            self.rect.centerx += random.randint(-self.maxMove, self.maxMove)

        if (self.rect.centery - self.maxMove > self.yStart) or (self.rect.centery + self.maxMove < self.yEnd):

                self.rect.centery += random.randint(-self.maxMove, self.maxMove)
            
class Enemy(pygame.sprite.Sprite):
    """
    Enemy class chases player initially then changes to random 
    movement when the player hits final form
    """

    def __init__(self, background, player):

        pygame.sprite.Sprite.__init__(self)
        self.imgSrc = "enemy.png"
        self.image = pygame.image.load(self.imgSrc).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(0, background.get_width())
        self.rect.centery = random.randint(0, background.get_height())
        self.player = player
        
        # rotation animation
        self.degrees = 0
        self.rotationSpeed = random.randint(0, 5)

    def moveVert(self, speed):
        """
        updates vert with player movement
        """

        self.rect.centery += speed

    def moveHor(self, speed):
        """
        updates hor with player movement
        """
        
        self.rect.centerx += speed
        
    def rotate(self):
        
        if (self.degrees + self.rotationSpeed > 360):
            
            self.degrees = 0
            
        else:
            
            self.degrees += self.rotationSpeed
        
        self.image = pygame.transform.rotate(
                                pygame.image.load(self.imgSrc).convert_alpha(), self.degrees)


    def update(self):
        """
        Moves closer to the player every update
        or changes to random motion when they are
        in final form
        """

        self.rotate()

        if self.player.finalForm:

            self.randomMovement()

        else:

            self.chasePlayer()

    def chasePlayer(self):
        """
        Moves closer to the player
        """

        if self.player.rect.centerx > self.rect.centerx:

            self.rect.centerx += 1
        else:
            self.rect.centerx -= 1

        if self.player.rect.centery > self.rect.centery:

            self.rect.centery += 1

        else:
            self.rect.centery -= 1

    def randomMovement(self):

        self.rect.centerx += random.randint(-3, 3)
        self.rect.centery += random.randint(-3, 3)

class Label(pygame.sprite.Sprite):
    """
    Object to display text
    """
    
    def __init__(self, text, loc, alignment, color = (255, 255, 255)):
        """
        string text
        tuple location
        int alignment (-1 = left, 0 = center, 1 = right)
        3 tuple for color default is white
        """

        pygame.sprite.Sprite.__init__(self)

        self.font = pygame.font.SysFont("None", 30)
        self.text = text
        self.color = color
        self.loc = loc
        self.alignment = alignment

    def update(self):
        
        # image
        self.image = self.font.render(self.text, 1, self.color)
        self.rect = self.image.get_rect()

        # left aligned
        if self.alignment == -1:

            self.rect.left = self.loc[0]
            self.rect.centery = self.loc[1]

        # center aligned
        elif self.alignment == 0:

            self.rect.center = self.loc

        # right aligned
        else:

            self.rect.right = self.loc[0]
            self.rect.centery = self.loc[1]

class Border(pygame.sprite.Sprite):
    """
    Constrains player from moving outside of playable area
    and conceals black background from player with appropriate size
    """

    def __init__(self, startX, startY, width, height):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((width, height))
        self.image.fill((160, 160, 160))
        self.rect = self.image.get_rect()

        self.rect.left = startX
        self.rect.top = startY

    def moveVert(self, speed):
        """
        updates with player motion
        """

        self.rect.centery += speed

    def moveHor(self, speed):
        """
        updates with player motion
        """

        self.rect.centerx += speed

def checkKeysMoveViewArea(keys, x, y, movementRate, player, movementGroup, background, borders):
    """
    keys: list of keys pressed during the game
    x, y: x and y to move all objects and background by when player moves
    movementRate: the rate at which objects and bg are moved
    movementGroup: all non-BG objects which need to be shifted
    background:
    borders: list of 4 borders in clockwise format that constrain player and objects

    This function checks whether a key is currently being pressed
    and moves objects on screen accordingly

    returns x, y so they can be constantly updated
    """
    
    if keys[pygame.K_UP]:

        # top border
        if not player.rect.colliderect(borders[0].rect):
        
            y += movementRate
            for sprite in movementGroup:

                sprite.moveVert(movementRate)

    if keys[pygame.K_RIGHT]:

        # right border
        if not player.rect.colliderect(borders[1].rect):

            x -= movementRate
            for sprite in movementGroup:

                sprite.moveHor(-movementRate)

    if keys[pygame.K_DOWN]:

        # bottom border
        if not player.rect.colliderect(borders[2].rect):

            y -= movementRate
            for sprite in movementGroup:

                sprite.moveVert(-movementRate)
            
    if keys[pygame.K_LEFT]:

        # left border
        if not player.rect.colliderect(borders[3].rect):

            x += movementRate
            for sprite in movementGroup:

                sprite.moveHor(movementRate)

    screen.blit(background, (x, y))
    return x, y

def getScore(lives, foodCollected, enemiesKilled, secondsRemain):
    
    lifeMult = 100
    foodMult = 10
    enemyMult = 20
    secondsMult = 30
    
    return (lifeMult * lives) + (foodMult * foodCollected) + (enemyMult * enemiesKilled) + (secondsMult * secondsRemain)
        
def game():
    
    #display

    pygame.display.set_caption("basic blob game")

    #entities

    # game setup
    startSeconds = 20
    seconds = startSeconds
    lives = 3

    # bg
    background = pygame.image.load("background.png").convert_alpha()

    # shadow
    shadowBase = pygame.image.load("shadow.png").convert_alpha()
    shadow = shadowBase.copy()
    shadowAlpha = 255 - (startSeconds * 4) # opacity of on screen shadow
    shadow.fill((255, 255, 255, shadowAlpha), None, pygame.BLEND_RGBA_MULT)
    screen.blit(shadow, (0,0))

    # num food and enemies
    numEnemies = 15
    numFood = 15
    numFoodCollected = 0
    numEnemiesKilled = 0 

# borders
    # setting up game borders
    borderThickness = 20 # thickness of each border
    offset = (screen.get_width() / 2) - 30 # how far from background edge each border is
    """
    Used in this case to hide the edge of the background from the screen
    """

    # the area remaining for game use after offset is set
    playAreaStart = borderThickness + offset
    playAreaEnd = background.get_height() - borderThickness - offset

    borderTop = Border(offset, offset, background.get_height() - (2 * offset), borderThickness)
    borderRight = Border(background.get_width() - offset - borderThickness, offset, borderThickness, background.get_height() - (2 * offset))
    borderBottom = Border(offset, background.get_height() - offset - borderThickness, background.get_width() - (2 * offset), borderThickness)
    borderLeft = Border(offset, offset, borderThickness, background.get_height() - (2 * offset))
    # clockwise array of border sides
    borders = [borderTop, borderRight, borderBottom, borderLeft]

# player
    player = Player()
    playerGroup = pygame.sprite.Group(player)

# enemies
    enemyGroup = pygame.sprite.Group()
    for i in range(numEnemies):
        
        enemyGroup.add(Enemy(background, player))

# food
    foodGroup = pygame.sprite.Group()
    for i in range(numFood):

        foodGroup.add(Food(playAreaStart, playAreaEnd, playAreaStart, playAreaEnd))

# screen labels
    timeLabelLoc = (screen.get_width() / 2, 20)
    collisionLabelLoc = (20 , screen.get_height() - 50)
    livesLabelLoc = (20, screen.get_height() - 20)

    timeLabelText = "%d Seconds Left"

    foodCollisionText = "%d/%d Food Collected"
    enemyCollisionText = "%d/%d Enemies Killed"

    livesLabelText = "Lives Remaining: %d"

    timeLabel = Label("", timeLabelLoc, 0)
    collisionLabel = Label(foodCollisionText % (numFoodCollected, numFood), collisionLabelLoc, -1)
    livesLabel = Label(livesLabelText %(lives), livesLabelLoc, -1)

# groupings
    labelGroup = pygame.sprite.Group()
    labelGroup.add(timeLabel)
    labelGroup.add(collisionLabel)
    labelGroup.add(livesLabel)

    # for collision detection
    entitiesGroup = pygame.sprite.Group()
    entitiesGroup.add(enemyGroup)
    entitiesGroup.add(foodGroup)

    # for movement on/off screen
    movementGroup = pygame.sprite.Group()
    movementGroup.add(enemyGroup)
    movementGroup.add(foodGroup)
    movementGroup.add(borders)

    #assign
    clock = pygame.time.Clock()
    keepGoing = True

    # for keeping track of background location
    x = 0
    y = 0

    # rate at which player moves
    movementRate = 10
    
    start = time.time()
    
    # score info    
    previousScore = 0

    #loop
    while keepGoing:

        #time
        clock.tick(30)

        keys = pygame.key.get_pressed()

        # moves the items around the screen based on player keys
        x, y = checkKeysMoveViewArea(keys, x, y, movementRate, player, movementGroup, background, borders)
                    
        #events
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                
                keepGoing = False
                previousScore = getScore(lives, numFoodCollected, numEnemiesKilled, seconds)

        collisions = pygame.sprite.spritecollide(player, entitiesGroup, True)

        for sprite in collisions:

            # player is still collecting food
            if numFoodCollected < numFood:

                # player has hit an enemy while they are not yet in final mode
                if isinstance(sprite, Enemy):

                    numEnemies -= 1
                    lives -= 1
                    livesLabel.text = livesLabelText % (lives)
                    
                    thing = pygame.Surface((screen.get_width(), screen.get_height()))
                    thing.fill((255, 0, 0))
                    screen.blit(thing, (0,0))

                    if lives == 0:

                        keepGoing = False
                        previousScore = getScore(lives, numFoodCollected, numEnemiesKilled, seconds)

                # player has collected another food sprite
                if isinstance(sprite, Food):

                    player.Feed()

                    # change lighting effect to indicate more energy
                    shadowAlpha -= 10
                    shadow = shadowBase.copy()
                    shadow.fill((255, 255, 255, shadowAlpha), None, pygame.BLEND_RGBA_MULT)

                    numFoodCollected += 1

                    if numFoodCollected == numFood:
                        
                        player.FinalForm()
                        labelGroup.add(Label("Final Form", (20,20), -1, (255, 0, 0)))
                        collisionLabel.text = enemyCollisionText % (numEnemiesKilled, numEnemies)
                        
                    else:
                        
                        collisionLabel.text = foodCollisionText % (numFoodCollected, numFood)

            # player has collected all food
            else:

                # eat enemy and increase in size
                if isinstance(sprite, Enemy):

                    numEnemiesKilled += 1
                    collisionLabel.text = enemyCollisionText % (numEnemiesKilled, numEnemies)

                    player.Feed(5)

                    # player has eaten all enemies
                    if numEnemies == numEnemiesKilled:

                        keepGoing = False
                        previousScore = getScore(lives, numFoodCollected, numEnemiesKilled, seconds)
                    

        elapsedTime = time.time() - start

        # change screen shadow opacity every half second
        if (elapsedTime > 0.5):

            start = time.time()
            
            alphaShift = 2
            shadowAlpha += alphaShift

            # reset to valid color argument
            if shadowAlpha <= 0:

                shadowAlpha = 0

            # player ran out of time
            if shadowAlpha + alphaShift >= 255:

                keepGoing = False
                previousScore = time.time() - start

            # update label
            else:

                seconds = (255 - shadowAlpha) / (alphaShift / 0.5)
                timeLabel.text = timeLabelText % (seconds)

            # update shadow overlay
            shadow = shadowBase.copy()
            shadow.fill((255, 255, 255, shadowAlpha), None, pygame.BLEND_RGBA_MULT)

        # update and move sprites in layers
            # moving group
        movementGroup.update()
        movementGroup.draw(screen)
            # player
        playerGroup.update()
        playerGroup.draw(screen)
            # screen
        screen.blit(shadow, (0,0))
            # labels on top of shadow to be visible
        labelGroup.update()
        labelGroup.draw(screen)

        #refresh
        pygame.display.flip()

    return previousScore

def instructions(previousScore, highScore):
    """
    Tells user how to play
    and shows previous scores
    """

    allSprites = pygame.sprite.Group(Player())

    # some interesting graphics for the intro screen
    for i in range(10):

        food = Food(0, screen.get_width() / 2, 500, screen.get_height() - 30)

        # using a food class and changing image to avoid the following enemy behaviour
        foodWithEnemyPic = Food(screen.get_width() / 2, screen.get_width(), 500, screen.get_height() - 30)
        foodWithEnemyPic.imgSrc = "enemy.png"

        allSprites.add(food)
        allSprites.add(foodWithEnemyPic)

    insFont = pygame.font.SysFont(None, 30)

    # really awful instruction string that tells user how to play
    instructions = ["",
    "Blob Game",
    "Collect the food and grow into your final form",
    "Then eat the enemies pursuing you",
    "Press space to begin", ("Previous Score: %d" % previousScore), ("Session High Score: %d" % highScore), "", "",
                    "                                       You ","","", "", "", "",
                    "        Food                                        Enemy"
        ]

    insLabels = []

    bg = pygame.image.load("background.png").convert_alpha()
                        
    screen.blit(bg, (0,0))

    for line in instructions:
        
        insLabels.append(insFont.render(line, 1, (255, 255, 0)))

    keepGoing = True
    clock = pygame.time.Clock()
    
    while keepGoing:
        
        clock.tick(30)

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                
                # exit game completely
                keepGoing = False
                donePlaying = True
                
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
    
                    # play again
                    keepGoing = False
                    donePlaying = False

        allSprites.clear(screen, bg)
        allSprites.update()
        allSprites.draw(screen)

        for i in range(len(insLabels)):

            screen.blit(insLabels[i], (50, 30 * i))

        pygame.display.flip()

    return donePlaying
    
    
def main():
    
    pygame.mouse.set_visible(False)

    previousScore = 0
    highScore = 0

    donePlaying = False
    
    while not donePlaying:
        
        pygame.mixer.stop()
        pygame.mixer.Sound("Soft_Blossom.ogg").play(-1)
        
        donePlaying = instructions(previousScore, highScore)

        if not donePlaying:
            
            pygame.mixer.stop()
            pygame.mixer.Sound("Babylon.ogg").play(-1)

            print("game")
            previousScore = game()
            if previousScore > highScore:
                
                highScore = previousScore

    pygame.quit()

if __name__ == "__main__":
    main()