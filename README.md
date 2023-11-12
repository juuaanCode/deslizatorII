# DESLIZATOR (II)
[![es](https://img.shields.io/badge/lang-es-red.svg)](/README-ES.md)

This assignment was made during my 1º year studing Computer Science at University of Valladolid, as part of the subject _Paradigmas de Programación_ (Programming Paradigms).

The objective with this task was to learn GUI management while creating a fun, quick game using the [wxPython library](https://wxpython.org/).

The best way to understand the game is to view it as a _flattened_ version of the popular game Tetris, as all the pieces here are only one row high. On every turn several pieces are generated on top of the display, and the user only has one movement to make on whichever piece he wants.

Whenever a row is full, it is deleted. But if that row is full of pieces of the same color, the entire board is cleared. 1 point is awarded per cell erased.

![DESLIZATOR II](/screenshot.png "DESLIZATOR II")

## Piece generation

Pieces are not generated randomly. Before starting to play, a file containing text correctly formatted must be provided.
The format of the file is as follows:
* Using capital and lowercase letters defines the different pieces. For example, "AAa" makes two pieces, the first one double the length of the second.
* The letter defines the color. A/a is green, B/b is blue, C/c is red.
Some example files are provided.

## About the code
The code is exactly as it was provided to be qualified. This means it is written with Spanish comments and variable names.
Keep in mind this is a first year subject when reviewing it, I had quite a lot yet to learn.