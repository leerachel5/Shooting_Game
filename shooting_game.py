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

class Heart(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.pos = pygame.math.Vector2(0, 0)

        self.image = pygame.transform.scale(pygame.image.load("assets/heart.png"), (40, 40))

        self.rect = self.image.get_rect()

    def set_pos(self, x, y):
        self.pos.xy = x, y
        self.rect.x = self.pos.x - self.rect.w / 2
        self.rect.y = self.pos.y - self.rect.h / 2


class Block(pygame.sprite.Sprite):
    """ This class represents the block. """
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.pos = pygame.math.Vector2(0, 0)
        self.v = pygame.math.Vector2(0, 0)
 
        self.image = pygame.transform.scale(pygame.image.load("assets/asteroid.png"), [25, 25])

        self.rect = self.image.get_rect()

    def set_pos(self, x, y):
        self.pos.xy = x, y
        self.rect.x = self.pos.x - self.rect.w / 2
        self.rect.y = self.pos.y - self.rect.h / 2

    def update(self):
        """ Find a new position for the player"""
        self.set_pos(self.pos.x + self.v.x, self.pos.y + self.v.y)


class Player(pygame.sprite.Sprite):
    """ This class represents the Player. """
 
    def __init__(self):
        """ Set up the player on creation. """
        # Call the parent class (Sprite) constructor
        super().__init__()
 
        # Load and resize shooter
        self.image = pygame.transform.scale(pygame.image.load("assets/shooter.png"), [80, 55])
 
        self.rect = self.image.get_rect()
 
        # Set speed vector
        self.pos = pygame.math.Vector2(0, 0)

        self.v = pygame.math.Vector2(0, 0)

    def set_pos(self, x, y):
        self.pos.xy = x, y
        self.rect.x = self.pos.x - self.rect.w / 2
        self.rect.y = self.pos.y - self.rect.h / 2

    def update(self):
        """ Find a new position for the player"""
        self.set_pos(self.pos.x + self.v.x, self.pos.y + self.v.y)

 
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
        self.pos = pygame.math.Vector2(x, y)
        self.set_pos(x, y)
 
        speed = 3
        self.v = pygame.math.Vector2(speed * vx, speed * vy)


    def set_pos(self, x, y):
        self.pos.xy = x, y
        self.rect.x = self.pos.x - self.rect.w / 2
        self.rect.y = self.pos.y - self.rect.h / 2


    def update(self):
        """ Find a new position for the player"""
        self.set_pos(self.pos.x + self.v.x, self.pos.y + self.v.y)
 

class Game():
    def __init__(self):
        pygame.init()
        
        self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

        self.players = pygame.sprite.Group()

        self.shooting = False
        self.fire_timer = 0
        self.fire_time_limit = 5

        # List of each heart in the game
        self.hearts = pygame.sprite.Group()

        # List of each block in the game
        self.blocks = pygame.sprite.Group()
        
        # List of each bullet
        self.bullets = pygame.sprite.Group()
        
        # Create hearts and set position
        self.heart1 = Heart()

        self.heart1.set_pos(23, 23)

        self.heart2 = Heart()

        self.heart2.set_pos(63, 23)

        self.heart3 = Heart()
        
        self.heart3.set_pos(103, 23)

        self.hearts.add(self.heart1, self.heart2, self.heart3)
   
        # Create player and set position to middle of screen
        self.player = Player()
        self.player.set_pos(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

        self.players.add(self.player)

        # Loop until the user clicks the close button.
        self.running = True

        self.score = 0
        self.lives = 3
        
        # Used to manage how fast the screen updates
        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font(None, 36)

        self.game_over = False

    def create_blocks(self):
        
        for i in range(3):
            # This represents a block
            block = Block()
        
            # Set a random location for the block
            block.set_pos(random.randrange(-25, 0), random.randrange(SCREEN_HEIGHT))

            # Add the block to the list of objects
            self.blocks.add(block)

        for i in range(3):
            block = Block()

            block.set_pos(random.randrange(700 , 725), random.randrange(SCREEN_HEIGHT))

            self.blocks.add(block)

        for i in range(3):
            block = Block()
        
            block.set_pos(random.randrange(SCREEN_WIDTH), random.randrange(-25, 0))

            self.blocks.add(block)

        for i in range(3):
            block = Block()
        
            block.set_pos(random.randrange(SCREEN_WIDTH), random.randrange(400, 425))

            self.blocks.add(block)
            
            break

    def fire_bullets(self):
        """Fire bullets based on a fire timer
        and tells the bullet where to go"""

        if self.fire_timer < self.fire_time_limit:
            self.fire_timer += 1
        else:
            self.fire_timer = 0

            # Create the bullet based on where we are, and where we want to go.
            bullet = Bullet(
                self.player.pos.x, self.player.pos.y,
                self.player.v.x, self.player.v.y
            )

            # Add the bullet to the lists
            self.bullets.add(bullet)
        
    def update_blocks_velocity(self):
        
        for block in self.blocks:
            new_v = self.player.pos - block.pos
            block.v = 0.7 * new_v.normalize()

    def update(self):
        self.clock.tick(60)

        self.handle_input()

        if len(self.blocks) % 12 == 0:
            self.create_blocks()

        if self.shooting:
            self.fire_bullets()
 
        self.blocks.update()
        self.player.update()
        self.bullets.update()

        self.update_blocks_velocity()
 
        # Calculate mechanics for each bullet
        for bullet in self.bullets:
            # See if it hit a block
            block_hit_list = pygame.sprite.spritecollide(bullet, self.blocks, True)
    
            # For each block hit, remove the bullet and add to the score
            if bullet.pos.y < -10 or bullet.pos.y > SCREEN_HEIGHT:
                self.bullets.remove(bullet)
            elif bullet.pos.x < -10 or bullet.pos.x > SCREEN_WIDTH:
                self.bullets.remove(bullet)
            else:
                for block in block_hit_list:
                    self.bullets.remove(bullet)
                    self.blocks.remove(block)
                    self.score += 1

        # Calculate mechanics for each block collision
        for player in self.players:
            # See if it hit a block
            player_hit_list = pygame.sprite.spritecollide(player, self.blocks, True)
    
            # For each block hit, remove the bullet and add to the score
            for block in player_hit_list:
                self.blocks.remove(block)
                self.lives -= 1

                if self.lives == 2:
                    self.hearts.remove(self.heart3)
                elif self.lives == 1:
                    self.hearts.remove(self.heart2)
                elif self.lives == 0:
                    self.hearts.remove(self.heart1)
                    self.game_over = True

        self.screen.fill(BLACK)
    
        # Draw all the spites

        self.blocks.draw(self.screen)
        self.bullets.draw(self.screen)
        self.players.draw(self.screen)
        self.hearts.draw(self.screen)

        pygame.display.flip()

        basicfont = pygame.font.SysFont(None, 48)
        text = basicfont.render('SCORE:' + str(self.score), True, (WHITE), (BLACK))
        textrect = text.get_rect()
        textrect.x = 530
        textrect.y = 13

        self.screen.blit(text, textrect)

        pygame.display.update()

        if self.game_over:
            for block in self.blocks:
                self.blocks.remove(block)
            for player in self.players:
                self.players.remove(player)
            for bullet in self.bullets:
                self.bullets.remove(bullet)
            
            bg = pygame.image.load("assets/game_over.jpg")
            self.screen.blit(bg, (-80, -70))

            pygame.display.update()

        
    def handle_input(self):
        """Takes user input and determines
        the velocity of the player as well
        as whether to shoot bullets"""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.v.x = -4          
                elif event.key == pygame.K_RIGHT:
                    self.player.v.x = 4
                if event.key == pygame.K_UP:
                    self.player.v.y = -4
                elif event.key == pygame.K_DOWN:
                    self.player.v.y = 4

                self.shooting = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.player.v.x = 0
                if event.key == pygame.K_RIGHT:
                    self.player.v.x = 0
                if event.key == pygame.K_UP:
                    self.player.v.y = 0
                if event.key == pygame.K_DOWN:
                    self.player.v.y = 0

                self.shooting = False
            

# Main Program Loop
game = Game()

while game.running:
    game.update()