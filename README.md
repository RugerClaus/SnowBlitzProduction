<p>This branch of Distant Realms Python is SnowBlitz remastered really. I'll be implementing the whole game in this modular framework and build a better entity system for it as well. I'm halfway there. The next parts will be finishing the entity system and then i'll work on the rendering logic. It should actually be stupidly easy and i can copy over a bunch of code.</p>

<p>UPDATE: I have fully prepared the player and its scaling along with decoupled movement controls using the Controls class. So you can move the player around and resize the screen with everything scaling successfully. Reworked the Surface class a bit in the Window.py file. Going to take some of the core engine mechanics that I have improved in this version (core/guts) and merge them with the main branch to keep the engine code consistent.</p>

<p>This whole thing has been an excersize in iterating and finding the most modular ways to do things as I actually scaffold Distant Realms into a fully fledged engine. For now though, I'm building Snow Blitz. It should be done in the next few weeks, I'll work on heavy play testing, and then I'll release this on steam.</p>

<p>Fortunately due to the way I have basically completely redesigned it using the framework, adding game modes, entities, and other fascets of the game will be totally trivial once I have all the core mechanics in place again. This way, there's no monolithic codebase keeping me from adding features.</p>


<h3><b>UPDATE 2:<b></h3>
<p>I could really structure this better and take all this rambling out of the readme file, but here we are.... Either way, I have now added the player UI for the progress bar and will work on the rest of the positions of it next. Then I will implement the small settings menu allowing you to change the controls, where the progress bar is, and toggle the music.</p>

<p>Overall it's shaping into a fine recreation of snow blitz, and once I have the next small details worked out I can finish the implementation of the game. It may take me less time than I thought it would. Which is great because I'd like to do an actual release and this little framework is speedrunning that.</p>

<h3>UPDATE 3:</h3>
<p>I have finished the UI. next step is adding a settings menu at the main menu and one for the pause menu. I may just have the settings on the pause screen to save effort.</p>
<p>Once I have settings for toggling music on/off, as well as a master volume, and a setting for moving the progress bar back and forth from top to bottom, I will start implementing the entities and the rest of the game mechanics. This is nearly good enough to sell on steam.</p>

<h3>UPDATE 4:</h3>

<p>Major update. I added a new type of submenu for settings as well as toggle switches for the progress bar position and music state. Scaling fully works for the player and its UI. I will be soon removing some of the more generic properties from the player class and further modularizing them in the Entity class for other entities to use (diameter, surface, so on). This game is already getting very very close to polished. Now I really just need to work in the game and a few other QOL tweaks like the ability to toggle true fullscreen mode, which should be pretty simple by addition of another state machine.</p>

<p>I made some significant changes around the framework itself as well that I will soon be merging into the main branch. I have given the mode manager and appstate manager classes an extension from the base state manager class and configured their logging properly now. Everything logs now and state is even more solidified. Added some helper methods such as the toggle music method on the audio engine.</p>

<h3>UPDATE 5:</h3>

<p>Finally we're here, the game actually fucking works at least in endless mode. Well the base mechanics. I have integrated the snowfall, and the rocks and collision logic for both with the player. Both are properly integrated as entities, so all the typing is consistent. This was a hurdle, but it's smooth sailing from here. For the most part I can copy the classes over with some changes for entity specific logic like snowflakes vs power up types.</p>

<p>The leveling system works fine and everything resets properly when transitioning to another level or the game being over due to the player dying. All those states are consistent as well. I may add state machines for the non player entities, but really they only have 2 states, on screen and off screen. when on screen they're falling and when off screen they don't exist. they are wiped from existence when falling to a certain height (the ground) or if the player collects them.Overall this is all pretty perfect and I am very proud to say that this game is nearly ready for release. The next month will be finishing the entity system (over the next day or two) and then working on polishing the UI as well as adding full screen mode.</p>

<p>This is certainly going far far smoother than the original codebase did and the scaffolding is far superior. Distant Realms as a framework is extremely good at this point. Thanks for reading my rambling if you do. Excuse my fuck words, there is no censorship in the open sorce as far as I'm concerned. Currently no sound is played when snow is collected, but i'll add that in in the next update since it's really no big deal.</p>

<p>The game is now fully playable. No level reducers or powerups yet, but endless mode is fully playable, rocks collide with snow more or less properly and the leveling system works without a hitch. There was a bug that spawned invisible rocks. Fixed that. No more game breaking bugs. All hail state machines!</p>

<h3>UPDATE 6:</h3>

<p>You can now pick up powerups and the entire logic system for powerups has been added. Now it's just down to adding powerup types. The absorb rock and anti shrink ones have been added along with handling their sound effects.</p>

<p>I'll focus on the level reducers next as i'm not going to add the grow power up yet since it was mostly pretty useless in the original codebase.</p>

<p>Either way, the game is actually a game now. In addition the reset methods all work fine now so you can reset the game at any time. Cleaned up the state machines and removed the redundant player status state. This isn't pokemon. The player has a state machine handling the powerups already as well as being alive or dead. the status state was totally redundant.</p>

<h3>UPDATE 7:</h3>

<p>This is a major update. I have began implementing the Tutorial game mode to little success so far, but I have pretty much finished all the mechanics and entities and endless mode works well. I have given a new curve to the progression system in Endless mode by only increasing the level up size by 5 each time. this makes earlier levels easier and the game last longer. However the level reducers are still a massive aid to the challenge as you level up. I'll need playtesters to confirm, but I'm certain that the progression is pretty nice on that front.</p>

<p>However I digress on that front. The endless mode is complete. I could add more powerups and I have some set up but haven't integrated them yet. The absorb rock and anti shrink are it for now, but they fit nicely with the progression. I just don't know how I feel about growth powerups anymore, but I'll definitely do the speed powerups.</p>

<h3>UPDATE 8:</h3>

<p>After taking a couple days break to play some minecraft, here we are. I finally finished the tutorial mode. It was a bit clunky to get going, but it works very well, and can easily be modified and updated. </p>

<p>So here we have it. Two of three game modes are implemented, and I have begun to implement a developer mode to the greater framework. So the developer mode is the next big update. I may stifle development of Blitz mode in favor of it for A: my own sanity, and B: this is being released as a beta. I'll sell it for 2 bucks as the beta despite the namesake mode being completely unstarted, but the application at this point is robust enough to release. I will start working on the rest of the settings including controls, and volume. Then I will proceed to implement the developer mode.</p>

<p>So finishing, i'm done for tonight I think. as much as I want to work on this more, a great book is calling my name and I have been putting off reading it just so I could get on implementing tutorial mode and making it fucking work. Well now it does, all the way to the win menu. I had to do some stupid modification of the game class to put it in, but it's the only mode you can win at I think for now. Otherwise I may have to rework the game states and just do it that way. Honestly that would have been cleaner, but it's really no trouble to fix at some point as a refactor of that class.</p>


<h3>UPDATE 9:</h3>

<p>Minor update. I just added a credits display so that you can see who worked on the application as well as tweaking the debug overlay's draw_most_recent_keypress for the input. I also tweaked the size bar so that the entire player UI can be shifted from top to bottom and the text snaps to the sizebar. It's an illusion, it doesn't really snap to it, but it may as well for the user.</p>

<h3>UPDATE 10:</h3>
<p>We're getting so close to the beta release now! I added minimal audio settings within the settings menu. This allows for turning the music on and off, as well as adjusting the volume. I will probably add this to the framework at large as well. So big double plus good there. I added Blitz mode, but it's just a clone of Endless for now. </p>

<p>Speaking of blitz mode I'm thinking of making it a bit of a doozy. We're gonna have weather events (besides snow), a timer on each level, and the progression will be easier. Going to add some entities like a freeze timer powerup and a powerup that gives the player a temporary speed boost. One other I'd like to add is a cannon to blast rocks!</p>

<p>Just kidding haha! I completely decoupled pygame's logic from the game itself as well as the framework outside of the Window class. This meanst the framework is now fully agnostic of the graphics library. I just have to obey the calls in the API and I can do what I want. I also implemented an error logging system and have implemented it for rendering all of the entities. So we're happy there. Going to improve the error logging to expand to all application variables.</p>

<p>So yeah this is a ground-breaking update and I'll soon be integrating those framework changes over to the primary engine codebase. We're getting there iteration by iteration.</p>