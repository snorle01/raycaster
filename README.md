# raycaster
you have to have pygame and python to run this game and the level editor.

open main.py to play the game or open level_editor.py to open the level editor.

# main game
to run the main game you have to have a map.json file if there is none then you can make one with the level editor.

you can walk around using (w a s d) and left and right arrow keys to look around.

press space to shoot, there is nothing to shoot at and there is no sound.

press enter to switch to 2D mode or back to 3D.

# level editor
the level editor is not user friendly.

when opening the level editor is stuck at a size of 13 x 10.

to place walls you use the mouse and click on a square. if you click on the wall multiple times you can change the texture and eventualy you will remove it. 
you can use both right and left mouse buttons.

if you press the S key you will place a sprite on the square where the mouse is. the sprites works just like the walls by pressing S multiple times.

if you press the P key you will move the player, BUT you can't change the players rotation. if you want to change the rotation then you can change the variable named 
player_angle on line 140.

if you press the enter key you can open the map.json in the folder, the map.json is the current map the game will run. if there is no map.json than the editor will crash.

if you press the space key then you will exsport your map and make or overwrite the current map.json file.

WARNING! be carefull not to overwrite your beautiful levels by pressing space by mistake as there is no popup or warning before overwriting.

you can move or rename the map.json file if you dont want to change it.
