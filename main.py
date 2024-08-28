"""
Copyright 2023 Google. This software is provided as-is, without warranty or representation for any use or purpose.
Your use of it is subject to your agreement with Google.
"""

from __future__ import annotations


import asyncio
import threading
import os
import time
from fastapi import FastAPI
from hypercorn.asyncio import serve
from hypercorn.config import Config
from starlette.staticfiles import StaticFiles
from starlette.routing import Route
from starlette.schemas import SchemaGenerator
import vertexai

from logger.logging import Logger
from router.json import JSONEndPoint
from router.ui import UIEndPoint
import config


# initializing configurations
conf = config.Config()

# vertex ai sdk intitialization
vertexai.init(project=conf.PROJECT_ID, location=conf.LOCATION)

#####################################################
# EXAMPLE: Import router endpoints. Add/Update/Delete as necessary.
#####################################################

__all__ = ["Server"]

# Create logger object
logger = Logger(__name__)


class Server:
    """
    FastAPI based server to expose endpoints for the application
    """

    def __init__(self, address: str = "0.0.0.0", port: int = 5000) -> None:
        """
        Initializes Server object

        :param address: Address to bind Server on. Deafult is 0.0.0.0
        :param port: Port to bind Server on. Default is 5000.

        :return: None
        """

        # Initialize object variables
        self.address = address
        self.port = port

        # Initialise API documentation download
        self.apis = SchemaGenerator(
            {"openapi": "3.0.0", "info": {"title": "API Endpoints", "version": "1.0"}}
        )

        # Initialize thread context to serve requests using threads
        self._thread = None
        self._stop_thread_event = None

        # Create FastApi app
        self._app = self._create_app()

        # Set initial state of the server
        self.started = False

    def _create_app(self) -> FastAPI:
        """
        Create the WebServer with HTTP and Websocket Routes

        :return: FastAPI App
        """

        # List to save different routes
        routes = []

        # Route to download API endpoints availble in OpenAPI format
        routes.append(Route("/apis", endpoint=self.dump_apis, include_in_schema=False))

        #####################################################
        # EXAMPLE: UI and JSON routers. Add/Update/Delete as necessary.
        routes.append(Route("/", UIEndPoint().get_request))
        routes.append(
            Route("/process", JSONEndPoint().get_request, methods=["GET", "POST"])
        )
        #####################################################

        # Create a FastApp App, add the routes
        app = FastAPI(routes=routes)

        #####################################################
        # EXAMPLE: Webpage mount static files if Web interface also required. Required for Webpage.
        # Add/Update/Delete as necessary.
        static_dir = os.path.join(os.path.dirname(__file__), "frontend/static")
        app.mount("/static", StaticFiles(directory=static_dir), name="static")
        #####################################################

        return app

    async def _start(self) -> None:
        """
        Background internal function to start Server. This function runs as a coroutine.

        :return: None
        """

        # Config for Hypercorn server.
        config = Config.from_mapping(
            {
                "accesslog": "-",
                "errorlog": "-",
                "loglevel": None,
                "logconfig": None,
                "logconfig_dict": {
                    "root": {},
                    "loggers": {},
                    "handlers": {},
                    "formatters": {},
                    "incremental": True,
                    "version": 1,
                },
            }
        )
        config.bind = [f"{self.address}:{self.port}"]

        # Event to gracefully stop the server. When thread stops, it is set
        shutdown_event = asyncio.Event()

        # Start Server inside an event loop
        server_task = asyncio.create_task(
            serve(self._app, config, shutdown_trigger=shutdown_event.wait)
        )

        logger.info(f"Server listening on http://{self.address}:{self.port}")

        # Run forever until the self._stop_thread_event is set. If stop thread event is set, then set
        # the shutdown_event which stops the server_task. This results in graceful shutdown.
        try:
            await asyncio.get_event_loop().run_in_executor(
                None, lambda: self._stop_thread_event.wait()
            )
        finally:
            shutdown_event.set()
            await server_task

    def start(self) -> None:
        """
        Start the server ascynchronously.

        :return: None
        """

        # Create a thread and run webserver inside it inside an event loop. _stop_threading_event
        # is used to gracefully shutdown the thread.
        self._stop_thread_event = threading.Event()
        self._thread = threading.Thread(
            target=asyncio.run, args=(self._start(),), name="WEBSERVER"
        )
        self._thread.start()
        self.started = True

    def stop(self) -> None:
        """
        Stop the server gracefully.

        :return: None
        """

        # Set the _stop_thread_event which triggers the coruutine hosting webserver to stop.
        self._stop_thread_event.set()

        # Wait for thread to terminate
        if self._thread is not None:
            self._thread.join()

        self.started = False

    def dump_apis(self, request):
        """
        Return available APIs in OpenAPI format
        """
        return self.apis.OpenAPIResponse(request=request)


if __name__ == "__main__":
    #####################################################
    # Example: Add/Update/Delete as required

    # Create a server and start it
    ws = Server()
    ws.start()

    # Sample code to keep the server running
    i = 0

    while i < 1000:
        time.sleep(3)
        i += 1
        continue

    # Stop the server
    ws.stop()

    #####################################################
