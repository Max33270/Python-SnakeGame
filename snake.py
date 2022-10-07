import pygame,random
from math import sqrt

pygame.init() 

background_color = (162,205,90) # light green
(width, height) = (600, 640)
window = pygame.display.set_mode((width, height))
red_color = (255,0,0) 
black_color = (0,0,0) 
pygame.display.flip() 
pygame.display.set_caption('Snake Game by Max')
font = pygame.font.SysFont(pygame.font.get_default_font(),50) 
still_playing = True
game_over = False 
x_snake = 285  
y_snake = 305 
score = 0
time = pygame.time.Clock() 

class Snake:
    def __init__(self,x,y,x_change,y_change):
        self.x = x
        self.y = y
        self.x_change = x_change
        self.y_change = y_change
        self.width = 20
        self.height = 20
        self.color = (0,100,0)
        self.body = [(x,y)]
        self.dir = (0,0)
    
    def draw(self): 
        for i in range(len(self.body)): 
            x,y = self.body[i] 
            pygame.draw.rect(window, self.color, pygame.Rect(x,y,self.width,self.height)) # x, y, w, h 
    
    def move_glizzy(self): 
        for i in reversed(range(len(self.body))): 
            if i == 0: 
                (x_change, y_change) = self.set_movement_glizzy(self.dir)
                x,y = self.body[i]
                x += x_change
                y += y_change
                self.body[i] = (x,y) 
            else: 
                (x,y) = self.body[i-1]
                (x1,y1) = self.body[i]
                distance = (x-x1,y-y1)
                magnitude = sqrt((distance[0]*distance[0]) + (distance[1] * distance[1]))
                normalize_dist = (distance[0]/magnitude, distance[1]/magnitude)
                (x_change, y_change) = self.set_movement_glizzy(normalize_dist)
                x,y = self.body[i]
                x += x_change
                y += y_change
                self.body[i] = (x,y)
    
    def grow(self):
        self.x,self.y = self.body[len(self.body)-1] 
        if self.dir == (-1,0):
            self.x += self.height
        elif self.dir  == (1,0):
            self.x -= self.height
        elif self.dir  == (0,-1):
            self.y +=  self.height
        elif self.dir  == (0,1):
            self.y -= self.height 
        self.body.append((self.x,self.y)) 
    
    def set_movement_glizzy(self,dir):
        x_change, y_change = 0, 0
        if dir == None: 
            dir = self.dir 
        x_change = 3 * dir[0]
        y_change = 3 * dir[1]
        return (x_change, y_change)
        

class Apple : 
    def __init__(self, apple_x, apple_y, apple_radius):
        self.apple_x = apple_x
        self.apple_y = apple_y
        self.apple_radius = apple_radius # size 
        self.apple_xy = apple_x, apple_y
    
    def draw(self): 
        pygame.draw.circle(window, red_color,(self.apple_x,self.apple_y),self.apple_radius)


def user_message(msg,color):
    messg = font.render(msg, True, color) 
    msg_rect = messg.get_rect()
    msg_rect.center = (width/2, height/2)
    window.blit(messg, msg_rect) #overlap new image on game screen 

def show_game_over_state():
    user_message("You are dead!!! Press 'r' to play again", red_color)

def score_message(score, color): 
    score_msg = font.render(score, True, color) 
    score_rect = score_msg.get_rect() 
    score_rect.center = (85,50)
    window.blit(score_msg, score_rect)

def show_score(score): 
    score_message("Score : " + str(score), black_color)

def playing(apple, snake, game_over, score): 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            game_over = True 
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_LEFT:
                snake.dir= (-1,0)
            elif event.key == pygame.K_RIGHT:
                snake.dir= (1,0)
            elif event.key == pygame.K_UP:
                snake.dir= (0,-1)
            elif event.key == pygame.K_DOWN:
                snake.dir= (0,1)

    if snake.body[0][0] >= width or snake.body[0][0] < 0 or snake.body[0][1] >= height or snake.body[0][1] < 0: 
        game_over = True

    snake.move_glizzy()
    window.fill(background_color)   
    snake.draw()
    show_score(score)
    apple.draw()
    threshold = 25 
    snake_x, snake_y = snake.body[0]
    if  (threshold*-1 <= (snake_x - apple.apple_x) <= threshold) and (threshold*-1 <= (snake.body[0][1] - apple.apple_y) <= threshold): 
        score += 1
        snake.grow()
        apple.apple_x = random.randrange(20,580) 
        apple.apple_y = random.randrange(20,620) 
    return (game_over, score) 

def reset() :
    dict1 = {
        "game_over" : False,
        "score" : 0, 
        "snake" : Snake(x=285,y=300,x_change=0,y_change=0),
        "apple" : Apple(apple_x=random.randrange(20,580),apple_y=random.randrange(20,620),apple_radius=10), 
    }
    return dict1
    
reesess = reset() 
game_over = reesess["game_over"]
snake = reesess["snake"] 
apple = reesess["apple"] 
score = reesess["score"]
time.tick(1) 

while still_playing :
    if game_over : 
        show_game_over_state() 
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r : 
                reesess = reset()
                game_over = reesess["game_over"]
                snake = reesess["snake"] 
                apple = reesess["apple"] 
                score = reesess["score"]
    else :
        game_over,score = playing(apple,snake,game_over,score)  
    pygame.display.update() 
pygame.quit() 
quit() 

