import pygame
import random

pygame.font.init()  # To render fonts in our game

# GLOBALS VARS
s_width = 800  # Window width
s_height = 700  # Window Height
play_width = 300  # Play area width, meaning 300 // 10 = 30 width per block
play_height = 600  # Play area height, meaning 600 // 20 = 20 height per block
block_size = 30  # Size of each square block

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

# SHAPE FORMATS
# 0's represent actual blocks. Each list has sub-lists to represent rotations of shape
S = [['.....',
      '......',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]  # list of all shapes
shape_colors = [(250, 100, 100), (100, 250, 100), (100, 100, 250), (250, 250, 100), (250, 100, 250), (100, 250, 250), (128, 20, 128)]


class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape  # get a shape
        self.color = shape_colors[shapes.index(shape)]  # find its colour
        self.rotation = 0


def create_grid(locked_positions={}):
    grid = [[(150, 150, 150) for _ in range(10)] for _ in range(20)]  # set grid background

    for i in range(len(grid)):  # loop through rows
        for j in range(len(grid[i])):  # loop through columns
            if (j, i) in locked_positions:  # if there is a block at that position
                c = locked_positions[(j, i)]  # get colour
                grid[i][j] = c  # set grid colour to that

    return grid


def convert_shape_format(shape):
    positions = []
    rot = shape.shape[shape.rotation % len(shape.shape)]  # find the orientation of shape

    for i, line in enumerate(rot):  # Find positions of 0 in rot
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)  # Offset left and up. Shape spawns above screen

    return positions


def valid_space(shape, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (150, 150, 150)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]  # 2D to 1D

    positions = convert_shape_format(shape)
    for pos in positions:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:  # Top of screen has been reached
            return True
    return False


def update_score(score):
    with open('scores.txt', 'r') as f:  # open txt file in read mode
        lines = f.readlines()
        highscore = lines[0].rstrip()

    with open('scores.txt', 'w') as f:
        if int(highscore) > int(score):
            f.write(str(highscore))
        else:
            f.write(str(score))


def max_score():
    with open('scores.txt', 'r') as f:  # open txt file in read mode
        lines = f.readlines()
        highscore = lines[0].rstrip()

    return highscore


def get_shape():  # Choose a random shape from list
    return Piece(5, 0, random.choice(shapes))


def draw_text_middle(text, size, color, surface):  # To print text in mid screen
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width//2 - (label.get_width())//2,
                         top_left_y + play_height//2 - (label.get_height())//2))


def draw_grid(surface, grid):  # Draw gray lines over blocks
    sx = top_left_x
    sy = top_left_y

    for i in range(len(grid)):
        pygame.draw.line(surface, (255, 255, 255), (sx, sy + i*block_size), (sx + play_width, sy + i*block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (255, 255, 255), (sx + j*block_size, sy), (sx + j*block_size, sy + play_height))


def clear_rows(grid, locked):  # If rows are full at bottom, clear them
    inc = 0  # Number of full rows
    ind = 0

    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if (150, 150, 150) not in row:  # This means all blocks in row are filled
            inc += 1  # increment full row count by 1
            ind = i  # Row that has to be at the bottom
            for j in range(len(row)):  # Now we will delete those locked positions from our dictionary
                try:
                    del locked[(j, i)]
                except:
                    continue

    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1], reverse=True):
            x, y = key  # Extract the coordinates
            if y < ind:  # These rows are to be shifted down
                new_key = (x, y + inc)  # Shift rows below
                locked[new_key] = locked.pop(key)  # Pop old key and add new key

    return inc


def draw_next_shape(shape, surface):  # Display next shape on screen
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('NEXT SHAPE:', 1, (255, 255, 255))  # Create label

    sx = top_left_x + play_width + 50  # X coordinate
    sy = top_left_y + play_height//2 - 100  # Y coordinate

    rot = shape.shape[shape.rotation % len(shape.shape)]  #get the shape

    for i, line in enumerate(rot):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':  # for positions that have 0, we will render that block on screen
                pygame.draw.rect(surface, shape.color, (sx + j*block_size, sy + i*block_size, block_size, block_size), 0)
    surface.blit(label, (sx + 10, sy - 30))  # Render on screen


def draw_window(surface, grid, score=0):
    surface.fill((150, 150, 150))  # fill surface with background colour
    font = pygame.font.SysFont('comicsans', 60)  # Use this font
    label = font.render('TETRIS 2020', 1, (128, 20, 128))  # Text, antialias(smooth edges), colour, background = None
    surface.blit(label, (top_left_x + play_width // 2 - label.get_width() // 2, 30))

    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('SCORE: ' + str(score), 1, (255, 255, 255))  # Create label to display score
    sx = top_left_x + play_width + 50  # X coordinate
    sy = top_left_y + play_height // 2 - 100  # Y coordinate
    surface.blit(label, (sx + 22, sy + 160))

    highscore = max_score()
    label = font.render('HIGH SCORE: ' + str(highscore), 1, (255, 255, 255))  # Create label to display score
    sx = top_left_x - play_width//2 - 50  # X coordinate
    sy = top_left_y + play_height // 2  # Y coordinate
    surface.blit(label, (sx, sy))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j],
                             (top_left_x + j*block_size, top_left_y + i*block_size, block_size, block_size))
    pygame.draw.rect(surface, (20,128, 128),(top_left_x, top_left_y, play_width, play_height), 4)

    draw_grid(surface, grid)  # call draw grid function


def main(window):
    locked_positions = {}
    grid = create_grid(locked_positions)  # Create grid

    change_piece = False
    run = True
    current_piece = get_shape()  # Get the current and next shape
    next_piece = get_shape()
    clock = pygame.time.Clock()
    falltime = 0
    fallspeed = 0.27  # This is actually not speed, but time after which each piece falls a little bit
    level_time = 0  # Represents time that has passed since start of level
    score = 0  # Scoreboard
    close = False  # Return this variable to main window

    while run:
        grid = create_grid(locked_positions)
        falltime += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time/1000 > 10:  # After every 5 seconds we increment speed
            level_time = 0
            if fallspeed > 0.12:  # We set a threshold for maximum speed
                fallspeed -= 0.05

        if falltime/1000 > fallspeed:
            falltime = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid) and current_piece.y > 0:  # if position is not acceptable
                current_piece.y -= 1
                change_piece = True  # Time to change piece as we've hit bottom/another piece
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If close button is pressed, close game
                run = False
                close = True

            if event.type == pygame.KEYDOWN:  # If a key is pressed
                if event.key == pygame.K_LEFT:  # If it is left arrow, we move left
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):  # If position is not valid
                        current_piece.x += 1

                if event.key == pygame.K_RIGHT:  # If it is right arrow, we move right
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):  # If position is not valid
                        current_piece.x -= 1

                if event.key == pygame.K_DOWN:  # if it is down arrow, we move down
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):  # If position is not valid
                        current_piece.y -= 1

                if event.key == pygame.K_UP:  # if it is up arrow, we rotate piece
                    current_piece.rotation += 1
                    if not valid_space(current_piece, grid):  # If rotation is not valid
                        current_piece.rotation -= 1

        shape_pos = convert_shape_format(current_piece)
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:  # If shape is within the screen
                grid[y][x] = current_piece.color  # Then change color of that block

        if change_piece:  # Time to change piece
            for pos in shape_pos:  # Then add position to locked positions
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece  # Move to next piece
            next_piece = get_shape()  # Get a new next piece
            change_piece = False  # Set change piece to False
            score += clear_rows(grid, locked_positions)*10  # Clear rows if any full, adds score
            update_score(score)  # Update high score

        draw_window(window, grid, score)  # Draw main window
        draw_next_shape(next_piece, window)  # Draw next shape
        pygame.display.update()  # Update display

        if check_lost(locked_positions):  # if we lost, stop program
            draw_text_middle("YOU LOST!", 80, (255, 255, 255), window)
            pygame.display.update()  # Update screen
            pygame.time.delay(2000)  # Wait for a while before exiting game
            run = False
            update_score(score)  # Update high score

    return close


def main_menu(window):
    run = True
    while run:
        window.fill((150, 150, 150))
        draw_text_middle("PRESS ANY KEY TO PLAY", 60, (255, 255, 255), window)
        pygame.display.update()  # Update window

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If 'x' button is pressed
                run = False
            if event.type == pygame.KEYDOWN:  # If any key is pressed we play game
                close = main(window)
                if close:  # If we closed game in main() function
                    run = False
                break

    pygame.display.quit()


window = pygame.display.set_mode((s_width, s_height))  # Create main window of game
pygame.display.set_caption('Tetris')  # Name the main window
main_menu(window)  # start game
