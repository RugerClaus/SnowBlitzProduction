**SNOW BLITZ PRODUCTION REPOSITORY**

<h2>Welcome To Snow Blitz. Stay open, friends!</h2>

<p>Any issues, you can email me (rugerclaus) at dev@snowblitz.net</p>

<p>This README markdown file will be used to document the framework, the game, and all the APIs allowing everything to connect.</p>

**THE "PRODUCTION" REPOSITORY** 

<p>This branch, the main branch will be for cutting edge features. Features need to be at least feature complete upon commit unless i'm personally feeling lazy.</p>

<p>The most recent stable update released (source code), will be available on <a href="https://snowblitz.net/downloads/source/SnowBlitz_Beta_Source_Latest.zip">DOWNLOAD LINK FROM SNOWBLITZ.NET</a></p>

<p>Previous versions will be archived on **snowblitz.net/downloads/archive/source**, and will be organized by version, latest first. I hate going into some software archive and finding it difficult to locate downloads. Every single list item MUST BE a download link for that version. The same applies to <b>snowblitz.net/downloads/archive/builds/[linux|windows|macos]</b>, and players will have an easy time regardless of their skill level. This is the MOST IMPORTANT part of the project.</p>


**DEPENDENCIES**

<p>This project has a few dependencies. The only third party assets are the fonts in assets/font:</p>
<p>This project uses the OpenSansPX font, a modified version of Open Sans, under the Apache License 2.0. Please see the LICENSE.txt in the assets/font directory for more details.</p>

<p>The reason we're lacking a requirements.txt file, is that there are only 4 dependencies!<p>

<h3>From the root directory run this series of commands to get set up</h3>

```bash
python3 -m venv virtualenv
source virtualenv/bin/activate
pip install pygame-ce pyinstaller mutagen requests
python3 setup.py
python3 main.py --dev
```
**NOTE:** passing the flag --dev enables developer mode by default on startup
**NOTE:** `setup.py` is absolutely **ESSENTIAL** to run the program.

**FEATURE ADDITIONS**

<p>For feature additions, before coming up with your own you should take a look at the requested_additions file in the root directory of this repository and see if you can piece in any of those requested features. Then submit a pull request to have your code merged into the main branch. This is mostly notation for me though</p>

**BUGS**

<p>For fixing bugs, please start in the bug_tracker file of this directory. For now it's a bit unorganized until I can set up a database and bug tracking section of the website. Then I'll make an easy UI to manage that stuff, but at the current scale of the project, we also have a lot of cushioning, so it shouldn't be super prudent to do so immediately.</p>

**COMMITS**

<p>We only use the latest versions of all dependencies to keep things consistent</p>

<p>Keep your commit messages as clear and concise as possible. We have no established versioning for commits, and we're going to rely on commit messages for minor updates to the main branch. Just the way it is. If you want to change it, build the infrastructure.</p>


**GAME PROGRESSION SYSTEMS**

# Shrink Rate System

The **shrink rate** determines how fast the player's size decreases over time. The rate is based on the player's current diameter. Smaller sizes shrink faster, while larger sizes shrink more slowly.

- If the player has the **ANTI_SHRINK** power-up, the shrink rate is `0`, and the player won't shrink.
- The system uses predefined size ranges to apply different shrink rates.

#### Shrink Rate Table:
Values calculated at 60 frames per second

|      Diameter      | Shrink Rate/frame  |
|--------------------|--------------------|
| 350+               | 1.00               |
| 325 - 349          | 0.90               |
| 300 - 324          | 0.80               |
| 275 - 299          | 0.70               |
| 250 - 274          | 0.60               |
| 225 - 249          | 0.50               |
| 200 - 224          | 0.40               |
| 175 - 199          | 0.30               |
| 150 - 174          | 0.20               |
| 125 - 149          | 0.10               |
| 100 - 124          | 0.09               |
| 75 - 99            | 0.08               |
| 50 - 74            | 0.07               |
| 40 - 49            | 0.05               |
| 10 - 39            | 0.02               |
| Less than 10       | 0.01               |

The shrink rate speeds up as the player gets bigger.
Power-ups like **ANTI_SHRINK** stop the player from shrinking.
