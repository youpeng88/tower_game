# tower_game
# Lastest Change by Yoyo:
    9.32pm: added a start menu with new game and load works (currently commented out at the end of the code to make debug easier)
    10:04pm: fixed the draw line problem, now you can see the tower laser shooting line in green. 
    10:32am (monday): added icons to the side bar and moved life bar above with some space (Alex's changes is merged)
    10:40 am (monday): added Alex's recent change with rotation
    1-19-16: Alex's change merged
    1-19-16 12:00pm: user input name (new window), display top 10 high score, goes back to start menu
    1-19-16 (12:16pm): Zach's recent changes merged (life bar with number)
    1-19-16(1:06pm): added level of difficulty menu after you select start game and can go back to main menu after that if you select back  
    1-19-16(2:31pm): added sidebar icon for score, addeed highscore display on main menu (click to go back to main menu)
    1-19-16(2:47pm): Zach's recent changes merged (stronger enemy and gives more money)
    1-19-16(3:20pm): added PC and MAC choices at the start menu (remembers previous selection if don't change platform choice)
    1-19-16(5:10pm): Alex's recent changes merged (turn_based appearance) also fixed box input to make it a larger box (and some small bugs)
    1-19-16(6:30pm): added Instruction buttom on the start menu and merged the changes. 
    1-20-16(3:40pm): fixed input box and merged Alex's changes
    1-20-16(7:30pm): added selection button on the side bar

#Latest Change by Zach:
    12:41 AM: Modified Enemies.point_at_base function such that all enemies now target base
    1/19/16 11:49 AM: Included text with lifebars
    1/19/16 1:53 PM: Enemies get stronger and give more money every 10 waves. Required a new initial variable money_earned_per_enemy
    1/20/16 1:52 AM: Added new function Enemy.touching_another_enemy that ensures enemies are unstackable
    1/20/16 3:51 PM: Slightly improved enemy self avoidance in Enemy.touching_another_enemy although "clumping" can still occur
    1/20/16 10:42 PM: Improved both enemy and knight self avoidance in their respective functions such that clumping should almost        never occur

# Changes by Alex:
    1-18-16 10:30am: Changed the Enemy.point_at_base function to make all enemies move in the right direction. Changed the direction and distance calculation to floats and the speed to 2. Previously, enemies had speed one so any direction that was less than 1 would floor to zero. Now the directions floor to either 0, 1, or 2, but the upper left sprites no longer have both directions floor to zero
    1-18-16 10:35am: Changed the Enemy.point_at_base function and the angle function to allow proper rotation. The angle calculation now takes two vectors, and using the dot product calculates the angle between the vectors, rotating the appropriate ammount. In order to prevent rotation on every turn, if angle is less than 1 the enemy does not rotate. The angle function catches divide by zero exceptions.
    1-18-16 11:10am: Modified the .png images for the sprites on the board to be transparent. For pygame on Windows the game can now have transparent pieces. It looks better? Maybe a better background?
    1-19-16 00:10am: Modified the save and load functionality to keep the defense_towers from the previous game upon load game.
    1-19-16 02:26am: Added a highscore archive to keep track of and display highscores. This involved: creating a highscore class, saving the score, adding user input for name, calling the scores at the beginning. Also changed to grass background.
    1-20-16 11:47am: Made the game smoother by removing unnecessary clock tick. Fixed bug in menu which prevented entire screen from filling. Made score icon transparent.
    1-20-16 2:04pm:  Made the game fullscreen with smooth transitions between screens. Sidebar now on right for aesthetics. 
    1-20-16 3:32pm:  Added knights that chase demons and can be placed with the right mousebutton

# Latest Version: 
    1-19-16: Alex's recnet change merged (grass backgorund, userinput name and high score)
    1-19-16 (12pm): Yoyo's recent changes merged (user input name, display high score and goes back to start menu)
    1-19-16 (12:16pm): Zach's recent changes merged (life bar with number)
    1-19-16(1:06pm): Yoyo's recent changes merged (difficulty level menu and parameters, display on side bar)
    1-19-16(2:31pm): Yoyo's recent changes merged (added sidebar icon for score, addeed highscore display on main menu (click to go back to main menu))
    1-19-16(2:47pm): Zach's recent changes merged (stronger enemy and gives more money)
    1-19-16(3:20pm): Yoyo's recent changes merged (added PC and MAC choices at the start menu (remembers previous selection if don't change platform choice)
    1-19-16(5:10pm): Alex's recent changes merged (turn_based appearance, also fixed box input)
    1-19-16(6:30pm): Yoyo's recent changes merged (added instruction buttom)
    1-20-16(3:40pm): Yoyo and Alex's recent changes merged (menu, full screen, knights added and input box)
    1-20-16(7:30pm): Yoyo's recent changes merged (added selection button on the side bar for defense units)
    1-20-16(7:34pm): Zach's recent changes merged (improved enemy self avoidance)
    

