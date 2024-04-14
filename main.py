import pygame, sys, time, random

#Set classes for objects
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, size, groups, kup, kdown):
        super().__init__(groups)
        self.image = pygame.Surface(size)
        self.image.fill('white')
        self.rect = self.image.get_rect(topleft = pos)
        self.old_rect = self.rect.copy()

        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = 0
        self.speed = 200
        self.kup = kup
        self.kdown = kdown

    def input(self):
        keys = pygame.key.get_pressed()

        #movement input
        if keys[self.kup]:
            self.direction = -1
        elif keys[self.kdown]:
            self.direction = 1
        else:
            self.direction = 0
    
    def window_collision(self):
        
        # collision on bottom
        if self.rect.bottom > wsize[1]:
            self.rect.bottom = wsize[1]
            self.pos.y = self.rect.y

        # collision on the top
        if self.rect.top < 0:
            self.rect.top = 0
            self.pos.y = self.rect.y
    
    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.input()

        self.pos.y += self.direction * self.speed * dt
        self.rect.y = round(self.pos.y)
        self.window_collision()

class Projectile(pygame.sprite.Sprite):
    def __init__(self, groups, obstacles):
        super().__init__(groups)
        self.image = pygame.Surface((40, 40))
        self.image.fill('green')
        self.rect = self.image.get_rect(center = (wsize[0]/2, wsize[1]/2))
        self.old_rect = self.rect.copy()

        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(random.choice([-1, 1]), random.choice([-1, 1]))
        self.speed = 400
        self.obstacles = obstacles

    def collision(self, direction):
        collision_sprites = pygame.sprite.spritecollide(self, self.obstacles, False)
        if collision_sprites:
            if direction == 'horizontal':
                for sprite in collision_sprites:
                    # collision on the right
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                        self.pos.x = self.rect.x
                        self.direction.x *= -1
                        self.speed += 15
                    
                    # collision on the left
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right
                        self.pos.x = self.rect.x
                        self.direction.x *= -1
                        self.speed += 15

            if direction == 'vertical':
                for sprite in collision_sprites:
                    # collision on the bottom
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                        self.pos.y = self.rect.y
                        self.direction.y *= -1
                    
                    # collision on the top
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                        self.pos.y = self.rect.y
                        self.direction.y *= -1
        
    def window_collision(self):
        if self.rect.bottom > wsize[1]:
            self.rect.bottom = wsize[1]
            self.pos.y = self.rect.y
            self.direction.y *= -1

        # collision on the top
        if self.rect.top < 0:
            self.rect.top = 0
            self.pos.y = self.rect.y
            self.direction.y *= -1
    
    def game_over_check(self):
        #Goal for the left
        if self.rect.right > wsize[0]:
            game_over('Left')

        #Goal for the right
        if self.rect.left < 0:
            game_over('Right')

    def update(self, dt):
        self.old_rect = self.rect.copy()

        #Normalize diagonal speed to match axis'
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.x = round(self.pos.x)
        self.collision('horizontal')
        self.window_collision()
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.y = round(self.pos.y)
        self.collision('vertical')
        self.window_collision()
        self.game_over_check()

def game_over(side):
    #Create font object
    font = pygame.font.SysFont('times new roman', 50)
    game_over_surface = (pygame.Surface)

    #Create a text surface on which text will be drawn
    if side == 'Left':
        game_over_surface = font.render('Left Wins!', True, 'white')
    elif side == 'Right':
        game_over_surface = font.render('Right Wins!', True, 'white')
    
    #Create a rectangular object for the text surface object
    game_over_rect = game_over_surface.get_rect()

    #Setting position of the text
    game_over_rect.midtop = (wsize[0]/2, wsize[1]/4)

    #Blit will draw the text on screen
    screen.blit(game_over_surface, game_over_rect)
    pygame.display.flip()

    #After five seconds we will quit the program
    time.sleep(5)
    pygame.quit()
    sys.exit()


#General setup
pygame.init()
wsize = (720, 480)
screen = pygame.display.set_mode(wsize)
pygame.mouse.set_visible(False)

all_sprites = pygame.sprite.Group()

#Sprite setup
Player((10, 170), (20, 150), all_sprites, pygame.K_w, pygame.K_s)
Player((wsize[0] - 30, 170), (20, 150), all_sprites, pygame.K_UP, pygame.K_DOWN)
Projectile(all_sprites, all_sprites)

last_time = time.time()
while True:
    
    #Delta time
    dt = time.time() - last_time
    last_time = time.time()

    #Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
    
    #Drawing and updating the screen
    screen.fill('black')
    all_sprites.update(dt)
    all_sprites.draw(screen)

    #Display output
    pygame.display.update()