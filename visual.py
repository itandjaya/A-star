## visual.py

import pygame;
from grid import Grid, MazeValue;
from random import random;


# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0);
BLUE = (0, 0, 255);
YELLOW  =   (255, 255, 0);
 
# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 10;
HEIGHT = 10;

# This sets the margin between each cell
MARGIN = 1;

ROWS    =   90;
COLS    =   90;


# Set the HEIGHT and WIDTH of the screen
#WINDOW_SIZE =   (255, 255);
WINDOW_SIZE = (1000, 1000);
FPS         =   60;

def path_iterator(  paths):

    for p in paths: yield p;
    return;

def path_found( steps):

    font = pygame.font.Font('freesansbold.ttf', 32); 
    text = font.render('PATH FOUND: {} STEPS'.format(steps), True, GREEN, BLUE); 
    textRect = text.get_rect();
    textRect.center = (1000 // 2, 35);

    return text, textRect;


def no_path_found():

    font = pygame.font.Font('freesansbold.ttf', 32); 
    text = font.render('NO PATH FOUND', True, GREEN, BLUE); 
    textRect = text.get_rect();
    textRect.center = (1000 // 2, 1000 // 2);

    return text, textRect;

def maze_visual():

    # Initialize pygame
    pygame.init();

    ## Initialize and set the screen.
    screen = pygame.display.set_mode(WINDOW_SIZE);

    # Set title of screen
    pygame.display.set_caption("PATH FINDER");
    
    # Loop until the user clicks the close button.
    is_done = False;
    min_dist    =   0;
    
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock();
    
    ## Initial Maze.
    maze    =   [ [0] * COLS for _ in range(ROWS)];
    for y in range(ROWS):
        for x in range(COLS):
            if  random() < 0.45: # or \
                #(10 < x < COLS and y == ROWS-15) or \
                #(x==20 and 5 < y < ROWS-10):                 
                maze[y][x] = 1;

    g       =   Grid(   maze = maze, start = (0,0));

    iter_path_finder    =   g.path_finder();
    px, py  =   g.start;


    screen.fill(    BLACK);

    for y in range(ROWS):

        for x in range(COLS):
            value   =   g.maze[y][x];
            
            if value == MazeValue.EMPTY.value:      color   =   WHITE;
            elif value == MazeValue.WALL.value:     color   =   BLACK;
            elif value == MazeValue.START.value:    color   =   RED;
            elif value == MazeValue.END.value:      color   =   BLUE;
            else:
                color = (255,50,50);
            
            pygame.draw.rect(   screen,
                                color,
                                [   (MARGIN + WIDTH) * x + MARGIN,
                                    (MARGIN + HEIGHT) * y + MARGIN,
                                    WIDTH,
                                        HEIGHT]);

    # -------- Main Program Loop -----------
    while not is_done:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:    is_done = True;

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my  =   pygame.mouse.get_pos();
                pos     =   (mx, my);
                # Change the x/y screen coordinates to grid coordinates
                my = my // (WIDTH + MARGIN)
                mx = mx // (HEIGHT + MARGIN)
                # Set that location to one
                #grid[my][mx] *= -1
                print("Click ", pos, "Grid coordinates: ", my, mx);

        prev_x, prev_y  =   px, py;
        px, py          =   next(iter_path_finder);
        
        if type(px) == list:
            curr_paths  =   path_iterator(px[1:-1]);
            res         =   py;
            is_done     =   True;
  

        else:

            if (px, py) != g.start and (px, py) != g.end:
                pygame.draw.rect(   screen,
                                    RED,
                                    [   (MARGIN + WIDTH) * px + MARGIN,
                                        (MARGIN + HEIGHT) * py + MARGIN,
                                        WIDTH,
                                        HEIGHT]);

                
            if (prev_x, prev_y) != g.start and (prev_x, prev_y) != g.end:
                pygame.draw.rect(   screen,
                                    YELLOW,
                                    [   (MARGIN + WIDTH) * prev_x + MARGIN,
                                        (MARGIN + HEIGHT) * prev_y + MARGIN,
                                        WIDTH,
                                        HEIGHT]);


            
        clock.tick( FPS);
        pygame.display.update();
    

    is_done =   False;
    no_path_text, no_path_rect  =   no_path_found();
    path_text, path_rect        =   path_found(res);

    while not is_done:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:    is_done = True;

        if res != -1:

            try:        
                x,y =   next(curr_paths);
                pygame.draw.rect(   screen,
                                    GREEN,
                                    [   (MARGIN + WIDTH) * x + MARGIN,
                                        (MARGIN + HEIGHT) * y + MARGIN,
                                        WIDTH,
                                        HEIGHT]);
                clock.tick(FPS//2+1);

            except StopIteration:
                screen.blit(path_text, path_rect);
                clock.tick(2);
            
            

        else:

            screen.blit(no_path_text, no_path_rect);
            clock.tick(2);

        pygame.display.update();
            
        
    
    pygame.quit();

    return;