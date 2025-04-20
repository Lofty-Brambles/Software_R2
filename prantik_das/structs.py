from typing import Any, TypedDict, Callable, Literal


# implement some sort of speed validation?
class Command(TypedDict):
    speed: int
    altitude: int
    movement: Literal["fwd", "rev"]


type Sensor = Literal["RED", "YELLOW", "GREEN"]


class Telemetry(TypedDict):
    position: tuple[int, int]
    battery: float
    gyro: tuple[float, float, float]
    wind: float
    dust: float
    sensor: Sensor


class DroneData(TypedDict):
    telemetry: list[Telemetry]
    commands: list[Command]
    metrics: Any


class ClientData(TypedDict):
    url: str
    conn_id: str | None
    time: float
    commands_count: int
    runner: Callable[[DroneData], Command]
