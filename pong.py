import pygame
import random
from sys import exit

WIDTH = 800
HEIGHT = 400

game_state = 'play'

left_score = 0
right_score = 0

class Lines(pygame.sprite.Sprite): 
    def __init__(self, x_pos, y_pos) -> None:
        super().__init__()
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.height = 75
        self.width = 6
        self.speed = 6
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill('Red')
        self.rect = self.image.get_rect(center = (x_pos, y_pos))
        
class Circle(pygame.sprite.Sprite):
    def __init__(self, starting_pos):
        super().__init__()
        
        self.image = pygame.image.load('Transparent Green Circle.png').convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0,.1)
        self.rect = self.image.get_rect(center = (starting_pos[0], starting_pos[1]))
        self.starting_pos = starting_pos
        self.x_pos = starting_pos[0]
        self.y_pos = starting_pos[1]
        self.x_direction = 10
        self.y_direction = 4
        
    def circle_movement(self, screen):
        self.rect.x += self.x_direction
        self.rect.y += self.y_direction

def line_input(line, line2, group):
    # Same function for left and right line with differnt key inputs
    group.draw(screen)
    # screen.blit(line2.surf, line2.rect)
    # line2_rect = line2.rect
    keys = pygame.key.get_pressed()        
    if line.x_pos < WIDTH/2:
        if keys[pygame.K_s] and line.rect.bottom <= HEIGHT: line.rect.bottom += line.speed
        if keys[pygame.K_w] and line.rect.top >= 0: line.rect.bottom -= line.speed
    if line2.x_pos > WIDTH/2:
        if keys[pygame.K_DOWN] and line2.rect.bottom <= HEIGHT: line2.rect.bottom += line2.speed
        if keys[pygame.K_UP] and line2.rect.top >= 0: line2.rect.bottom -= line2.speed

def line_ai(line):
        if line.rect.centery < (pong.sprite.rect.centery - 8) and line.rect.bottom <= WIDTH:
            line.rect.y += 5
        elif line.rect.centery > (pong.sprite.rect.centery + 8) and line.rect.top >= 0:
            line.rect.centery -= 5

def collision_sprite():
    # If ball hits ceiling
    if pong.sprite.rect.y <= 0 or pong.sprite.rect.bottom >= HEIGHT:
        pong.sprite.y_direction *=-1
    # if balls hits line
    if pygame.sprite.spritecollide(pong.sprite, line_group, False):
        pong.sprite.x_direction *= -1
        if pong.sprite.y_direction < 0: pong.sprite.y_direction = random.uniform(1,7) * -1
        else: pong.sprite.y_direction = random.uniform(1,7)

def score_point():
    global right_score, left_score, game_state
    # When the ball hits the left side of the window, score point
    if pong.sprite.rect.centerx <= 0: 
        right_score += 1
        pong.sprite.x_direction *= -1
        game_state = 'serve'

    # When the ball hits the right side of the stage 
    elif pong.sprite.rect.centerx >= WIDTH:
        left_score += 1
        pong.sprite.x_direction *= -1
        game_state = 'serve'
    
    # if max score is reached, game over
    if max(left_score, right_score) >= 7:
        print(max(left_score, right_score))
        game_state = 'game over'

def serve():
    global game_state
    display_score()
    # if point was scored on the left side,
    # ball will follow the left line until ball is served
    
    if pong.sprite.rect.x <= WIDTH/2: 
        pong.sprite.rect.center = (40, left_line.rect.centery)
        pong.sprite.y_direction = random.uniform(-7,7)
    else: 
        pong.sprite.rect.center = (WIDTH-40, right_line.rect.centery)
        pong.sprite.y_direction = random.uniform(-7,7)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        game_state = 'play'

def game_over():
    if pong.sprite.rect.centerx <= 0  or pong.sprite.rect.centerx >= WIDTH:
        return False
    else:
        return True  
    
def restart_game():
    global game_state, left_score, right_score
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        game_state = 'play'
        right_score = left_score = 0
        pong.sprite.rect.center = (WIDTH/2, HEIGHT/2) 

def display_score():
    global game_state
    # Displays score on top of the screen
    if game_state == 'play' or game_state == 'serve':
        score_surf = game_font.render(f'{left_score}   SCORE   {right_score}', False, 'White')
        score_rect = score_surf.get_rect(center = (WIDTH/2, 50))
        screen.blit(score_surf, score_rect)
    # Displays winner and instructions when the game is over
    else:
        if left_score == 7:
            winner_surf = game_font.render(f'This games Winner is: Left!', False, 'Black')
            winner_rect = winner_surf.get_rect(center = (WIDTH/2, 50))
        if right_score == 7:
            winner_surf = game_font.render(f'This games Winner is: Right!', False, 'Black')
            winner_rect = winner_surf.get_rect(center = (WIDTH/2, 50))
            
        instructions_surf = game_font.render(f'Press Space Bar to Restart Game', False, 'Black')
        instructions_rect =  instructions_surf.get_rect(center = (WIDTH/2, HEIGHT/2))
        screen.blit(winner_surf, winner_rect)
        screen.blit(instructions_surf, instructions_rect)

def play_update():
    screen.blit(background, (0,0))

    line_input(left_line, right_line, line_group)

    pong.draw(screen)
    pong.sprite.circle_movement(screen=screen)
    collision_sprite()
    display_score()
    score_point()
    line_ai(right_line)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pong V1')
clock = pygame.time.Clock()

# Class Instances
left_line = Lines(12, HEIGHT/2)
right_line = Lines(WIDTH-12, HEIGHT/2)

pong = pygame.sprite.GroupSingle()
pong.add(Circle((300, 300)))

line_group = pygame.sprite.Group()
line_group.add(left_line)
line_group.add(right_line)

# Surfaces

background = pygame.image.load('Background.Jpg')

top_surf = pygame.Surface((0,0))
top_rect = top_surf.get_rect()

game_font = pygame.font.Font('Pixeltype.ttf', 50)



# Game Loop

while True:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    
    if game_state == 'play':
        play_update()
    if game_state == 'serve':
        screen.blit(background, (0,0))
        pong.draw(screen)
        pong.sprite.circle_movement(screen=screen)
        line_input(left_line, right_line, line_group)
        collision_sprite()
        serve()
        line_ai(right_line)
    if game_state == 'game over':
        screen.fill((94,129,162))
        display_score()
        restart_game()
        

    

    #Leave following two lines untouched at the bottom
    pygame.display.update()
    clock.tick(60)
