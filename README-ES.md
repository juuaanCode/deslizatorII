# DESLIZATOR (II)
[![en](https://img.shields.io/badge/lang-en-red.svg)](/README.md)

Este trabajo fue realizado en 1º de Ingeniería Informática en la Universidad de Valladolid, como parte de la asignatura _Paradigmas de Programación_.

El objetivo del trabajo era iniciarse en el manejo de GUI creando un juego rápido y divertido usando la [librería wxPython](https://wxpython.org/).

La mejor manera de entender el juego es verlo como una versión _aplanada_ del juego Tetris, al ser todas las piezas solo de 1 celda de altura. En cada turno las piezas se generan en la fila superior, y el usuario puede hacer un movimiento en la pieza que quiera.

Cuando una fila se completa se elimina, a menos que sea una fila completamente de un solo color. En ese caso, el tablero entero se borra. Por cada celda borrada se añade un punto al total.

![DESLIZATOR II](/screenshot.png "DESLIZATOR II")

## Generación de piezas

Las piezas no se generan aleatoriamente, sino siguiendo un patrón. Ese patrón lo marca un fichero que debe estar correctamente formateado.
El formato es el siguiente:
* Distinguiendo entre letras mayúsculas y minúsculas se crean las piezas. Por ejemplo, "AAa" genera dos piezas, una el doble de ancho que la otra.
* Las letras marcan el color. A/a es verde, B/b es azul, C/c es rojo.
Como ejemplo hay 2 ficheros.

## Sobre el código
El código está tal cual se entregó en su momento. Se debe entender que es un trabajo de una asignatura de primero, y que se realizó con los conocimientos y las capacidades del momento. Todavía había mucho que aprender.