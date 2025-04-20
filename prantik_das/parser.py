from typing import Final
import re

from prantik_das.structs import Telemetry


class Parser:
    @staticmethod
    def parse_telemetry(telemetry: str) -> Telemetry | None:
        REGEX: Final = (
            r"X-(\d+)-Y-(\d+)-BAT-([\d\.]+)-GYR-(\[.+\])-WIND-([\d\.]+)-DUST-([\d\.]+)-SENS-(.+)"
        )

        match = re.search(REGEX, telemetry)
        return (
            None
            if match == None
            else {
                "position": (int(match.group(1)), int(match.group(2))),
                "battery": float(match.group(3)),
                "gyro": Parser.degreefy(eval(match.group(4))),
                "wind": float(match.group(5)),
                "dust": float(match.group(6)),
                "sensor": match.group(7),
            }
        )

    @staticmethod
    def degreefy(params: list[int]) -> tuple[int, int, int]:
        return tuple(map(lambda x: x * 90.0, params))
