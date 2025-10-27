<h1>Welcome To The Distant Realms Framework/Engine-thingy</h1>



<p>This is basically a KOTOR remake or i'm going to try to kinda do that. I want to do it from a topdown or quasi-isometric perspective. Maybe something a bit like pokemon but more detailed.</p>

<p>In order to handle game events, each event can be thought of as a new state in a tree of states. A child state. Think of Choose Your Own Adventure novels. Each choice influences the path you take. That's down to the application level, and frankly, I think, central to a decent RPG engine.</p>

<p>I've improved a lot of the handling of the framework with this update. Put centralized input handling onto game event handler. Redid all the state handling, and centralized all states to the core/state directory and each layer is separated. Each subdirectory contains every state manager at that layer (i.e. core/state/ApplicationLayer contains both state managers for the APPSTATE and APPMODE) of parallel state machines.</p>