import argparse
import logging
import math

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
        self.ghoststart = None
        self.ghost = []
        try:
            with open(fname) as f:
                for idx, line in enumerate(f):
                    self.maze.append(line)
                    self.maze_flags.append([])

                    for cnt, char in enumerate(line):
                        if char == '%':
                            self.maze_flags[idx].append({'type': 'wall'})
                        elif char == ' ':
                            self.maze_flags[idx].append({'type': 'unmarked', 'N': False, 'E': False, 'S': False, 'W': False})
                        elif char == 'P':
                            self.maze_flags[idx].append({'type': 'start', 'N': False, 'E': False, 'S': False, 'W': False})
                            self.start = (idx, cnt)
                        elif char == '.':
                            self.maze_flags[idx].append({'type': 'dest', 'N': False, 'E': False, 'S': False, 'W': False})
                            self.dest = (idx, cnt)
                        elif char == 'G':
                            self.ghoststart = (idx,cnt)
                            self.ghost.append('ghost')
                        elif char == 'g':
                            self.ghost.append('ghost')

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

    def __manhat_dist(self, row, col, case = 0):
        if case == 0 or case == 1:
            dist = abs(self.dest[0] - row) + abs(self.dest[1] - col)
        elif case == 2:
            dist = (abs(self.dest[0] - row) + abs(self.dest[1] - col)) * 1.5
        elif case == 3:
            dist = (abs(self.dest[0] - row) + abs(self.dest[1] - col))
            max_dist = len(self.maze[0]) + len(self.maze[0][0])
            if dist < max_dist:
                dist *= 1.1

        return dist

    def __dfs(self, row, col, maze, maze_flags):
        try:
            if maze_flags[row][col]['type'] == 'wall':
                return False
        except IndexError:
            return False

        if maze_flags[row][col]['type'] == 'marked':
            return False

        if maze_flags[row][col]['type'] == 'dest':
            return True

        up = (row - 1, col)
        down = (row + 1, col)
        left = (row, col - 1)
        right = (row, col + 1)

        maze_flags[row][col]['type'] = 'marked'
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

    def __bfs(self, row, col, maze, maze_flags):
        q = queue.Queue()

        q.put(([],row,col))
        maze_flags[row][col]['type'] = 'marked'
        pathsol = []
        while(q.empty() == False):
            path, r, c = q.get()
            if(maze_flags[r][c]['type'] == 'dest'):
                pathsol = path
                break

            if(maze_flags[r-1][c]['type'] == 'unmarked' or maze_flags[r-1][c]['type'] == 'dest'):
                if(maze_flags[r-1][c]['type'] != 'dest'): maze_flags[r-1][c]['type'] = 'marked'
                q.put((path + [(r-1,c)],r-1,c))
            if(maze_flags[r+1][c]['type'] == 'unmarked' or maze_flags[r+1][c]['type'] == 'dest'):
                if(maze_flags[r+1][c]['type'] != 'dest'): maze_flags[r+1][c]['type'] = 'marked'
                q.put((path + [(r+1,c)],r+1,c))
            if(maze_flags[r][c-1]['type'] == 'unmarked' or maze_flags[r][c-1]['type'] == 'dest'):
                if(maze_flags[r][c-1]['type'] != 'dest'): maze_flags[r][c-1]['type'] = 'marked'
                q.put((path + [(r,c-1)],r,c-1))
            if(maze_flags[r][c+1]['type'] == 'unmarked' or maze_flags[r][c+1]['type'] == 'dest'):
                if(maze_flags[r][c+1]['type'] != 'dest'): maze_flags[r][c+1]['type'] = 'marked'
                q.put((path + [(r,c+1)], r,c+1))

        for item in pathsol:
            list_maze_row = list(maze[item[0]])
            list_maze_row[item[1]] = '.'
            maze[item[0]] = ''.join(list_maze_row)

    def __greedy(self, row, col, maze, maze_flags):
        pq = queue.PriorityQueue()

        pq.put((self.__manhat_dist(row, col),[],row,col))
        maze_flags[row][col]['type'] = 'marked'
        pathsol = []

        while(pq.empty() == False):
            _, path, r, c = pq.get()
            if(maze_flags[r][c]['type'] == 'dest'):
                pathsol = path
                break

            if(maze_flags[r-1][c]['type'] == 'unmarked' or maze_flags[r-1][c]['type'] == 'dest'):
                if(maze_flags[r-1][c]['type'] != 'dest'): maze_flags[r-1][c]['type'] = 'marked'
                pq.put((self.__manhat_dist(r-1,c),path + [(r-1,c)],r-1,c))

            if(maze_flags[r+1][c]['type'] == 'unmarked' or maze_flags[r+1][c]['type'] == 'dest'):
                if(maze_flags[r+1][c]['type'] != 'dest'):maze_flags[r+1][c]['type'] = 'marked'
                pq.put((self.__manhat_dist(r+1,c),path + [(r+1,c)],r+1,c))

            if(maze_flags[r][c-1]['type'] == 'unmarked' or maze_flags[r][c-1]['type'] == 'dest'):
                if(maze_flags[r][c-1]['type'] != 'dest'):maze_flags[r][c-1]['type'] = 'marked'
                pq.put((self.__manhat_dist(r,c-1),path + [(r,c-1)],r,c-1))

            if(maze_flags[r][c+1]['type'] == 'unmarked' or maze_flags[r][c+1]['type'] == 'dest'):
                if(maze_flags[r][c+1]['type'] != 'dest'):maze_flags[r][c+1]['type'] = 'marked'
                pq.put((self.__manhat_dist(r,c+1),path + [(r,c+1)],r,c+1))

        for item in pathsol:
            list_maze_row = list(maze[item[0]])
            list_maze_row[item[1]] = '.'
            maze[item[0]] = ''.join(list_maze_row)

    def __a_search(self, row, col, maze, maze_flags):
        q = queue.PriorityQueue()

        q.put((self.__manhat_dist(row, col), 0, [], row, col))
        maze_flags[row][col]['type'] = 'marked'
        pathsol = []
        while(q.empty() == False):
            _, cost, path, r, c = q.get()
            if(maze_flags[r][c]['type'] == 'dest'):
                pathsol = path
                break

            if(maze_flags[r-1][c]['type'] == 'unmarked' or maze_flags[r-1][c]['type'] == 'dest'):
                if(maze_flags[r-1][c]['type'] != 'dest'): maze_flags[r-1][c]['type'] = 'marked'
                q.put((cost + self.__manhat_dist(r-1, c), cost + 1, path + [(r-1,c)],r-1,c))
            if(maze_flags[r+1][c]['type'] == 'unmarked' or maze_flags[r+1][c]['type'] == 'dest'):
                if(maze_flags[r+1][c]['type'] != 'dest'):maze_flags[r+1][c]['type'] = 'marked'
                q.put((cost + self.__manhat_dist(r+1, c), cost + 1, path + [(r+1,c)],r+1,c))
            if(maze_flags[r][c-1]['type'] == 'unmarked' or maze_flags[r][c-1]['type'] == 'dest'):
                if(maze_flags[r][c-1]['type'] != 'dest'):maze_flags[r][c-1]['type'] = 'marked'
                q.put((cost + self.__manhat_dist(r, c-1), cost + 1, path + [(r,c-1)],r,c-1))
            if(maze_flags[r][c+1]['type'] == 'unmarked' or maze_flags[r][c+1]['type'] == 'dest'):
                if(maze_flags[r][c+1]['type'] != 'dest'):maze_flags[r][c+1]['type'] = 'marked'
                q.put((cost + self.__manhat_dist(r, c-1), cost + 1, path + [(r,c+1)], r,c+1))

        for item in pathsol:
            list_maze_row = list(maze[item[0]])
            list_maze_row[item[1]] = '.'
            maze[item[0]] = ''.join(list_maze_row)

    def __penalized_a_search(self, row, col, maze, case, maze_flags):
        q = queue.PriorityQueue()

        if(case == 0 or case == 2):
            turn = 1
            forward = 2
        elif(case == 1 or case == 3):
            turn = 2
            forward = 1

        q.put((self.__manhat_dist(row, col, case), 0, 'E', [], row, col))
        maze_flags[row][col]['type'] = 'marked'
        pathsol = []

        while(q.empty() == False):
            _, cost, direction, path, r, c = q.get()
            if(maze_flags[r][c]['type'] == 'dest'):
                pathsol = path
                break

            if(direction == 'N'):
                fr = r - 1
                fc = c
                right = 'E'
                left = 'W'
            elif(direction == 'E'):
                fr = r
                fc = c + 1
                right = 'S'
                left = 'N'
            elif(direction == 'S'):
                fr = r + 1
                fc = c
                right = 'W'
                left = 'E'
            else:
                fr = r
                fc = c - 1
                right = 'N'
                left = 'S'

            if(maze_flags[fr][fc]['type'] == 'unmarked' or maze_flags[fr][fc]['type'] == 'dest'):
                if(maze_flags[fr][fc]['type'] != 'dest'): maze_flags[fr][fc]['type'] = 'marked'
                q.put((cost + forward + self.__manhat_dist(fr, fc, case), cost + forward, direction, path + [(fr, fc)], fr, fc))

            if(maze_flags[r][c][right] == False):
                q.put((cost + turn + self.__manhat_dist(r, c, case), cost + turn, right, path, r, c))
                maze_flags[r][c][right] = True

            if(maze_flags[r][c][left] == False):
                q.put((cost + turn + self.__manhat_dist(r, c, case), cost + turn, left, path, r, c))
                maze_flags[r][c][left] = True

        for item in pathsol:
            list_maze_row = list(maze[item[0]])
            list_maze_row[item[1]] = '.'
            maze[item[0]] = ''.join(list_maze_row)

        return cost

    def __a_ghost(self, row, col, maze, maze_flags):
        q = queue.PriorityQueue()

        q.put((self.__manhat_dist(row, col), 0, [], row, col))
        maze_flags[row][col]['type'] = 'marked'
        pathsol = []
        while(q.empty() == False):
            _, cost, path, r, c = q.get()
            if(maze_flags[r][c]['type'] == 'dest'):
                pathsol = path
                break

            if(maze_flags[r-1][c]['type'] == 'unmarked' or maze_flags[r-1][c]['type'] == 'dest'):
                if(maze_flags[r-1][c]['type'] != 'dest'): maze_flags[r-1][c]['type'] = 'marked'
                q.put((cost + self.__manhat_dist(r-1, c), cost + 1, path + [(r-1,c)],r-1,c))
            if(maze_flags[r+1][c]['type'] == 'unmarked' or maze_flags[r+1][c]['type'] == 'dest'):
                if(maze_flags[r+1][c]['type'] != 'dest'):maze_flags[r+1][c]['type'] = 'marked'
                q.put((cost + self.__manhat_dist(r+1, c), cost + 1, path + [(r+1,c)],r+1,c))
            if(maze_flags[r][c-1]['type'] == 'unmarked' or maze_flags[r][c-1]['type'] == 'dest'):
                if(maze_flags[r][c-1]['type'] != 'dest'):maze_flags[r][c-1]['type'] = 'marked'
                q.put((cost + self.__manhat_dist(r, c-1), cost + 1, path + [(r,c-1)],r,c-1))
            if(maze_flags[r][c+1]['type'] == 'unmarked' or maze_flags[r][c+1]['type'] == 'dest'):
                if(maze_flags[r][c+1]['type'] != 'dest'):maze_flags[r][c+1]['type'] = 'marked'
                q.put((cost + self.__manhat_dist(r, c-1), cost + 1, path + [(r,c+1)], r,c+1))

        return pathsol #ghost things

    def _dfs(self):
        logger.info('Running depth-first search on maze')

        maze = self.maze
        maze_flags = self.maze_flags
        self.__dfs(self.start[0], self.start[1], maze, maze_flags)
        self.print_maze(maze)
        num_nodes = 0
        for row in maze_flags:
            for col in row:
                if col['type'] == 'marked':
                    num_nodes += 1
        logger.info('{0} nodes visited'.format(num_nodes))
        logger.info('cost: {0}'.format(sum(x.count('.') for x in
                    maze)))


    def _bfs(self):
        logger.info('Running breadth-first search on maze')

        maze = self.maze
        maze_flags = self.maze_flags
        self.__bfs(self.start[0], self.start[1], maze, maze_flags)
        self.print_maze(maze)
        num_nodes = 0
        for row in maze_flags:
            for col in row:
                if col['type'] == 'marked':
                    num_nodes += 1
        logger.info('{0} nodes visited'.format(num_nodes))
        logger.info('cost: {0}'.format(sum(x.count('.') for x in
                    maze)))

    def _greedy(self):
        logger.info('Running greedy best-first search on maze')

        maze = self.maze
        maze_flags = self.maze_flags
        self.__greedy(self.start[0], self.start[1], maze, maze_flags)
        self.print_maze(maze)
        num_nodes = 0
        for row in maze_flags:
            for col in row:
                if col['type'] == 'marked':
                    num_nodes += 1
        logger.info('{0} nodes visited'.format(num_nodes))
        logger.info('cost: {0}'.format(sum(x.count('.') for x in
                    maze)))

    def _a_search(self):
        logger.info('Running A* search on maze')

        maze = self.maze
        maze_flags = self.maze_flags
        self.__a_search(self.start[0], self.start[1], maze, maze_flags)
        self.print_maze(maze)
        num_nodes = 0
        for row in maze_flags:
            for col in row:
                if col['type'] == 'marked':
                    num_nodes += 1
        logger.info('{0} nodes visited'.format(num_nodes))
        logger.info('cost: {0}'.format(sum(x.count('.') for x in
                    maze)))

    def _penalized_a_search(self, case):
        logger.info('Running A* search on maze')

        maze = self.maze
        maze_flags = self.maze_flags
        cost = self.__penalized_a_search(self.start[0], self.start[1], maze, case, maze_flags)
        self.print_maze(maze)
        num_nodes = 0
        for row in maze_flags:
            for col in row:
                if col['type'] == 'marked':
                    num_nodes += 1
        logger.info('{0} nodes visited'.format(num_nodes))
        logger.info('cost: {0}'.format(cost))

    def solve(self):
        if self.runmode == 'dfs':
            self._dfs()
        elif self.runmode == 'bfs':
            self._bfs()
        elif self.runmode == 'greedy':
            self._greedy()
        elif self.runmode == 'a*':
            self._a_search()
        elif self.runmode == 'a*1.2.1':
            self._penalized_a_search(0)
        elif self.runmode == 'a*1.2.2':
            self._penalized_a_search(1)
        elif self.runmode == 'a*1.2.3':
            self._penalized_a_search(2)
        elif self.runmode == 'a*1.2.4':
            self._penalized_a_search(3)
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
                                           "a*", 'a*1.2.1', 'a*1.2.2',
                                           'a*1.2.3', 'a*1.2.4'or "all"''')
    args = parser.parse_args()

    maze_solver = MazeSolver(args.fname, args.runmode)
    maze_solver.solve()


if __name__ == '__main__':
    main()