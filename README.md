# Maze solver yo
Maze solver by Shibo Yao, Mike Chen, and Jeff Zhu

## Dependencies
pip install pillow

## Usage

maze_solver.py [-h] fname runmode

positional arguments:  
* fname -- Input maze  
* runmode -- Determine which algorithm to solve the maze: "dfs", "bfs", "greedy", "a\*", "a\*1.2.1", "a\*1.2.2", "a\*1.2.3", "a\*1.2.4", "a\*ghost", or "a\*ghost_mov", or "all"

optional arguments:
  -h, --help  show this help message and exit

## Animations
To create the mp4 files, get ffmpeg and run maze_solver.py with runmode a*ghost_mov
```
.\ffmpeg.exe -f image2 -r 10 -i .\res\solutions\smallGhostSol%d.png -vcodec mpeg4 -y .\smallGhostSol.mp4
.\ffmpeg.exe -f image2 -r 10 -i .\res\solutions\mediumGhostSol%d.png -vcodec mpeg4 -y .\mediumGhostSol.mp4
.\ffmpeg.exe -f image2 -r 10 -i .\res\solutions\bigGhostSol%d.png -vcodec mpeg4 -y .\bigGhostSol.mp4
```
