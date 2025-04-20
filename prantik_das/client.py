"""Main client for the drone simulator."""

from typing import Any
import json
import time

from websockets import ClientConnection, connect, exceptions

from drone_simulator.logging_config import get_logger
from prantik_das.parser import Parser
from prantik_das.runners import all_runners
from prantik_das.structs import DroneData, ClientData


class Client:
    """Client with sockets to fly the thing as per a selected runner."""

    def __init__(self, url: str, runner: str):
        self.drone: DroneData = {"telemetry": [], "commands": [], "metrics": None}
        self.logger = get_logger(f"{runner}_client")
        self.clientData: ClientData = {
            "url": url,
            "conn_id": None,
            "time": time.time(),
            "commands_count": 0,
            "runner": all_runners[runner],
        }

    async def register(self) -> None:
        """Register a connection to the server."""
        self.logger.info(f"Trying to connect to server @ {self.clientData["url"]}")
        print(f"Connecting to server @ {self.clientData["url"]}, ensure it's running.")

        try:
            async with connect(
                self.clientData["url"], ping_timeout=10, close_timeout=5
            ) as ws:
                response = await ws.recv()
                data = json.loads(response)

                self.clientData["conn_id"] = data.get("connection_id")
                message = f"Connected: {self.clientData["conn_id"]}. Messsage: {data["message"]}"
                self.logger.info(message)

                await self.handle_drone(ws)

        except exceptions.ConnectionClosedOK:
            self.logger.info("Server connection closed: OK")

        except exceptions.ConnectionClosedError as e:
            message = f"Server connection closed: Error\n{e}"
            self.logger.error(message, exc_info=True)

        except Exception as e:
            exception = f"Server connection error: {e}"
            self.logger.error(exception, exc_info=True)

        finally:
            self.clientData["time"] = time.time() - self.clientData["time"]
            self.logger.info(f"Client session data: {self.clientData}")

    async def handle_drone(self, ws: ClientConnection) -> None:
        try:
            while True:
                command = self.clientData["runner"](self.drone)
                self.clientData["commands_count"] += 1
                self.drone["commands"].append(command)
                self.logger.info(
                    f"Sending command #{self.clientData["commands_count"]}: {command}"
                )

                await ws.send(json.dumps(command))
                response = await ws.recv()
                response_data = json.loads(response)
                self.update_state(response_data)

                if response_data.get("status") == "crashed":
                    crash_message = response_data.get("message", "unknown")
                    message = f"The drone has crashed: {crash_message}. Statistics: {self.drone["metrics"]}"
                    self.logger.warning(message)
                    break

        except KeyboardInterrupt:
            message = f"The client {self.clientData["runner"]}, was killed by the user."
            self.logger.info(message)

        except exceptions.ConnectionClosed:
            message = f"The server for client {self.clientData["runner"]} was closed."
            self.logger.error(message)

    def update_state(self, response: Any):
        def telemetry_update():
            self.logger.info(f"Appending telemetry: {response["telemetry"]}")
            telemetry = Parser.parse_telemetry(response["telemetry"])
            self.drone["telemetry"].append(telemetry)

        def final_telemetry_update():
            self.logger.info(
                f"Appending final telemetry: {response["final_telemetry"]}"
            )
            telemetry = Parser.parse_telemetry(response["final_telemetry"])
            self.drone["telemetry"].append(telemetry)

        def crash_update():
            if response["status"] != "success":
                self.logger.warning(f"Non-successful response: {response["message"]}")

        def metrics_update():
            self.logger.info(f"Updating metrics: {response["metrics"]}")
            self.drone["metrics"] = response["metrics"]

        updates = {
            "telemetry": telemetry_update,
            "final_telemetry": final_telemetry_update,
            "status": crash_update,
            "metrics": metrics_update,
        }

        for key in updates:
            if key in response:
                updates[key]()
