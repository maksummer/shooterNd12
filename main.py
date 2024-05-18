import pygame
from random import randint
WIDTH = 1200
HEIGHT = 700

SIZE = (WIDTH,HEIGHT)

FPS = 60

monster_num = 5
score= 0
lost = 0

pygame.display.set_caption("Гра шутер автор Максим Федоришин")
window = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
background = pygame.transform.scale(pygame.image.load("galaxy.jpg"), SIZE)

pygame.mixer.init()
pygame.mixer.music.load("space.ogg")
pygame.mixer.music.play()

fire_sfx = pygame.mixer.Sound("fire.ogg")

pygame.font.init()

big_font  =  pygame.font.Font(None, 70)
medium_font =pygame.font.Font(None, 35)
small_font = pygame.font.Font(None, 15)

class GameSprite(pygame.sprite.Sprite):
    def __init__(self,image,coords:tuple[int,int],speed, size: tuple[int,int]): 
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load(image),
            size
        )
        self.rect = self.image.get_rect()
        self.rect.center = coords
        self.speed = speed

    def reset(self):
        window.blit(self.image,self.rect.topleft)

class Player(GameSprite):
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            if self.rect.x < WIDTH:
                self.rect.x += self.speed
            else:
                self.rect.x = 0
        if keys[pygame.K_a]:
            if self.rect.x > 0:
                self.rect.x -= self.speed
            else:
                self.rect.x = WIDTH
        

    def fire(self):
        new_bullet = Bullet("bullet.png",
                            (self.rect.centerx, self.rect.top),
                            5,
                            (10,15)
                            )
        bullets.add(new_bullet)
        fire_sfx.play()


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= HEIGHT:
            self.rect.y = 0
            self.rect.x = randint(20,WIDTH-20)
            global lost
            lost += 1


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()




player = Player("rocket.png",(WIDTH/2,HEIGHT-50), 8, (75,100))

bullets = pygame.sprite.Group()
monsters = pygame.sprite.Group()

for i in range(monster_num):
    new_monster = Enemy("ufo.png",(randint(20,WIDTH-20), 0), randint(2,8), (75,50) )

    monsters.add(new_monster)

game = True
finish = False
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            
                if event.button == 1:
                    player.fire()
            

    if not finish:
        window.blit(background, (0,0))
        player.update()
        player.reset()

        monsters.update()
        monsters.draw(window)

        bullets.update()
        bullets.draw(window)

        text_lost = medium_font.render(
            "Пропущенно " + str(lost),
            True,
            (255,255,255)
        )
        text_score = medium_font.render(
            "Рахунок " + str(score),
            True,
            (255,255,255)
        )

        window.blit(text_score,(0,0))
        window.blit(text_lost,(0,40))



    pygame.display.update()
    clock.tick(FPS)
