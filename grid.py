## grid.py
## grid class:
##  -. 2D grid/maze.
##  -. Starting coord.
##  -. End coord.
##  -. A* method as minimum path finder from start to end coordinates.

from enum import Enum;
from heapq import heapify, heappush, heappop, heappushpop;

DEBUG   =   0;          ## Global variable used for debugging purposes.
DIAGONALS_ALLOWED   =   1;

class MazeValue(Enum):
    ## Maze description:

    EMPTY   =   0;
    WALL    =   1;
    START   =   2;
    END     =   3;
    


class Grid( object):

    def __init__(   self, maze  =   [], start   =   (0,0), end  =   None):

        ## Maze description:
        ##      0: walkable-space,
        ##      1: Wall/obstacle,
        ##      2: starting coord.
        ##      3: end/finish coord.       

        if not maze or not maze[0]:     return;


        self.maze   =   maze;
        self.max_row, self.max_col  =   len(maze), len(maze[0]);

        self.start  =   start;
        self.end    =   end;

        if end == None:     
            self.end    =     ( self.max_col-1, self.max_row-1);
            self.maze[-1][-1]   =   3;
        
        self.set_start_coord(   self.start);
        self.set_end_coord(     self.end);

        return;

    def set_start_coord(    self, coord):
        self.start  =   coord;
        self.maze[coord[1]][coord[0]]   =   MazeValue.START.value;
        return;

    def set_end_coord(  self, coord):
        self.end    =   coord;
        self.maze[coord[1]][coord[0]]   =   MazeValue.END.value;
        return;

    def heuristic_dist( self, curr_coord    =   (0,0)):
        x0, y0  =   curr_coord;
        x1, y1  =   self.end;
        dist_sq =   (x1-x0)**2 + (y1-y0)**2;
        return dist_sq**0.5;

    def neighbors_coords(   self, coord, visited):
        x,y =   coord;
        neighbors   =   set();

        top         =   (x, max(0, y-1));
        left        =   (max(0, x-1), y);
        right       =   (min(self.max_col-1, x+1), y);
        bottom      =   (x, min(self.max_row-1, y+1));

        if top not in visited:      neighbors.add(  top);
        if left not in visited:     neighbors.add(  left);
        if right not in visited:    neighbors.add(  right);
        if bottom not in visited:   neighbors.add(  bottom);

        if DIAGONALS_ALLOWED:
            top_left    =   (max(0, x-1),               max(0, y-1));
            top_right   =   (min(self.max_col-1, x+1),  max(0, y-1));
            bottom_left =   (min(self.max_col-1, x+1),  min(self.max_row-1, y+1));
            bottom_right=   (max(0, x-1),               min(self.max_row-1, y+1));

            if top_left not in visited:     neighbors.add(  top_left);
            if top_right not in visited:    neighbors.add(  top_right);
            if bottom_left not in visited:  neighbors.add(  bottom_left);
            if bottom_right not in visited: neighbors.add(  bottom_right);
        
        return neighbors;


    def path_finder(    self):

        visited =   set();
        
        # (heu_dist + steps, steps, x, y, paths_history);
        x, y            =   (self.start[0], self.start[1]);
        to_be_visited   =   [   (0, 0, x, y, [(x,y)])];  
        
        while to_be_visited:

            weight, steps, x, y, curr_paths =   heappop(to_be_visited);

            if (x,y) in visited:    continue;

            visited.add(    (x,y));
            yield (x,y);

            if (x,y)    ==  self.end:       break;
            
            neighbors   =   self.neighbors_coords(  (x,y), visited);

            for nx, ny in neighbors:

                weight  =   (steps + 1) +   self.heuristic_dist(    (x,y));

                if self.maze[ny][nx] != MazeValue.WALL.value:
                    heappush(   to_be_visited, (weight, steps+1, nx, ny, curr_paths + [(nx, ny)]));

        yield (-1, -1);

        res =   steps    if (x,y)    ==  self.end        else -1;
        yield curr_paths, res;
        return ;
        






