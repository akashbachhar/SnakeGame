import pygame
import random
import os

pygame.init()
pygame.mixer.init()

white = (255, 255, 255)
red = (212, 0, 0)
black = (0, 0, 0)
blue = (6, 2, 230)
green = (81, 245, 92)
dark_blue = (1, 1, 54)
screen_width = 900
screen_height = 600

gameWindow = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game")
pygame.display.update()
clock = pygame.time.Clock()

font1 = pygame.font.SysFont('sans-serif', 50)
font2 = pygame.font.SysFont('timesnewroman', 30)


def text_screen(text, color, x, y):
    screen_text = font1.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])


def text_screen_small(text, color, x, y):
    screen_text = font2.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])


def plot_snake(windowGame, snake_list, snake_size):
    for x, y in snake_list:
        pygame.draw.rect(windowGame, black, [x, y, snake_size, snake_size])


def welcome():
    exit_game = False
    fps = 30
    while not exit_game:
        gameWindow.fill(green)
        text_screen("Welcome to SNAKE GAME !", red, 240, 220)
        text_screen("Press 'SPACE' to Play the Game", blue, 210, 270)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    gameloop()

        pygame.display.update()
        clock.tick(fps)


def gameloop():
    if not os.path.exists("highscore.txt"):
        with open("highscore.txt", "w") as f:
            f.write("0")

    with open("highscore.txt", "r") as f:
        highscore = f.read()

    score = 0
    exit_game = False
    game_over = False

    snake_size = 15
    snake_x = 100
    snake_y = 100
    velocity_x = 0
    velocity_y = 0
    init_velocity = 6

    snake_list = []
    snake_length = 1

    food_x = random.randint(20, screen_width)
    food_y = random.randint(20, screen_height)
    fps = 30

    while not exit_game:
        if game_over:
            with open("highscore.txt", "w") as f:
                f.write(str(highscore))

            gameWindow.fill(green)
            text_screen("Game Over !", red, 330, 100)
            text_screen("Press 'ENTER' to Play Again ! ", red, 210, 150)
            text_screen("Score: " + str(score), black, 200, 270)
            text_screen_small("High Score: " + str(highscore), black, 200, 305)
            text_screen_small("Developer: Akash Bachhar", blue, 300, 450)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        gameloop()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_LEFT:
                        velocity_x = - init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_UP:
                        velocity_x = 0
                        velocity_y = - init_velocity
                    if event.key == pygame.K_DOWN:
                        velocity_x = 0
                        velocity_y = init_velocity
                    if event.key == pygame.K_q:
                        score += 50

            snake_x += velocity_x
            snake_y += velocity_y

            if abs(snake_x - food_x) < 12 and abs(snake_y - food_y) < 12:
                score += 10
                pygame.mixer.music.load("beep.mp3")
                pygame.mixer.music.play()
                food_x = random.randint(50, screen_width - 20)
                food_y = random.randint(50, screen_height - 20)
                snake_length += 5

                if score > int(highscore):
                    highscore = score
            gameWindow.fill(green)
            text_screen("Score: " + str(score) + "    High Score: " + str(highscore), blue, 5, 5)
            pygame.draw.circle(gameWindow, red, [food_x, food_y], snake_size / 1.5)

            head = [snake_x, snake_y]
            snake_list.append(head)

            if len(snake_list) > snake_length:
                del snake_list[0]
            if head in snake_list[:-1]:
                game_over = True
                pygame.mixer.music.load("over.wav")
                pygame.mixer.music.play()
            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True
                pygame.mixer.music.load("over.wav")
                pygame.mixer.music.play()

            plot_snake(gameWindow, snake_list, snake_size)

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()


welcome()
