# Understanding

```
drone_simulator/
├── __init__.py
├── admin_server.py     # [?>0] Does regular reporting of data
├── client.py           # 
├── dashboard.py        # [1] Dash @ ws://localhost:8765
├── drone.py            # [4] Main drone control thing
├── environment.py      # [3] Parsed partially, sets up mock env
├── logging_config.py   # [0] Also logging
├── main.py             # 
├── run_server.py       # 
├── server.py           # 
├── telemetry.py        # [0] Saves drone state
└── validators.py       # [0] Validate input structures of client responses
tools/
└── log_viewer.py       # [1] We do some logging
```

### Data management
- Keep gyro under 45deg
- 50+ meters give altitude stability, no gyro rotation
- Wind speed comes from any direction and gives a gyro of 0-40 (scaled 0-100)
- Movement by speed gives a gyro of +/- 20 gyro on x (scaled 0-5)

- Storm is random, changing altitude or speed doesnt seem to effect it
- SENSOR is also effected by dust and wind

- iter is only counted if speed and dy are non zero
- formula of decay: `f(y) = (0.5 * vs + 0.005 * abs(y)) * (a + (b-a) * e^(-c*y))`
- battery decay = min(0.1, base * factor) - (https://www.desmos.com/calculator/sk2kceulu3)

- speed of 2-5: stay @ 100m
- speed of 1: stay @ 70m, drain is 0.635
- speed of 0: upto 14.5m, drain is 0.1, 0.217 @ 50m, 0.261m @ 70m, 0.33 @ 100m
- travelling below 3m: 0.873 @ 1, 1.722 @ 2, 2.57 @ 3, 3.42 @ 4, **4.26 @ 5** [due to rounding, all equal at 115/116]

- Red sensor is immediate crash, it seems. Avoid it with an expected value.