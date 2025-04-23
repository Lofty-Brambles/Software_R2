# An Attempt at Flying (Documentary by JUright Brothers™) 🚀

This is mainly a gist of what I did and how I approached a problem, and not a hugely detailed and comprehensive report.

## Initial setup ⚙

I knew that Python had some _weird_ shenanigans with their package management setup. Took me some time to set up `venv` and install. Ran into some weird problems with project roots and not recognising modules where I ended up copying some of the code from the problem itself to setup modules. Wish the organisation was better, makes me miss `cargo`.

I wanted some sort of _testing_, even if I wasnt planning on doing TDD the whole way, atleast for some of the components like the parser. `pytest` was surprisingly nifty.

## Mindmap and Planning 🗺

I started by reading up on the problem code itself, ranking each file with some importance based on what it contained at a glance. Diving deeper into the drone's flight conditions and the environment simulation, I found the logic behind how it functions proportional to the battery drain and environmental conditions.

Avoiding the checks, I tried to optimize it's flight:

- The gyro check didn't actually work. Only the spin generated due to speed was checked and it was always below critical. Thus max speed was always best. **If** it was checked properly, this would have yielded a check on the wind speed to ensure that even if the drone encountered a storm, the tilt was always a net below critcal.
- Storm, wind and dust is randomly generated. There's no regions that are marked to be rough, so no need of application logic to dodge those.
- A RED sensor due to wind and/or dust levels being too high, at y > 3 is an immediate crash. The code didn't allow for a tick of telemetry to let the drone adjust its course, so the only possible way to avoid a red sensor was to take an expected value and check if the levels could rise above that in the next tick, and if so, head towards a safer altitude.
- Battery drain seems to be a function: `f(v, y, dy) = (0.5 * v + 0.005 * abs(dy)) * (a + (b-a) * e^(-c*y))`. This is capped at a minimum of 0.1. This is one of the key points where I optimised the flight numbers.
- The iterations seem to only count if speed was above 0 and the **altitude changed**. Thus to work around it, I kept shifting the drone up and down by 1, every tick.

This leads to the main point of optimisations - the battery drain function and the expected wind and dust levels to consider. First, the wind and dust. There's two ways to go about this - either take the expected value and stay below the level where the sum of all increases has 50% chance to go above 90 (i.e. E(storm + random generation)), or stay fully safe and never let the drone crash due to levels. In most cases, the expected value works, since storms still only have a 30% chance to trigger.

Next is the battery function. Since we don't have to consider the gyroscope crash conditions, speed is an independant variable. The safe height at a RED sensor is too low, so if there's descent, it is almost always nearly equal to y. Thus, it ends up being `f(y) = (0.5 * v + 0.005 * abs(y)) * (a + (b-a) * e^(-c*y))` for when altitude changes. Plotting it, we get a few curves [https://www.desmos.com/calculator/sk2kceulu3]. We end up getting a minima with some data points:

- speed of 2-5: stay @ **100m**
- speed of 1: stay @ **70m**, drain is 0.635
- speed of 0: upto 14.5m, drain is 0.1, 0.217 @ 50m, 0.261 @ 70m, 0.33 @ 100m
- travelling below 3m: 0.873 @ 1, 1.722 @ 2, 2.57 @ 3, 3.42 @ 4, **4.26 @ 5** [due to rounding, all equal at 115/116]

## Solution Structure 📂

```
prantik_das
├── assets/       # Drone svg images for the bonus task
├── tests/        # Tests for the code
├── __init__.py
├── client.py     # A common client instance associated with a runner strategy, and independant logging
├── mindmap.md    # Dump file for note-taking
├── objects.py    # Pygame objects for the bonus task (Incomplete)
├── parser.py     # Telemetry parser
├── README.md
├── run_client.py # Main CLI, uses client instances associated with runner strategies for the drone
├── run_game.py   # Bonus task's CLI, runs a pygame loop (Incomplete)
├── runners.py    # De-coupled strategies that peek at drone data and yield a command
└── structs.py    # Interface storing file
```

## Bonus Task 🦖

Due to a time constraint (engineer's mentality syndrome), it's mostly incomplete. The plan was to create a sliding window with the drone moving forward every iteration, with a delay, and connect previous points to showcase the trajectory.

## Final Nitpicks ⛏

Python docs need to be better, man.
