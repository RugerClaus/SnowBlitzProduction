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