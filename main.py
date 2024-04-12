import pygame
import time #for close/restart game

window_size = (720, 480)
refrate = 15
black = pygame.Color(0,0,0)
white = pygame.Color(255,255,255)
red = pygame.Color(255,0,0)

""" player1_pos = [ [0, 120], 
            [0, 130],
            [0, 140],
            [0, 100],
            [0, 160] ] """
""" player2_pos = [ [710, 120], 
            [710, 130],
            [710, 140],
            [710, 150],
            [710, 160] ] """
            
player1_pos = [0, 170]
player2_pos = [710, 170]
test_rect_pos = [480, 170]

proj_pos = [window_size[0]/2, window_size[1]/2]
proj_radius = 10

rect_size = (10, 100)

pygame.init()
pygame.display.set_caption("PingPong")
game_window = pygame.display.set_mode(window_size)

fps = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        """ print(event.type) """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                raise SystemExit
        if event.type == pygame.QUIT:
            raise SystemExit
        
    player1_rect = pygame.draw.rect(game_window, white,
                     pygame.Rect(player1_pos[0], player1_pos[1], rect_size[0], rect_size[1]))
    player2_rect = pygame.draw.rect(game_window, white,
                     pygame.Rect(player2_pos[0], player2_pos[1], rect_size[0], rect_size[1]))
    
    #pygame.mouse.get_pos() #get mouse pos
    #playern_rect.collidepoint() #test if a point is inside a rectangle
    #playern_react.colliderect() #test if two rectangles overlap

    test_rect = pygame.draw.rect(game_window, white,
                                 pygame.Rect(test_rect_pos[0], test_rect_pos[1], 40, 120))
    
    projec_rect = pygame.draw.circle(game_window, red, proj_pos, proj_radius)



    
    pygame.display.update()
    fps.tick(refrate)