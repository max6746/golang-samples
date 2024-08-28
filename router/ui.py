"""
Copyright 2023 Google. This software is provided as-is, without warranty or representation for any use or purpose.
Your use of it is subject to your agreement with Google.
"""

import os

from fastapi.templating import Jinja2Templates
from frontend.ui.base import UI
from logger.logging import Logger

__all__ = ["UIEndPoint"]

# Create logger object
logger = Logger(__name__)


class UIEndPoint:
    # Initialise variables
    def __init__(self):
        """
        :return:
        """

        ##################################################
        # EXAMPLE: Update to UI subclass as required
        self.ui = UI()
        ##################################################

        template_dir = os.path.join(os.path.dirname(__file__), "../frontend/templates")
        self.templates = Jinja2Templates(directory=template_dir)

    async def get_request(self, request):
        """
        responses:
            200:
                description: UI for demo. ### Update as required
        """

        # Log request for debugging
        logger.debug(f"HTTP Request - ID: {request.id}  Method: {request.method}")

        # Get data from the UI
        html = str(self.ui.html())
        css = str(self.ui.css())
        css_references = str(self.ui.css_references())
        js = str(self.ui.js())
        js_references = str(self.ui.js_references())

        return self.templates.TemplateResponse(
            "base.html",
            {
                "request": request,
                "html": html,
                "css": css,
                "css_references": css_references,
                "js": js,
                "js_references": js_references,
            },
        )
