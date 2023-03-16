# 🔍 A* Pathfinding Visualizer

<img src="https://user-images.githubusercontent.com/45187177/225208243-057b478e-7a06-4b1d-82d9-19c04f031db7.png" alt="A* Pathfinding Visualizer Banner" width="1015"/>

An interactive visualization of the A* search algorithm using a PyGame interface. Aside from the A* algorithm, Prim's algorithm was also implemented in order to generate randomized, but traversable, mazes.

![python](https://img.shields.io/badge/Python-3.11-blue.svg)

## ⚙️ Requirements

[Install python](https://www.python.org/downloads/) and the required libraries (must have [pip](https://packaging.python.org/en/latest/tutorials/installing-packages/) installed):
```
pip install pygame
```

## 🖥️ Running the Program

* Download the ```astar_visualizer.py``` and the ```maze_generator.py``` files to the **same directory.**

* **Run the A\* Visualizer python file** (command line method below):
> Ensure that you are in the directory of the astar_visualizer.py file or replace "astar_visualizer.py" with the file's path, e.g. "/Users/rawsab/Desktop/astar_visualizer.py"
```
python astar_visualizer.py
```

## 📝 Instructions
* Click on a cell to place the starting point and click another cell to place the end point. Right click to remove either of the points.
* After placing the start and end points, click cells and drag to create obstacles/barriers. Right click them to remove.
* Press ```M``` to generate a randomized maze.
* Press ```Space``` to run the A* pathfinding visualizer. *Make sure that the start and end points are set!*
* Press ```Return``` to reset the grid.

<p align="center">
<img src="https://user-images.githubusercontent.com/45187177/225208462-2e74a9a5-c997-4a05-ad17-0ec4ce6c9964.png" alt="Screenshot of Program" width="650"/>
</p>
