import argparse
import logging

# For python 2 and 3 compatibility
try:
    import queue
except ImportError:
    import Queue as queue

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MazeSolver():

    def __init__(self, fname, runmode):
        self.fname = fname
        self.runmode = runmode
        self.maze = []
        self.maze_flags = []
        self.start = None
        self.dest = None
        try:
            with open(fname) as f:
                for idx, line in enumerate(f):
                    self.maze.append(line)
                    self.maze_flags.append([])

                    for cnt, char in enumerate(line):
                        if char == '%':
                            self.maze_flags[idx].append('wall')
                        elif char == ' ':
                            self.maze_flags[idx].append('unmarked')
                        elif char == 'P':
                            self.maze_flags[idx].append('start')
                            self.start = (idx, cnt)
                        elif char == '.':
                            self.maze_flags[idx].append('dest')
                            self.dest = (idx, cnt)

        except Exception as e:
            print(e)

    def __get_val(self, array, coords):
        return array[coords[0]][coords[1]]

    def __write_sol(self, solved_maze, fname):
        try:
            with open(fname, 'w+') as f:
                for line in solved_maze:
                    f.write(line)
        except:
            pass

    def __dfs(self, row, col, maze, maze_flags):
        try:
            if maze_flags[row][col] == 'wall':
                return False
        except IndexError:
            return False

        if maze_flags[row][col] == 'marked':
            return False

        if maze_flags[row][col] == 'dest':
            return True

        up = (row - 1, col)
        down = (row + 1, col)
        left = (row, col - 1)
        right = (row, col + 1)

        maze_flags[row][col] = 'marked'
        if (row, col) != self.start:
            list_maze_row = list(maze[row])
            list_maze_row[col] = '.'
            maze[row] = ''.join(list_maze_row)

        if (self.__dfs(up[0], up[1], maze, maze_flags) or
            self.__dfs(down[0], down[1], maze, maze_flags) or
            self.__dfs(left[0], left[1], maze, maze_flags) or
            self.__dfs(right[0], right[1], maze, maze_flags)):
            return True


        if (row, col) != self.start:
            list_maze_row = list(maze[row])
            list_maze_row[col] = ' '
            maze[row] = ''.join(list_maze_row)
        return False


    def _dfs(self):
        logger.info('Running depth-first search on maze')

        maze = self.maze
        maze_flags = self.maze_flags
        self.__dfs(self.start[0], self.start[1], maze, maze_flags)
        self.print_maze(maze)
        logger.info('{0} nodes visited'.format(sum(x.count('marked') for x in
                    maze_flags)))


    def _bfs(self):
        logger.info('Running breadth-first search on maze')

    def _greedy(self):
        logger.info('Running greedy best-first search on maze')

    def _a_search(self):
        logger.info('Running A* search on maze')

    def solve(self):
        if self.runmode == 'dfs':
            self._dfs()
        elif self.runmode == 'bfs':
            self._bfs()
        elif self.runmode == 'greedy':
            self._greedy()
        elif self.runmode == 'a*':
            self._a_search()
        elif self.runmode == 'all':
            self._dfs()
            self._bfs()
            self._greedy()
            self._a_search()
        else:
            logging.error('Invalid runmode!')

    def print_maze(self, solved_maze):
        for line in solved_maze:
            print(line.strip('\n'))


def main():
    parser = argparse.ArgumentParser(description='''Maze solver for CS 440 by
                                                    Shibo Yao, Mike Chen,
                                                    and Jeff Zhu''')
    parser.add_argument('fname', help='Input maze')
    parser.add_argument('runmode', help='''Determine which algorithm to solve
                                           the maze: "dfs", "bfs", "greedy",
                                           "a*", or "all"''')
    args = parser.parse_args()

    maze_solver = MazeSolver(args.fname, args.runmode)
    maze_solver.solve()


if __name__ == '__main__':
    main()