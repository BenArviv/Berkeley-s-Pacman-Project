## Project 2: Multi-Agent Search

### Question 1: Reflex Agent
Improve the _ReflexAgent_ in `multiAgents.py` to play respectively.
The provided reflex agent code provides some helpful examples of methods that query the _GameState_ for information.
A capable reflex agent will have to consider both food locations and ghost locations to perform well.
Your agent should easily and reliably clear the _testClassic_ layout:
```
python pacman.py -p ReflexAgent -l testClassic
```
Try out your reflex agent on the default _mediumClassic_ layout with one ghost or two (and animation off to speed up the display):
```
python pacman.py --frameTime 0 -p ReflexAgent -k 1
```
```
python pacman.py --frameTime 0 -p ReflexAgent -k 2
```
It will likely often die with 2 ghosts on the default board, unless your evaluation function is quite good.
Options: Default ghosts are random; you can also play for fun with slightly smarter directional ghosts using `-g DirectionslGhost`.
You can also play multiple games in a row with `-n`. 

### Question 2: Minimax
Now you will write an adversarial search agent in the provided _MinimaxAgent_ class stub in `multiAgents.py`.
Your minimax agent should work with any number of ghosts, so you'll have to write an algorithm that is slightly more general
than what you've previously seen in lecture.
In particular, your minimax tree will have multiple min layers (one for each ghost) for every max layer.

Your code should also expand the game tree to an arbitrary depth.

Importent: A single search ply is considered to be one Pacman move and all the ghosts' responses, so depth 2
search will involve Pacman and each ghost moving two times.

* The correct implementation of minimax will lead to Pacman losing the game in some tests.
This is not a problem: as it is correct behaviour.
```
python pacman.py -p MinimaxAgent -l minimaxClassic -a depth=4
```
* On larger boards such as _openClassic_ and _mediumClassic_ (the default), you'll find Pacman to be good at not dying, but quite bad at winning.
He'll often thrash around without making progress.
He might even thrash around right next to a dot without eating it because he doesn't know where he'd go after eating that dot.

* When Pacman  believes that his death is unavoidable, he will try to end the game as soon as possible because of the constant penalty for living. 
Sometimes, this is the wrong thing to do with random ghosts, but minimax agents always assume the worst.

### Question 3: Alpha-Beta Pruning
Make a new agent that uses alpha-beta pruning to more efficiently explore the minimax tree, in _AlphaBetaAgent_. 
Again, your algorithm will be slightly more general than the pseudocode from lecture, so part of the challenge is to extend the alpha-beta pruning 
logic appropriately to multiple minimizer agents.

You should see a speed-up (perhaps depth 3 alpha-beta will run as fast as depth 2 minimax).
Ideally, depth 3 on _smallClassic_ should run in just a few seconds per move or faster.
```
python pacman.py -p AlphaBetaAgent -a depth=3 -l smallClassic
```
The _AlphaBetaAgent_ minimax values should be identical to the _MinimaxAgent_ minimax values,
although the actions it selects can vary because of different tie-breaking behavior.

### Question 5: Expectimax
Minimax and alpha-beta are great, but they both assume that you are playing against an adversary who makes optimal decisions.
As anyone who has ever won tic-tac-toe can tell you, this is not always the case.
In this question you will implement the _ExpectimaxAgent_, which is useful for modeling probabilistic behavior of agents who may make suboptimal choices.

As with the search and constraint satisfaction problems covered so far in this class, the beauty of these algorithms is their general applicability. 

Once your algorithm is working on small trees, you can observe its success in Pacman.
Random ghosts are of course not optimal minimax agents, and so modeling them with minimax search may not be appropriate.
_ExpectimaxAgent_, will no longer take the min over all ghost actions, but the expectation according to your agent’s model of how the ghosts act.
To simplify your code, assume you will only be running against an adversary which chooses amongst their _getLegalActions_ uniformly at random.

To see how the ExpectimaxAgent behaves in Pacman, run:
```
python pacman.py -p ExpectimaxAgent -l minimaxClassic -a depth=3
```
You should now observe a more cavalier approach in close quarters with ghosts.
In particular, if Pacman perceives that he could be trapped but might escape to grab a few more pieces of food, he’ll at least try.

The correct implementation of expectimax will lead to Pacman losing some of the tests.

### Question 5: Evaluation Function
Write a better evaluation function for pacman in the provided function _betterEvaluationFunction_.
The evaluation function should evaluate states, rather than actions like your reflex agent evaluation function did.
With depth 2 search, your evaluation function should clear the _smallClassic_ layout with one random ghost 
more than half the time and still run at a reasonable rate (to get full credit,
Pacman should be averaging around 1000 points when he’s winning).

You can try your agent out with:
```
python autograder.py -q q5
```
