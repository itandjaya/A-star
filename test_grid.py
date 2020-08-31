## test_grid.py


from grid import Grid;

def main():

    maze    =   [   [0, 0,  0,  0,  0,  0],
                    [1, 1,  1,  1,  1,  0],
                    [0, 0,  0,  0,  0,  0],
                    [0, 1,  1,  1,  1,  1],
                    [0, 1,  0,  0,  0,  0],
                    [0, 0,  0,  1,  1,  0],
                ];
    #maze    =   [ [0]* 8 for _ in range(8)]; 
    g = Grid(   maze = maze, start = (0,0), end = None);

    for res in g.path_finder(): pass;

    print(res[1]);
    return 0;

    g = Grid(   maze = maze, start = (2,4), end = (5,5));
    print(g.maze);

    print(g.path_finder());

    return 0;

main()      if __name__ == '__main__'       else None;