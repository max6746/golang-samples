"""
Copyright 2023 Google. This software is provided as-is, without warranty or representation for any use or purpose.
Your use of it is subject to your agreement with Google.
"""

import json
import random

from logger.logging import Logger
from starlette.responses import PlainTextResponse

__all__ = ["JSONEndPoint"]

# Create logger object
logger = Logger(__name__)


class JSONEndPoint:
    """
    Sample endpoint that can be replicated to meet any customer requirement. Update the code as required.
    request_body = await request.json() will capture the JSON query from the user and can be passed for further processing.
    response can be a dictionary which is converted to JSON and eventually to HTTP response using PlainTextResponse() function.
    """

    async def get_request(self, request) -> str:
        """
        responses:
            200:
                description: A json output. ### Update as required
                examples:
                    {"key1": "value1", "key2": "value2"} ### Update as required
        """

        # User request data
        request_body = await request.json()

        # Generate a random request ID for tracking
        request_id = random.randint(1000000, 9999999)

        # Log input request for debugging
        logger.debug(
            f"HTTP Request - ID: {request_id} URL: {request.url} Method: {request.method} JSON: {request_body}"
        )

        #####################################################
        # EXAMPLE: Update this section to perform any function and then return the response.
        response = {}
        #####################################################

        # Log response for debugging
        logger.debug(f"HTTP Response - ID: {request_id} JSON: {response}")

        return PlainTextResponse(json.dumps(response))
