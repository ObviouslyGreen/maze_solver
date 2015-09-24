import argparse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MazeSolver():

    def __init__(self, fname, runmode):
        self.fname = fname
        self.runmode = runmode
        self.maze = []
        self.start = None
        self.dest = None
        try:
            with open(fname) as f:
                for line in f:
                    print(line)
                    self.maze.append(line)

                    if not self.start:
                        start_index = line.find('P')
                        if start_index != -1:
                            self.start = (len(self.maze) - 1, start_index)

                    if not self.dest:
                        dest_index = line.find('.')
                        if dest_index != -1:
                            self.dest = (len(self.maze) - 1, dest_index)
        except:
            pass

    def __write_sol(self, solved_maze, fname):
        try:
            with open(fname, 'w+') as f:
                for line in solved_maze:
                    f.write(line)
        except:
            pass

    def _dfs(self):
        logger.info('Running depth-first search on maze')

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
            print(line[:-1])


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