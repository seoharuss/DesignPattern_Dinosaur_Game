import pygame
import os
import random
pygame.init()

# Global Constants
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))


# State Pattern
class DinoState:
    def handle_input(self, dino, userInput):
        pass

    def update(self, dino):
        pass

    def enter(self, dino):
        pass

class RunningState(DinoState):
    def enter(self, dino):
        dino.dino_run = True
        dino.dino_duck = False
        dino.dino_jump = False
        dino.image = dino.run_img[0]
        dino.dino_rect.y = dino.Y_POS

    def handle_input(self, dino, userInput):
        if userInput[pygame.K_UP]:
            dino.set_state(JumpingState())
        elif userInput[pygame.K_DOWN]:
            dino.set_state(DuckingState())

    def update(self, dino):
        dino.image = dino.run_img[dino.step_index // 5]
        dino.dino_rect.x = dino.X_POS
        dino.dino_rect.y = dino.Y_POS
        dino.step_index = (dino.step_index + 1) % 10

class DuckingState(DinoState):
    def enter(self, dino):
        dino.dino_run = False
        dino.dino_duck = True
        dino.dino_jump = False
        dino.image = dino.duck_img[0]
        dino.dino_rect.y = dino.Y_POS_DUCK

    def handle_input(self, dino, userInput):
        if not userInput[pygame.K_DOWN]:
            dino.set_state(RunningState())

    def update(self, dino):
        dino.image = dino.duck_img[dino.step_index // 5]
        dino.dino_rect.x = dino.X_POS
        dino.dino_rect.y = dino.Y_POS_DUCK
        dino.step_index = (dino.step_index + 1) % 10

class JumpingState(DinoState):
    def enter(self, dino):
        dino.dino_run = False
        dino.dino_duck = False
        dino.dino_jump = True
        dino.image = dino.jump_img
        dino.jump_vel = dino.JUMP_VEL

    def handle_input(self, dino, userInput):
        pass

    def update(self, dino):
        if dino.dino_jump:
            dino.dino_rect.y -= dino.jump_vel * 4
            dino.jump_vel -= 0.8
            if dino.jump_vel < -dino.JUMP_VEL:
                dino.set_state(RunningState())

# Dinosaur Class with State Pattern
class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.step_index = 0
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

        self.state = RunningState()
        self.state.enter(self)

    def set_state(self, state):
        self.state = state
        self.state.enter(self)

    def update(self, userInput):
        self.state.handle_input(self, userInput)
        self.state.update(self)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

# Strategy Pattern for Obstacle Update
class ObstacleUpdateStrategy:
    def update(self, obstacle):
        pass

class DefaultUpdateStrategy(ObstacleUpdateStrategy):
    def update(self, obstacle):
        obstacle.rect.x -= game_speed
        if obstacle.rect.x < -obstacle.rect.width:
            obstacles.pop()

# Factory Pattern for Obstacles
class ObstacleFactory:
    @staticmethod
    def create_obstacle(obstacle_type):
        if obstacle_type == "small_cactus":
            return SmallCactus()
        elif obstacle_type == "large_cactus":
            return LargeCactus()
        elif obstacle_type == "bird":
            return Bird()

# Obstacle Classes
class Obstacle:
    def __init__(self, image, type, update_strategy):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH
        self.update_strategy = update_strategy

    def update(self):
        self.update_strategy.update(self)

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)

class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type, DefaultUpdateStrategy())
        self.rect.y = 325

class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type, DefaultUpdateStrategy())
        self.rect.y = 300

class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type, DefaultUpdateStrategy())
        self.rect.y = 250
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1

# Cloud Class
class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    death_count = 0

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1

        text = font.render("Points: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()

        player.draw(SCREEN)
        player.update(userInput)

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(BIRD))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(2000)
                death_count += 1
                menu(death_count)

        background()

        cloud.draw(SCREEN)
        cloud.update()

        score()

        clock.tick(30)
        pygame.display.update()


def menu(death_count):
    global points
    run = True
    while run:
        SCREEN.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 30)

        if death_count == 0:
            text = font.render("Press any Key to Start", True, (0, 0, 0))
        elif death_count > 0:
            text = font.render("Press any Key to Restart", True, (0, 0, 0))
            score = font.render("Your Score: " + str(points), True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.KEYDOWN:
                main()


menu(death_count=0)
