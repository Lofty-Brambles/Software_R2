import math
import scipy.optimize as opt

from prantik_das.structs import Telemetry, Command, DroneData


def constantRunner(data: DroneData) -> Command:  # maximizes at 116
    """
    This runner keeps the drone at the least possible RED-safe altitude.
    As travelling at max speed is the most efficient, it uses that.
    Exploits critical gyro not being a problem.
    """
    initial = {"altitude": 3, "speed": 4, "movement": "fwd"}
    nextodd = {"altitude": -1, "speed": 4, "movement": "fwd"}
    nexteven = {"altitude": 1, "speed": 4, "movement": "fwd"}

    if len(data["telemetry"]) == 0:
        return initial
    else:
        return nextodd if len(data["telemetry"]) % 2 != 0 else nexteven


def minimaApproachRunner(data: DroneData) -> Command:  # maximizes at 150
    """
    This runner pushes the drone to the minima of battery drain at a particular speed.
    To make it safe, it pushes the drone down to y = 3 if sensor turns red.
    """
    SPEED = 5

    drain = lambda x: (SPEED * 0.5 + x * 0.005) * (0.6 + 1.2 * math.exp(-0.03 * x))
    minima_result = opt.minimize(drain, x0=85)
    minima_altitude = int(minima_result.x)

    EV_CHANGE = 50 + 0
    LT_VALUE = 90 - EV_CHANGE

    def is_in_danger(telemetry: Telemetry):
        return telemetry["wind"] > LT_VALUE or telemetry["dust"] > LT_VALUE

    def perfect_altitude():
        last, s2last = data["telemetry"][-1], data["telemetry"][-2]
        last_cmd = data["commands"][-1]

        if (not is_in_danger(last)) and (is_in_danger(s2last)):
            return minima_altitude - last["position"][1]
        elif (is_in_danger(last)) and (not is_in_danger(s2last)):
            return 3 - last["position"][1]
        else:
            return -1 if last_cmd["altitude"] != -1 else 1

    if len(data["telemetry"]) == 0:
        return {"altitude": minima_altitude, "speed": SPEED, "movement": "fwd"}
    elif len(data["telemetry"]) == 1:
        return {"altitude": -1, "speed": SPEED, "movement": "fwd"}
    else:
        return {"altitude": perfect_altitude(), "speed": SPEED, "movement": "fwd"}


all_runners = {"constant": constantRunner, "minima": minimaApproachRunner}
