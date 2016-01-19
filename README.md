# tower_game
# Lastest Change by Yoyo:
    9.32pm: added a start menu with new game and load works (currently commented out at the end of the code to make debug easier)
    10:04pm: fixed the draw line problem, now you can see the tower laser shooting line in green. 
    10:32am (monday): added icons to the side bar and moved life bar above with some space (Alex's changes is merged)
    10:40 am (monday): added Alex's recent change with rotation
    1-19-16: Alex's change merged
    1-19-16 12:00pm: user input name (new window), display top 10 high score, goes back to start menu

#Latest Change by Zach:
    12:41 AM: Modified Enemies.point_at_base function such that all enemies now target base
    1/19/16 11:49 AM: Included text with lifebars

# Changes by Alex:
    1-18-16 10:30am: Changed the Enemy.point_at_base function to make all enemies move in the right direction. Changed the direction and distance calculation to floats and the speed to 2. Previously, enemies had speed one so any direction that was less than 1 would floor to zero. Now the directions floor to either 0, 1, or 2, but the upper left sprites no longer have both directions floor to zero
    1-18-16 10:35am: Changed the Enemy.point_at_base function and the angle function to allow proper rotation. The angle calculation now takes two vectors, and using the dot product calculates the angle between the vectors, rotating the appropriate ammount. In order to prevent rotation on every turn, if angle is less than 1 the enemy does not rotate. The angle function catches divide by zero exceptions.
    1-18-16 11:10am: Modified the .png images for the sprites on the board to be transparent. For pygame on Windows the game can now have transparent pieces. It looks better? Maybe a better background?
    1-19-16 00:10am: Modified the save and load functionality to keep the defense_towers from the previous game upon load game.
    1-19-16 02:26am: Added a highscore archive to keep track of and display highscores. This involved: creating a highscore class, saving the score, adding user input for name, calling the scores at the beginning. Also changed to grass background.

# Latest Version: 
    1-19-16: Alex's recnet change merged (grass backgorund, userinput name and high score)
    1-19-16 (12pm): Yoyo's recent changes merged (user input name, display high score and goes back to start menu)
