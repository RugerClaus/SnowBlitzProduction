# Welcome to the Snow Blitz production reopository.

## This document is under construction


**GAME PROGRESSION SYSTEMS**

# Shrink Rate System

The **shrink rate** determines how fast the player's size decreases over time. The rate is based on the player's current diameter. Smaller sizes shrink faster, while larger sizes shrink more slowly.

- If the player has the **ANTI_SHRINK** power-up, the shrink rate is `0`, and the player won't shrink.
- The system uses predefined size ranges to apply different shrink rates.

#### Shrink Rate Table:
Values calculated at 60 frames per second

|   Diameter   | Shrink Rate/frame  |
|--------------|--------------------|
| 350+         | 1.00               |
| 325 - 349    | 0.90               |
| 300 - 324    | 0.80               |
| 275 - 299    | 0.70               |
| 250 - 274    | 0.60               |
| 225 - 249    | 0.50               |
| 200 - 224    | 0.40               |
| 175 - 199    | 0.30               |
| 150 - 174    | 0.20               |
| 125 - 149    | 0.10               |
| 100 - 124    | 0.09               |
| 75 - 99      | 0.08               |
| 50 - 74      | 0.07               |
| 40 - 49      | 0.05               |
| 10 - 39      | 0.02               |
| Less than 10 | 0.01               |

The shrink rate speeds up as the player gets bigger.
Power-ups like **ANTI_SHRINK** stop the player from shrinking.


# Welcome to the Distant Realms Framework for Developing Applications with Python

## Introduction
- Distant Realms is a Python application framework and tooling ecosystem for building games and interactive applications. Containing support for rendering, audio, input, simple networking as well as a ready built WYSIWYG ui editor that outputs to a format the engine can read directly. Below you will learn how to make games and other applications using Distant Realms

- Distant Realms is designed around convenience without lock-in.

- The framework provides high-level systems for common application needs, but those systems are built on straightforward underlying APIs. You can use as much or as little of the framework as your application requires.

NOTE: ALL EXAMPLE SECTIONS START WITH A NUMBER LIKE THIS: [01] +. When I refer to an example, I will refer to its number.

## Dependencies

This project has a few dependencies. The only third-party assets are the fonts in `assets/font`.

It uses the OpenSansPX font, a modified version of Open Sans, under the Apache License 2.0. See `LICENSE.txt` in the `assets/font` directory for details.

There is no requirements.txt because there are only four dependencies.

## Setup

From the root directory, run:

```bash setup.sh```

Once this has run, you should be all set to run the program using:

To start the program in normal most with developer mode off:

```python3 main.py```

To start the program with developer mode on:

```python3 main.py --dev```

To skip the splash screen and start the program with developer mode on:

```python3 main.py --devg```

For windows use:
 ```python main.py --flags```
