"""
Copyright 2023 Google. This software is provided as-is, without warranty or representation for any use or purpose.
Your use of it is subject to your agreement with Google.
"""

__all__ = ["UI"]


class UI:
    """
    Base UI which needs to be inheritted by every UI
    """

    def html(self) -> str:
        """
        HTML for the Application

        :return: HTML for the Application
        """
        return ""

    def js(self) -> str:
        """
        JavaScript for the Application

        - onApplicationReady() function is called at document ready. It must be declared.

        :return: JavaScript for the Application
        """
        return_js = """
                        function  onApplictionReady(){
                        }
                    """
        return return_js

    def js_references(self) -> str:
        """
        Link to external JS references.

        :return: External JS references
        """
        return ""

    def css(self) -> str:
        """
        CSS for the application

        :return: CSS for the application
        """
        return ""

    def css_references(self) -> str:
        """
        CSS external references

        :return: CSS external references
        """
        return ""
