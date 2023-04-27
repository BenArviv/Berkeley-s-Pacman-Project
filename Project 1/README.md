## Project 1: Search

### Question 1: Finding a Fixed Food Dot using Depth First Search
In `searchAgents.py`, you’ll find a fully implemented _SearchAgent_, which plans out a path through Pacman’s world and then executes that path step-by-step. The search algorithms for formulating a plan are not implemented – that’s your job.

First, test that the _SearchAgent_ is working correctly by running:
```
python pacman.py -l tinyMaze -p SearchAgent -a fn=tinyMazeSearch
```
The command above tells the _SearchAgent_ to use _tinyMazeSearch_ as its search algorithm, which is implemented in `search.py`. Pacman should navigate the maze successfully.

Your code should quickly find a solution for:
```
python pacman.py -l tinyMaze -p SearchAgent
```
```
python pacman.py -l mediumMaze -p SearchAgent
```
```
python pacman.py -l bigMaze -z .5 -p SearchAgent
```
The Pacman board will show an overlay of the states explored, and the order in which they were explored (brighter red means earlier exploration).

### Question 2: Breadth First Search
Test your code the same way you did for depth-first search.
```
python pacman.py -l mediumMaze -p SearchAgent -a fn=bfs
```
```
python pacman.py -l bigMaze -p SearchAgent -a fn=bfs -z .5
```
 If Pacman moves too slowly for you, try the option `--frameTime 0`.
 
 Your code should work equally well for the eight-puzzle search problem without any changes.
 ```
 python eightpuzzle.py
 ```
 
 ### Question 3: Varying the Cost Function
 While BFS will find a fewest-actions path to the goal, we might want to find paths that are “best” in other senses. Consider _mediumDottedMaze_ and _mediumScaryMaze_.
 
 By changing the cost function, we can encourage Pacman to find different paths. For example, we can charge more for dangerous steps in ghost-ridden areas or less for steps in food-rich areas, and a rational Pacman agent should adjust its behavior in response.
 
 You should now observe successful behavior in all three of the following layouts, where the agents below are all UCS agents that differ only in the cost function they use (the agents and cost functions are written for you):
 ```
 python pacman.py -l mediumMaze -p SearchAgent -a fn=ucs
 ```
 ```
 python pacman.py -l mediumDottedMaze -p StayEastSearchAgent
 ```
 ```
 python pacman.py -l mediumScaryMaze -p StayWestSearchAgent
 ```
 Note: You should get very low and very high path costs for the _StayEastSearchAgent_ and _StayWestSearchAgent_ respectively, due to their exponential cost functions (see `searchAgents.py` for details).
 
 ### Question 4: A* search
 A* takes a heuristic function as an argument. Heuristics take two arguments: a state in the search problem (the main argument), and the problem itself (for reference information). The _nullHeuristic_ heuristic function in `search.py` is a trivial example.
 
 You can test your A* implementation on the original problem of finding a path through a maze to a fixed position using the Manhattan distance heuristic (implemented already as _manhattanHeuristic_ in `searchAgents.py`).
 ```
 python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic
 ```
 You should see that A* finds the optimal solution slightly faster than uniform cost search (about 549 vs. 620 search nodes expanded in our implementation, but ties in priority may make your numbers differ slightly).
 
 ### Question 5: Finding All the Corners
 The real power of A* will only be apparent with a more challenging search problem. Now, it’s time to formulate a new problem and design a heuristic for it.
 
 In corner mazes, there are four dots, one in each corner. Our new search problem is to find the shortest path through the maze that touches all four corners (whether the maze actually has food there or not). Note that for some mazes like _tinyCorners_, the shortest path does not always go to the closest food first! Hint: the shortest path through _tinyCorners_ takes 28 steps.
 
 Now, your search agent should solve:
 ```
 python pacman.py -l tinyCorners -p SearchAgent -a fn=bfs,prob=CornersProblem
 ```
 ```
 python pacman.py -l mediumCorners -p SearchAgent -a fn=bfs,prob=CornersProblem
 ```
 Our implementation of _breadthFirstSearch_ expands just under 2000 search nodes on _mediumCorners_. However, heuristics (used with A* search) can reduce the amount of searching required. 
 
 ### Question 6: Corners Problem: Heuristic
 Implement a non-trivial, consistent heuristic for the _CornersProblem_ in _cornersHeuristic_.
 ```
 python pacman.py -l mediumCorners -p AStarCornersAgent -z 0.5
 ```
 Note: _AStarCornersAgent_ is a shortcut for
 ```
 -p SearchAgent -a fn=aStarSearch,prob=CornersProblem,heuristic=cornersHeuristic
 ```
 
 ### Question 7: Eating All The Dots
 Now we’ll solve a hard search problem: eating all the Pacman food in as few steps as possible. For this, we’ll need a new search problem definition which formalizes the food-clearing problem: _FoodSearchProblem_ in `searchAgents.py` (implemented for you). A solution is defined to be a path that collects all of the food in the Pacman world. For the present project, solutions do not take into account any ghosts or power pellets; solutions only depend on the placement of walls, regular food and Pacman. (Of course ghosts can ruin the execution of a solution! We’ll get to that in the next project.) If you have written your general search methods correctly, A* with a null heuristic (equivalent to uniform-cost search) should quickly find an optimal solution to _testSearch_ with no code change on your part (total cost of 7).
 ```
 python pacman.py -l testSearch -p AStarFoodSearchAgent
 ```
 Note: _AStarFoodSearchAgent_ is a shortcut for
 ```
 -p SearchAgent -a fn=astar,prob=FoodSearchProblem,heuristic=foodHeuristic
 ```
 You should find that UCS starts to slow down even for the seemingly simple _tinySearch_. As a reference, our implementation takes 2.5 seconds to find a path of length 27 after expanding 5057 search nodes.
 
 Try your agent on the _trickySearch_ board:
 ```
 python pacman.py -l trickySearch -p AStarFoodSearchAgent
 ```
 Our UCS agent finds the optimal solution in about 13 seconds, exploring over 16,000 nodes.
 
 ### Question 8: Suboptimal Search
 Sometimes, even with A* and a good heuristic, finding the optimal path through all the dots is hard. In these cases, we’d still like to find a reasonably good path, quickly. In this section, you’ll write an agent that always greedily eats the closest dot. _ClosestDotSearchAgent_ is implemented for you in `searchAgents.py`, but it’s missing a key function that finds a path to the closest dot.
 
 Implement the function _findPathToClosestDot_ in `searchAgents.py`. Our agent solves this maze (suboptimally!) in under a second with a path cost of 350:
 ```
 python pacman.py -l bigSearch -p ClosestDotSearchAgent -z .5
 ```
 Your _ClosestDotSearchAgent_ won’t always find the shortest possible path through the maze.
 
