from prantik_das.parser import Parser

from typing import Dict, Any
from pytest import mark as m


@m.describe("Parser.parse_tokens")
class TestParseTokens:
    _example_telemetry = [
        (
            "X-13-Y-3-BAT-80.00621714504325-GYR-[-0.3793388716037352, 0.21570397559529014, 0.02868268024337442]-WIND-100-DUST-86.29307191559865-SENS-RED",
            {
                "position": (13, 3),
                "battery": 80.00621714504325,
                "gyro": (-34.14049844433617, 19.413357803576112, 2.581441221903698),
                "wind": 100.0,
                "dust": 86.29307191559865,
                "sensor": "RED",
            },
        ),
        (
            "X-15-Y-2-BAT-83.55823560376925-GYR-[0.14297539527701458, -0.12254725315940954, 0.03185131026428015]-WIND-100-DUST-93.9598436500795-SENS-RED",
            {
                "position": (15, 2),
                "battery": 83.55823560376925,
                "gyro": (12.867785574931313, -11.029252784346859, 2.8666179237852134),
                "wind": 100.0,
                "dust": 93.9598436500795,
                "sensor": "RED",
            },
        ),
        (
            "X-9-Y-3-BAT-92.1339733475372-GYR-[0.10527757870421009, 0.07874995016821879, -0.04116082149292102]-WIND-59.57026608966422-DUST-58.53100200028633-SENS-GREEN",
            {
                "position": (9, 3),
                "battery": 92.1339733475372,
                "gyro": (9.474982083378908, 7.087495515139691, -3.7044739343628916),
                "wind": 59.57026608966422,
                "dust": 58.53100200028633,
                "sensor": "GREEN",
            },
        ),
    ]

    @m.context("When passed some telemetry string")
    @m.it("returns the data as a dict")
    @m.parametrize("telemetry, data", _example_telemetry)
    def test_parse_tokens(self, telemetry: str, data: Dict[str, Any]):
        result = Parser.parse_telemetry(telemetry)

        assert result == data

    @m.context("When passed an invalid telemetry string")
    @m.it("returns None")
    def test_parse_invalid(self):
        string = "Invalid data"
        result = Parser.parse_telemetry(string)

        assert result == None


@m.describe("Parser.degreefy")
class TestDegreefy:
    _example_degrees = [
        (
            [0.10527757870421009, 0.07874995016821879, -0.04116082149292102],
            (9.474982083378908, 7.087495515139691, -3.7044739343628916),
        ),
        (
            [0.14297539527701458, -0.12254725315940954, 0.03185131026428015],
            (12.867785574931313, -11.029252784346859, 2.8666179237852134),
        ),
    ]

    @m.context("When passed a set of gyroscopic data in -1 to 1")
    @m.it("returns them in -90 to 90 degrees")
    @m.parametrize("gyro_input, gyro_output", _example_degrees)
    def test_degreefy(
        self, gyro_input: tuple[int, int, int], gyro_output: tuple[int, int, int]
    ):
        assert Parser.degreefy(gyro_input) == gyro_output
