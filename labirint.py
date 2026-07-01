from pygame import *

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('game labirin')
img_bg = transform.scale(image.load('angkasa.jpg'), (win_width, win_height))


class GameSprite(sprite.Sprite):
    def __init__(self,picture,w,h,x,y): 
        super().__init__()
        self.image=transform.scale(image.load(picture),(w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player(GameSprite):
    def __init__(self,picture,w,h,x,y, x_speed,y_speed): 
        super().__init__(picture,w,h,x,y)
        self.x_speed = x_speed
        self.y_speed = y_speed
    def update(self):
        self.rect.x += self.x_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0: 
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
                print('posisi kanan', self.rect.right)
                print('posisi dinding kiri', p.rect.left)
        elif self.x_speed < 0: 
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)
                print('posisi kiri', self.rect.left)
                print('posisi dinding kanan', p.rect.right)
        self.rect.y += self.y_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0: # turun
            for p in platforms_touched:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
                print('posisi bawah', self.rect.bottom)
                print('posisi dinding atas', p.rect.top)
        elif self.y_speed < 0: # naik ke atas
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom)
                print('posisi atas', self.rect.top)
                print('posisi dinding bawah', p.rect.bottom)

    def fire(self):
        bullet = Bullet('bullet.png', 10, 5, self.rect.right, self.rect.centery, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    direction = "kiri"
    def __init__(self, picture,w,h,x,y, speed):
        super().__init__(picture,w,h,x,y)
        self.speed = speed
    
    def update(self):
        if self.rect.x <= 470:
            self.direction = "kanan"
        if self.rect.x >= win_width - 85:
            self.direction = "kiri"
        if self.direction == "kiri":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Bullet(GameSprite):
    def __init__(self, picture,w,h,x,y, speed):
        super().__init__(picture,w,h,x,y)
        self.speed = speed

    def update(self):
        self.rect.x += self.speed
        # menghilang setelah mencapai tepi layar
        if self.rect.x > win_width+10:
            self.kill()


pacman = Player('hero.png', 70, 70, 50, 400, 0, 0)
wall_1 = GameSprite('platform2_v.png',40,250,200,150)
wall_2 = GameSprite('platform2.png', 250, 40, 230, 300)
wall_3 = GameSprite('platform2_v.png', 40, 250, 350, 100)
final = GameSprite('pac-1.png', 70, 70, 600, 400)
enemy1 = Enemy('cyborg.png', 70, 70, 600, 200, 5)
enemy2 = Enemy('cyborg.png', 70, 70, 600, 100, 5)

barriers = sprite.Group()
barriers.add(wall_1)
barriers.add(wall_2)
barriers.add(wall_3)

bullets = sprite.Group()

enemys = sprite.Group()
enemys.add(enemy1)
enemys.add(enemy2)

win = transform.scale(image.load('thumb.jpg'), (win_width, win_height))
lose = transform.scale(image.load('game-over_1.png'), (win_width, win_height))
finish = False
run = True
while run:
    time.delay(40)
    
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_w:
                pacman.y_speed = -5
            if e.key == K_d:
                pacman.x_speed = 5
            if e.key == K_s:
                pacman.y_speed = 5
            if e.key == K_a:
                pacman.x_speed = -5
            if e.key == K_SPACE:
                pacman.fire()
        elif e.type == KEYUP:
            if e.key == K_w:
                pacman.y_speed = 0
            if e.key == K_d:
                pacman.x_speed = 0
            if e.key == K_s:
                pacman.y_speed = 0
            if e.key == K_a:
                pacman.x_speed = 0
    if finish != True:
        window.blit(img_bg, (0, 0))
        barriers.draw(window)
        pacman.reset()
        final.reset()
        pacman.update()
        enemys.draw(window)
        enemys.update()
        bullets.draw(window)
        bullets.update()
        if sprite.collide_rect(pacman, final):
            finish = True
            window.blit(win, (0, 0))
        
        if sprite.spritecollide(pacman, enemys, False):
            finish = True
            window.blit(lose, (0, 0))

    sprite.groupcollide(bullets, barriers, True, False)
    sprite.groupcollide(bullets, enemys, True, True)

    display.update()