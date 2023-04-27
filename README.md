# Berkeley's Pacman project
This is an assignment given in the Open University of Israel's course: **Introduction to Artificial Intelligence**, and is based on Berkeley's Pacman project, written by **John DeNero**, **Dan Klein** and **Pieter Abbeel**.

All of the question parts has been filled and ready for use by pasting the relevant code for each section into the command line, you can find the added code in `search.py` and `searchAgent.py`.

## Introduction
In this project, your Pacman agent will find paths through his maze world, both to reach a particular location and to collect food efficiently. You will build general search algorithms and apply them to Pacman scenarios.

The code for this project consists of several Python files, some of which you will need to read and understand in order to complete the assignment, and some of which you can ignore.

## Welcome to Pacman
After downloading the code you should be able to play a game of Pacman by typing the following at the command line:
```
> python pacman.py
```
Pacman lives in a shiny blue world of twisting corridors and tasty round treats. Navigating this world efficiently will be Pacman’s first step in mastering his domain.

The simplest agent in `searchAgents.py` is called the _GoWestAgent_, which always goes West (a trivial reflex agent). This agent can occasionally win:
```
python pacman.py --layout testMaze --pacman GoWestAgent
```
But, things get ugly for this agent when turning is required:
```
python pacman.py --layout tinyMaze --pacman GoWestAgent
```
If Pacman gets stuck, you can exit the game by typing **CTRL-c** into your terminal.

Soon, your agent will solve not only _tinyMaze_, but any maze you want.

Note that `pacman.py` supports a number of options that can each be expressed in a long way (e.g., --layout) or a short way (e.g., -l). You can see the list of all options and their default values via:
```
python pacman.py -h
```
