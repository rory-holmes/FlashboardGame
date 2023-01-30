import pygame
import json
import random

from Game import Game


""" Class containing the snake pygame """

class SnakeGame(Game):

    def __init__(self):
        super().__init__("Snake")
        self.snake = [ (0, self.row_num//2)]
        self.running = True
        self.current_dir = (1, 0)

        super().difficulty_screen()

    def set_next_food(self):
        """ Sets the next location of the snake food """
        run = True
        while run:
            self.next_food = (random.randint(0, self.row_num-1), random.randint(0, self.col_num-1))
            if self.next_food not in self.snake:
                run = False
            elif len(self.snake) == (self.col_num * self.row_num):
                #TODO Run win animation
                pass
        self.matrix[self.next_food[0]][self.next_food[1]] = 2

    def move_snake(self):
        """ Moves snake in the given direction 
        Inputs:
        -------
        direction - (x, y) for -1 <= x, y <= 1 """

        tail_x, tail_y = self.snake[0][0], self.snake[0][1]
        head_x, head_y = self.snake[-1][0], self.snake[-1][1]


        # Position of new head of the snake, loops around if out of bounds
        new_head = ((head_x + self.current_dir[0]), (head_y + self.current_dir[1]))
        if new_head[0] > (self.row_num-1):
            new_head = (0, new_head[1])
        if new_head[0] < 0:
            new_head = ((self.row_num-1), new_head[1])
        if new_head[1] > (self.col_num-1):
            new_head = (new_head[0], 0)
        if new_head[1] < 0:
            new_head = (new_head[0], (self.col_num-1))

        if new_head == self.next_food:
            self.increase_snake()

        if new_head in self.snake:
            self.running = False
            self.matrix[new_head[0]][new_head[1]] = 3
            self.render_game()
            pygame.time.wait(9000)
            return

        # Update snake list
        del self.snake[0]
        self.snake.append(new_head)

        # Update matrix to show snake
        self.matrix[tail_x][tail_y] = 0
        self.matrix[head_x][head_y] = 1
        self.matrix[new_head[0]][new_head[1]] = 4
    
    def increase_snake(self):
        """ Adds another circle to the tail of the snake """

        # Calculate where to put the new tail based off of the current tail orientation
        tail = (self.snake[0][0], self.snake[0][1])
        dir = ((self.current_dir[0]*-1), (self.current_dir*-1))
        new_tail = ((tail[0] + dir[0]), (tail[1] + dir[1]))

        # Add new tail to the snake
        self.snake = [new_tail] + self.snake
        # self.matrix[new_tail[0]][new_tail[1]] = 4
        self.set_next_food()
    
    def run(self):
        """ Runs the main game loop """
        self.start()
        self.set_next_food()

        # Set the title of the window
        pygame.display.set_caption("Memory Game")
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_mode(self.size)

        # Create clock object
        clock = pygame.time.Clock()

        move_wait = 400

        while self.running:
            # Resets the clicked circle back to a grey after the flash_time interval
            if self.time_passed > move_wait:
                self.time_passed = 0
                self.move_snake()

            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.current_dir = (-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.current_dir = (1, 0)
                    elif event.key == pygame.K_UP:
                        self.current_dir = (0, -1)
                    elif event.key == pygame.K_DOWN:
                        self.current_dir = (0, 1)
                
            self.render_game()
            self.time_passed += clock.tick(30)