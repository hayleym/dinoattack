    
import pygame, random
pygame.init()

screen = pygame.display.set_mode((640, 500))

class Dino(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("walk/dinoWalk1.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        
        if not pygame.mixer:
            print("Sound Error")
        else:
            pygame.mixer.init()
            self.sndpickupHuman = pygame.mixer.Sound("pickupHuman.ogg")
            self.sndbomb = pygame.mixer.Sound("bomb.ogg")
            self.sndbgTrack = pygame.mixer.Sound("03_Chibi_Ninja.ogg")
            self.sndbgTrack.play(-1)
        
    def update(self):
        mousex, mousey = pygame.mouse.get_pos()
        self.rect.center = (mousex, 430)
                
class Man(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("falling.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.reset()
        
        self.dy = 5
    
    def update(self):
        self.rect.centery += self.dy
        if self.rect.top > screen.get_height():
            self.reset()
            
    def reset(self):
        self.rect.top = 0
        self.rect.centerx = random.randrange(0, screen.get_width())
      
class Bomb(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("bomb.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.reset()

    def update(self):
        self.rect.centerx += self.dx
        self.rect.centery += self.dy
        if self.rect.top > screen.get_height():
            self.reset()
    
    def reset(self):
        self.rect.bottom = 0
        self.rect.centerx = random.randrange(0, screen.get_width())
        self.dy = random.randrange(0, 5)
        self.dx = random.randrange(-2, 2)
    
class City(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("City_street.gif")
        self.rect = self.image.get_rect()
        self.dx = 5
        self.reset()
        
    def update(self):
        self.rect.centerx -= self.dx
        if self.rect.right <= 640:
            self.reset() 
    
    def reset(self):
        self.rect.left = 0

class Scoreboard(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.lives = 10
        self.score = 0
        self.font = pygame.font.SysFont("sans-serif", 20)
        
    def update(self):
        self.text = "Lives: %d    Score: %d" % (self.lives, self.score)
        self.image = self.font.render(self.text, 1, (255, 255, 0))
        self.rect = self.image.get_rect()
    
def game():
    pygame.display.set_caption("DINO ATTACK!!!")

    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    dino = Dino()
    man = Man()
    bomb1 = Bomb()
    bomb2 = Bomb()
    bomb3 = Bomb()
    city = City()
    scoreboard = Scoreboard()

    friendSprites = pygame.sprite.OrderedUpdates(city, man, dino)
    bombSprites = pygame.sprite.Group(bomb1, bomb2, bomb3)
    scoreSprite = pygame.sprite.Group(scoreboard)

    clock = pygame.time.Clock()
    keepGoing = True
    while keepGoing:
        clock.tick(30)
        pygame.mouse.set_visible(False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False

        
        if dino.rect.colliderect(man.rect):
            dino.sndpickupHuman.play()
            man.reset()
            scoreboard.score += 1

        hitBombs = pygame.sprite.spritecollide(dino, bombSprites, False)
        if hitBombs:
            dino.sndbomb.play()
            scoreboard.lives -= 1
            if scoreboard.lives <= 0:
                keepGoing = False
            for theBomb in hitBombs:
                theBomb.reset()
        
        friendSprites.update()
        bombSprites.update()
        scoreSprite.update()
        
        friendSprites.draw(screen)
        bombSprites.draw(screen)
        scoreSprite.draw(screen)
        
        pygame.display.flip()
    
    dino.sndbgTrack.stop()
    #return mouse cursor
    pygame.mouse.set_visible(True) 
    return scoreboard.score
    
def instructions(score):
    pygame.display.set_caption("DINO ATTACK!!!")

    dino = Dino()
    city = City()
    
    allSprites = pygame.sprite.Group(city, dino)
    insFont = pygame.font.SysFont(None, 25)
    insLabels = []
    instructions = (
    " ",
    "Dino Attack",     
    " ",
    "Last score: %d" % score ,
    " ",
    "You're in a robot dino terrorizing",
    "the city",
    " ",
    "Avoid the bombs and eat",
    "the people!.",
    " ",
    "Click to Start, ESC to quit."
    )
    
    for line in instructions:
        tempLabel = insFont.render(line, 1, (255, 255, 255))
        insLabels.append(tempLabel)
 
    keepGoing = True
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)
    while keepGoing:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                donePlaying = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                keepGoing = False
                donePlaying = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    keepGoing = False
                    donePlaying = True
    
        allSprites.update()
        allSprites.draw(screen)

        for i in range(len(insLabels)):
            screen.blit(insLabels[i], (50, 30*i))

        pygame.display.flip()
        
    dino.sndbgTrack.stop()    
    pygame.mouse.set_visible(True)
    return donePlaying
        
def main():
    donePlaying = False
    score = 0
    while not donePlaying:
        donePlaying = instructions(score)
        if not donePlaying:
            score = game()


if __name__ == "__main__":
    main()
    
    
