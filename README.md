**SNOW BLITZ PRODUCTION REPOSITORY**

<h2>Welcome To Snow Blitz. Stay open, friends!</h2>

<p>Any issues, you can email me (rugerclaus) at dev@snowblitz.net</p>

<p>This README markdown file will be used to document the framework, the game, and all the APIs allowing everything to connect.</p>

**THE "PRODUCTION" REPOSITORY** 

<p>This branch, the main branch will be for cutting edge features. Features need to be at least feature complete upon commit unless i'm personally feeling lazy.</p>

<p>The most recent stable update released (source code), will be available on its own branch. We will delete that branch upon a new version.</p>

<p>Previous versions will be archived on <b>snowblitz.net/downloads/archive/source</b>, and will be organized by version, latest first. I hate going into some software archive and finding it difficult to locate downloads. Every single list item MUST BE a download link for that version. The same applies to <b>snowblitz.net/downloads/archive/builds/[linux|windows|macos]</b>, and players will have an easy time regardless of their skill level. This is the MOST IMPORTANT part of the project.</p>


**DEPENDENCIES**

<p>This project has a few dependencies. The only third party assets are the fonts in assets/font:</p>
<p>This project uses the OpenSansPX font, a modified version of Open Sans, under the Apache License 2.0. Please see the LICENSE.txt in the assets/font directory for more details.</p>

<p>The reason we're lacking a requirements.txt file, is that there are only 4 dependencies!<p>

<h3>From the root directory run this series of commands to get set up</h3>

```bash
python3 -m venv virtualenv
source virtualenv/bin/activate
pip install pygame-ce pyinstaller mutagen requests
python3 main.py