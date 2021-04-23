import time
import random
import pygame
from pygame.locals import *

BLOCKSIZE = 40
BACKGROUND_COLOR = (135,86,0)
TEXT_COLOR = (255,255,255)
WINDOW_X = 1200
WINDOW_Y = 800
# The max X and Y positions objects are allowed to spawn with, 
# to avoid objects spawning offscreen
X_MAX = WINDOW_X - BLOCKSIZE
Y_MAX = WINDOW_Y - BLOCKSIZE

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Python Snake Game')
        pygame.mixer.init() # Initialize sounds
        self.play_bgm('bgm.mp3', 0.1)
        # Draw the window
        self.surface = pygame.display.set_mode(size=(WINDOW_X, WINDOW_Y))
        self.snake = Snake(self.surface, 3)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()
        self.orange_portal = Portal(self.surface)
        self.blue_portal = Portal(self.surface)
        self.orange_portal.draw('orange')
        self.blue_portal.draw('blue')

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + BLOCKSIZE: # x1 is on top of x2
            if y1 >= y2 and y1 < y2 + BLOCKSIZE:
                return True

    def is_offscreen(self, x1, y1, x2, y2,):
        if x1 >= x2 or x1 < 0 or y1 >= y2 or y1 < 0: # snake is outside of window
            return True

    def render_background(self):
        bg = pygame.image.load('assets/background.jpg')
        self.surface.blit(bg, (0,0))

    def display_score(self):
        font = pygame.font.SysFont('comic sans MS', 30)
        score = font.render(f'Score: {self.snake.length*10}', True, TEXT_COLOR)
        self.surface.blit(score, (970,10))

    # 'Sound' param requires filetype e.g. sfx.wav
    def play_sound(self, sound, volume):
        sfx = pygame.mixer.Sound(f'assets/{sound}')
        pygame.mixer.Sound.set_volume(sfx, volume)
        pygame.mixer.Sound.play(sfx)

    # 'Music' param requires filetype e.g. bgm.mp3
    def play_bgm(self, music, volume):
        pygame.mixer.music.load(f'assets/{music}')
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1) # -1 loops for infinite looping

    def play(self): # Runs every frame
        self.render_background()
        self.snake.move()
        self.apple.draw()
        self.orange_portal.draw('orange')
        self.blue_portal.draw('blue')
        self.display_score()
        pygame.display.flip()

        # Snake eating apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound('chomp.wav', 0.2)
            self.snake.increase_length()
            self.apple.move()

        # Snake enters orange portal - warps to blue
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.orange_portal.x, self.orange_portal.y):
            self.snake.x[0] = self.blue_portal.x
            self.snake.y[0] = self.blue_portal.y
            #self.orange_portal.move()
            #self.blue_portal.move()
        # Snake enters blue portal - warps to orange
        elif self.is_collision(self.snake.x[0], self.snake.y[0], self.blue_portal.x, self.blue_portal.y):
            self.snake.x[0] = self.orange_portal.x
            self.snake.y[0] = self.orange_portal.y
            #self.orange_portal.move()
            #self.blue_portal.move()

        # Snake collising with itself - game over
        for i in range(1, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound('game-over-2.wav', 0.3)
                raise 'Game Over'

        # Snake collides with edge of window - game over
        #if self.is_offscreen(self.snake.x[0], self.snake.y[0], WINDOW_X, WINDOW_Y):
        #    self.play_sound('game-over-2.wav', 0.3)
        #    raise 'Game Over'

        # Snake goes offscreen and wraps around pac man style
        if self.is_offscreen(self.snake.x[0], self.snake.y[0], WINDOW_X, WINDOW_Y):
            if self.snake.x[0] >= WINDOW_X: # offscreen to the right
                self.snake.x[0] = 0
            elif self.snake.x[0] <= 0: # offecreen to the left
                self.snake.x[0] = WINDOW_X
            elif self.snake.y[0] >= WINDOW_Y: # offscreen to the bottom
                self.snake.y[0] = 0
            elif self.snake.y[0] <= 0: # offscreen to the top
                self.snake.y[0] = WINDOW_Y

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('comic sans MS', 30)
        line1 = font.render(f'Game Over! Your final score is {self.snake.length*10}', True, TEXT_COLOR)
        self.surface.blit(line1, (350, 300))
        line2 = font.render(f'Hit Enter to go agane, or Esc to quit.', True, TEXT_COLOR)
        self.surface.blit(line2, (350, 350))
        pygame.display.flip()

    def reset(self):
        self.snake = Snake(self.surface, 3)
        self.apple = Apple(self.surface)
        self.orange_portal = Portal(self.surface)
        self.blue_portal = Portal(self.surface)

    def run(self):
        # Game loop
        running = True
        paused = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                
                    if event.key == K_RETURN:
                        if paused: # Stops enter key restarting music in game
                            self.play_bgm('bgm.mp3', 0.1)
                        paused = False

                    if not paused: # direction check prevents snake turning 180 degrees and colliding
                        if event.key == K_w and self.snake.direction != 'down':
                            self.snake.move_up()
                        if event.key == K_s and self.snake.direction != 'up':
                            self.snake.move_down()
                        if event.key == K_a and self.snake.direction != 'right':
                            self.snake.move_left()
                        if event.key == K_d and self.snake.direction != 'left':
                            self.snake.move_right()

                elif event.type == QUIT:
                    running = False

            try:
                if not paused:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pygame.mixer.music.stop()
                paused = True
                self.reset()
            time.sleep(0.1) # Game speed

class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.head = pygame.image.load('assets/block_head.jpg').convert()
        self.body = pygame.image.load('assets/block.jpg').convert()
        self.stripe = pygame.image.load('assets/block2.jpg').convert()
        # init an array of size 'length'
        self.x = [BLOCKSIZE] * length
        self.y = [BLOCKSIZE] * length
        self.direction = 'down'

    def draw(self):
        for i in range(self.length):
            if i == 0: # Snake's head
                self.parent_screen.blit(self.head, (self.x[i], self.y[i]))
            elif i % 2 == 0: # Adjust colour patterns by changing condition
                self.parent_screen.blit(self.stripe, (self.x[i], self.y[i]))
            else:
                self.parent_screen.blit(self.body, (self.x[i], self.y[i]))
        pygame.display.flip()
    
    def increase_length(self):
        self.length +=1
        self.x.append(-1)
        self.y.append(-1)

    def move(self):
        for i in range(self.length -1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == 'up':
            self.y[0] -= BLOCKSIZE
        if self.direction == 'down':
            self.y[0] += BLOCKSIZE
        if self.direction == 'left':
            self.x[0] -= BLOCKSIZE
        if self.direction == 'right':
            self.x[0] += BLOCKSIZE
        self.draw()

    def move_up(self):
        self.direction = 'up'
        self.draw()

    def move_down(self):
        self.direction = 'down'
        self.draw()
    
    def move_left(self):
        self.direction = 'left'
        self.draw()
    
    def move_right(self):
        self.direction = 'right'
        self.draw()

class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load('assets/apple.png').convert_alpha()
        self.parent_screen = parent_screen
        # Apples can't spawn on the edges of the screen and break collision
        self.x = random.randrange(BLOCKSIZE, X_MAX, BLOCKSIZE)
        self.y = random.randrange(BLOCKSIZE, Y_MAX, BLOCKSIZE)

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()
    
    def move(self): # Re randomise position
        self.x = random.randrange(BLOCKSIZE, X_MAX, BLOCKSIZE)
        self.y = random.randrange(BLOCKSIZE, Y_MAX, BLOCKSIZE)
        #self.draw()

# TODO: Create decoy apple object that hurts the snake in some way

# TODO: Add functionality to wait before moving portals
class Portal:
    def __init__(self, parent_screen):
        self.orange_image = pygame.image.load('assets/orange_portal.jpg').convert()
        self.blue_image = pygame.image.load('assets/blue_portal.jpg').convert()
        self.parent_screen = parent_screen
        self.x = random.randrange(BLOCKSIZE, X_MAX, BLOCKSIZE)
        self.y = random.randrange(BLOCKSIZE, Y_MAX, BLOCKSIZE)

    def draw(self, color):
        self.color = color
        if color == 'orange':
            self.parent_screen.blit(self.orange_image, (self.x, self.y))
        elif color == 'blue':
            self.parent_screen.blit(self.blue_image, (self.x, self.y))
        pygame.display.flip()

    def move(self): # Re randomise position
        self.x = random.randrange(BLOCKSIZE, X_MAX, BLOCKSIZE)
        self.y = random.randrange(BLOCKSIZE, Y_MAX, BLOCKSIZE)

if __name__ == '__main__':
    game = Game()
    game.run()
