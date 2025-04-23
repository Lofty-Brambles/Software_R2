import argparse
import sys
import os
import asyncio

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prantik_das.runners import all_runners
from prantik_das.client import Client


# @TODO improve this bit with more logging?
def main() -> None:
    """The drone runner method."""
    parser = argparse.ArgumentParser(description="Drone Simulator Server")
    parser.add_argument(
        "--runner", choices=["all"] + list(all_runners.keys()), help="Runner type"
    )
    parser.add_argument(
        "--url", default="ws://localhost:8765", help="URI to the server"
    )

    async def executable():
        args = parser.parse_args()
        tasks = all_runners.keys()
        if args.runner in all_runners:
            tasks = list(filter(lambda x: x == args.runner, tasks))
        tasks = list(
            map(lambda x: asyncio.create_task(Client(args.url, x).register()), tasks)
        )

        try:
            await asyncio.gather(*tasks)
        except asyncio.CancelledError:
            print("Client's corresponding server tasks were cancelled.")


    try:
        asyncio.run(executable())

    except KeyboardInterrupt:
        exit_log = f"The clients were killed by the user."
        print(exit_log)


if __name__ == "__main__":
    main()
