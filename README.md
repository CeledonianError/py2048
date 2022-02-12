# py2048
I wrote 2048 in Python. It's very messy, uses tkinter, ~~and expects you to have the fonts Atkinson Hyperlegible (https://brailleinstitute.org/freefont) and Monospace installed (this is easy to change).~~

~~If you want to change the fonts:~~

~~Line 135 - Atkinson Hyperlegible~~

~~Line 155 - Monospace~~

Apparently it has no issues if you don't have those fonts. Just note that it may look funky if you don't.
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
My teacher wanted me to write the following, hence why it's so formal:

The "simple" game of 2048, uses tkinter for GUI.
 
2048 is a tile-matching game. With each move (up, down, left or right), every tile on the 4x4 board is moved as far in that direction as it can go. If it collides with the same valued tile, they are added together ONCE. If tiles merge and end up beside a tile of the same, new value, they do not get merged. Merging starts at the side of the board that corrosponds to the inputted direction, i.e.: if the board is as follows:
  
`2 0 2 4`
  
`2 0 0 2`

`4 0 4 0`

`2 2 2 4`

and the player presses RIGHT, the resulting board should be:

`0 0 4 4`

`0 0 0 4`

`0 0 0 8`

`0 2 4 4`


At the start, 2 tiles (valued either 2 or 4, more likely to be 2) are randomly placed. After every move, if there are any empty tiles remaining, a random 2, or, less likely, 4, valued tile will be generated. The game ends if the board is filled and there are no valid moves left. The player wins if they create a tile with value 2048. The game can continue past 2048, but this program will not react to the player creating a 4096, or higher, tile. It will only produce a win state for a 2048 tile.
