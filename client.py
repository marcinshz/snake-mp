import pygame
import random
import socket
import pickle
import time

class SnakeClient:
    def __init__(self, HOST='127.0.0.1', PORT=65432):
        self.HOST = HOST
        self.PORT = PORT
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def Connect(self):
        self.s.connect((self.HOST, self.PORT))

    def Send(self, snake):
        data = pickle.dumps(snake)
        self.s.sendall(data)

    def Receive(self):
        data = self.s.recv(1024)
        enemy_snake = pickle.loads(data)
        return enemy_snake

class Snake:
    def __init__(self, multiplayer=False, HOST='127.0.0.1', PORT=65432):
        pygame.init()
        self.screen = pygame.display.set_mode((600, 600))
        pygame.display.set_caption('Snake')

        self.running = True
        self.multiplayer = multiplayer
        self.food_pos = []
        self.direction = "Up"
        self.current_direction = self.direction

        if self.multiplayer:
            self.sc = SnakeClient(HOST, PORT)
            self.sc.Connect()
        self.enemy_snake = []
        self.snake = self.GetSpawnPos()
        self.GameLoop()

    def GetSpawnPos(self):
        x = 0
        y = 0
        not_in_other_snake = False
        while True:
            x = random.randint(3, 25) * 20
            y = random.randint(3, 26) * 20
            not_in_other_snake = True
            for yadd in range(0, 200, 20):
                if not not_in_other_snake:
                    break
                for xadd in range(0, 200, 20):
                    if ([x + xadd, y + yadd] not in self.enemy_snake and
                        [x - xadd, y - yadd] not in self.enemy_snake and
                        [x + xadd, y - yadd] not in self.enemy_snake and
                        [x - xadd, y + yadd] not in self.enemy_snake):
                        pass
                    else:
                        not_in_other_snake = False
                        break
            if not_in_other_snake:
                break
        return [[x, y], [x + 20, y]]

    def KeyPressed(self):
        key_input = pygame.key.get_pressed()
        if key_input[pygame.K_UP] and self.current_direction != "Down":
            self.direction = "Up"
        elif key_input[pygame.K_DOWN] and self.current_direction != "Up":
            self.direction = "Down"
        elif key_input[pygame.K_RIGHT] and self.current_direction != "Left":
            self.direction = "Right"
        elif key_input[pygame.K_LEFT] and self.current_direction != "Right":
            self.direction = "Left"

    def GameLoop(self):
        fps = 10
        frametime = 1 / fps
        t = time.time()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                self.KeyPressed()
            if time.time() - t >= frametime:
                self.screen.fill((0, 0, 0))
                self.HeadPosition = self.snake[-1]
                self.MoveSnake()
                self.MapBorder()
                self.DrawSnake(self.snake, (0, 0, 255), (255, 255, 0))

                if self.multiplayer:
                    self.sc.Send(self.snake)
                    self.enemy_snake = self.sc.Receive()
                    self.food_pos = self.enemy_snake[-1]
                    self.Food()
                    self.enemy_snake = self.enemy_snake[:-1]
                    self.DrawSnake(self.enemy_snake, (255, 0, 255), (0, 255, 255))
                else:
                    self.Food()

                self.GetTailHit()
                pygame.display.flip()
                t = time.time()

    def DrawSnake(self, snake, head_color, tail_color):
        for index, value in enumerate(snake):
            try:
                next_value = snake[index + 1]
                if next_value[0] > value[0]:
                    pygame.draw.rect(self.screen, tail_color,
                                     (value[0] + 2, value[1] + 2, 20, 16))
                elif next_value[0] < value[0]:
                    pygame.draw.rect(self.screen, tail_color,
                                     (value[0] - 2, value[1] + 2, 20, 16))
                elif next_value[1] > value[1]:
                    pygame.draw.rect(self.screen, tail_color,
                                     (value[0] + 2, value[1] + 2, 16, 20))
                elif next_value[1] < value[1]:
                    pygame.draw.rect(self.screen, tail_color,
                                     (value[0] + 2, value[1] - 2, 16, 20))
            except:
                pygame.draw.rect(self.screen, head_color,
                                 (value[0] + 2, value[1] + 2, 16, 16))

    def SnakeDead(self):
        self.snake = self.GetSpawnPos()

    def MapBorder(self):
        border_start = 0
        border_end = 580
        border_thickness = 20

        pygame.draw.rect(self.screen, (0, 255, 0), (border_start,
                                                   border_start, border_end, border_thickness))
        pygame.draw.rect(self.screen, (0, 255, 0), (border_start,
                                                   border_start, border_thickness, border_end))
        pygame.draw.rect(self.screen, (0, 255, 0), (border_end,
                                                   border_start, border_thickness, border_end))
        pygame.draw.rect(self.screen, (0, 255, 0), (border_start,
                                                   border_end, border_end + border_thickness, border_thickness))

        if not border_end > self.HeadPosition[1] > 0:
            self.SnakeDead()
        if not border_end > self.HeadPosition[0] > 0:
            self.SnakeDead()

    def MoveSnake(self):
        for index, value in enumerate(self.snake):
            try:
                self.snake[index] = [
                    int(self.snake[index + 1][0]), int(self.snake[index + 1][1])]
            except:
                if self.direction == "Down":
                    self.snake[index][1] += 20
                if self.direction == "Up":
                    self.snake[index][1] -= 20
                if self.direction == "Left":
                    self.snake[index][0] -= 20
                if self.direction == "Right":
                    self.snake[index][0] += 20
        self.current_direction = self.direction

    def Food(self):
        while not self.food_pos:
            x = random.randint(2, 28) * 20
            y = random.randint(2, 28) * 20
            if not [x, y] in self.snake:
                self.food_pos = [x, y]
        pygame.draw.rect(self.screen, (255, 0, 0),
                         (self.food_pos[0] + 2, self.food_pos[1] + 2, 16, 16))

        if self.HeadPosition == self.food_pos:
            self.food_pos = []
            self.snake.insert(0, self.snake[0])

    def GetTailHit(self):
        if self.HeadPosition in self.snake[:-1] or self.HeadPosition in self.enemy_snake:
            self.SnakeDead()

if __name__ == "__main__":
    game = Snake(multiplayer=True)
