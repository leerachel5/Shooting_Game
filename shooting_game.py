import pygame
import random
import math
 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
 
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 400

# Classes
 
 
class Block(pygame.sprite.Sprite):
    """ This class represents the block. """
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()
 
        self.image = self.image = pygame.transform.scale(pygame.image.load("assets/asteroid.png"), [25, 25])

        self.rect = self.image.get_rect()
 
 
class Player(pygame.sprite.Sprite):
    """ This class represents the Player. """
 
    def __init__(self):
        """ Set up the player on creation. """
        # Call the parent class (Sprite) constructor
        super().__init__()
 
        # Load and resize shooter
        self.image = pygame.transform.scale(pygame.image.load("assets/shooter.png"), [100, 100])
 
        self.rect = self.image.get_rect()
 
        # Set speed vector
        self.vx = 0
        self.vy = 0

    def set_pos(self, x, y):
        self.x = x
        self.y = y
        self.rect.x = self.x - self.rect.w / 2
        self.rect.y = self.y - self.rect.h / 2

    def update(self):
        """ Find a new position for the player"""
        self.set_pos(self.x + self.vx, self.y + self.vy)

 
class Bullet(pygame.sprite.Sprite):
    """ This class represents the bullet. """
 
    def __init__(self, x, y, vx, vy):
        """ Constructor.
        It takes in the starting x and y location.
        It also takes in the destination x and y position.
        """
 
        # Call the parent class (Sprite) constructor
        super().__init__()
 
        # Set up the image for the bullet
        self.image = pygame.Surface([8, 8])
        self.image.fill(RED)
 
        self.rect = self.image.get_rect()
 
        # Move the bullet to our starting location
        self.set_pos(x, y)
 
        speed = 3
        self.vx = speed * vx
        self.vy = speed * vy


    def set_pos(self, x, y):
        """Set the bullet's position to
         the center of the player's postiion"""
        self.x = x
        self.y = y
        self.rect.x = self.x - self.rect.w / 2
        self.rect.y = self.y - self.rect.h / 2

 
    def update(self):
        """ Move the bullet. """
        self.set_pos(self.x + self.vx, self.y + self.vy)
 

class Game():
    def __init__(self):
        pygame.init()
        
        self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

        self.players = pygame.sprite.Group()
        
        self.shooting = False
        self.fire_timer = 0
        self.fire_time_limit = 6

        # List of each block in the game
        self.blocks = pygame.sprite.Group()
        
        # List of each bullet
        self.bullets = pygame.sprite.Group()
        
        for i in range(50):
            # This represents a block
            block = Block()
        
            # Set a random location for the block
            block.rect.x = random.randrange(SCREEN_WIDTH)
            block.rect.y = random.randrange(SCREEN_HEIGHT - 50)
        
            # Add the block to the list of objects
            self.blocks.add(block)
        
        # Create player and set position to middle of screen
        self.player = Player()
        self.player.set_pos(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

        self.players.add(self.player)

        # Loop until the user clicks the close button.
        self.running = True

        self.score = 0
        
        # Used to manage how fast the screen updates
        self.clock = pygame.time.Clock()


    def fire_bullets(self):
        """Fire bullets based on a fire timer
        and tells the bullet where to go"""

        if self.fire_timer < self.fire_time_limit:
            self.fire_timer += 1
        else:
            self.fire_timer = 0

            # Create the bullet based on where we are, and where we want to go.
            bullet = Bullet(
                self.player.x, self.player.y,
                self.player.vx, self.player.vy
            )

            # Add the bullet to the lists
            self.bullets.add(bullet)
        


    def update(self):
        self.clock.tick(60)

        self.handle_input()

        if self.shooting:
            self.fire_bullets()
 
        self.blocks.update()
        self.player.update()
        self.bullets.update()
 
        # Calculate mechanics for each bullet
        for bullet in self.bullets:
            # See if it hit a block
            block_hit_list = pygame.sprite.spritecollide(bullet, self.blocks, True)
    
            # For each block hit, remove the bullet and add to the score
            if bullet.y < -10 or bullet.y > SCREEN_HEIGHT:
                self.bullets.remove(bullet)
            elif bullet.x < -10 or bullet.x > SCREEN_WIDTH:
                self.bullets.remove(bullet)
            else:
                for block in block_hit_list:
                    self.bullets.remove(bullet)
                    self.blocks.remove(block)
                    self.score += 1
            
        self.screen.fill(BLACK)
    
        # Draw all the spites

        self.blocks.draw(self.screen)
        self.bullets.draw(self.screen)
        self.players.draw(self.screen)

        pygame.display.flip()
    

    def handle_input(self):
        """Takes user input and determines
        the velocity of the player as well
        as whether to shoot bullets"""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.vx = -3            
                elif event.key == pygame.K_RIGHT:
                    self.player.vx = 3
                if event.key == pygame.K_UP:
                    self.player.vy = -3
                elif event.key == pygame.K_DOWN:
                    self.player.vy = 3

                self.shooting = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.player.vx = 0
                if event.key == pygame.K_RIGHT:
                    self.player.vx = 0
                if event.key == pygame.K_UP:
                    self.player.vy = 0
                if event.key == pygame.K_DOWN:
                    self.player.vy = 0

                self.shooting = False
            

# Main Program Loop
game = Game()

while game.running:
    game.update()