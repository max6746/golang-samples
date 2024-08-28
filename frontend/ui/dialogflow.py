"""
Copyright 2023 Google. This software is provided as-is, without warranty or representation for any use or purpose.
Your use of it is subject to your agreement with Google.
"""

from frontend.ui.base import UI
import html as htmlesc


class DialogFlow(UI):
    """
    Generates a UI that has a chat popup. The chat pop up has a send buttom that can be used to send user
    text to the endpoint and get a response back and display it to the user.

    When user clicks the send button a HTTP POST Request is sent to API endpoint in JSON format:

        {
            "user_input": "user text from the chat"
        }

    Response is expected in JSON having following format and it is then returned to user:

        {
            "bot_response": "response from the application"
        }
    """

    def __init__(
        self,
        bot_name: str = "Vyommitra",
        helper_html: str = "",
        project_id: str = "",
        agent_id: str = "",
    ):
        """

        :param bot_name: Name of the bot
        :param helper_html: Text displayed on webpage to provide more details about the bot
        :param api_endpoint: API endpoint to be called

        :return:
        """

        # Required to initialize the superclass. Creates the _ws and data.
        UI.__init__(self)

        # Initialize Variables
        self.project_id = project_id
        self.agent_id = agent_id
        self.bot_name = bot_name
        self.helper_html = helper_html

    # Returns the html to the server

    def html(self) -> str:
        """
        HTML for chat bot

        :return: HTML for chat bot
        """

        html = """
        <div class ="row">
            <div class = "col-md-12 text-center">
                <h1>&nbsp;</h1>
                <h3>{bot_name} is here to help! </h3>
                <p>&nbsp;</p>
                <hr>
                <h1>&nbsp;</h1>
            </div>
        </div>
        <div class ="row">
            <div class = "col-md-1"></div>
            <div class = "col-md-3">
                <p>
                    <b>Experience the power of Google GenAI Language model through Conversations.</b>
                    <br/></br>
                    <img src='static/img/tick.png' width='30' />Help customers and employees quickly get relevant information<br/></br>
                    <img src='static/img/tick.png' width='30' />Combine enterprise data with Google search and conversational AI<br/></br>
                    <img src='static/img/tick.png' width='30' />Build generative AI experiences with text, voice, images, and video<br/></br>
                    <img src='static/img/tick.png' width='30' />Enjoy enterprise grade scalability, data privacy, security, and controls<br/></br>
                </p>
            </div>
            <div class = "col-md-1"></div>
            <div class = "col-md-3">
                {helper_html}
            </div>
            <div class = "col-md-4">
            <div class="d-flex justify-content-center container mt-5">
                <div class="wrapper">
                    <div class="d-flex align-items-center text-right justify-content-end">
                    <script src="https://www.gstatic.com/dialogflow-console/fast/df-messenger/prod/v1/df-messenger.js"></script>
                    <df-messenger project-id={project_id} agent-id={agent_id} language-code="en">
                    <df-messenger-chat-bubble chat-title={bot_name}> </df-messenger-chat-bubble> 
                    </df-messenger>
                    </div>
                </div>
            </div> <!-- col -->
        </div> <!-- row -->
            
        """.format(
            bot_name=self.bot_name,
            helper_html=self.helper_html,
            project_id=self.project_id,
            agent_id=self.agent_id,
        )

        return html

    def css(self) -> str:
        """
        returns CSS required for the chat bot

        :return: CSS for the chat bot
        """

        css = """
                body{
                background:#E5E8E8;
                }

                ::-webkit-scrollbar {
                    width: 10px
                }

                ::-webkit-scrollbar-track {
                    background: #eee
                }

                ::-webkit-scrollbar-thumb {
                    background: #888
                }

                ::-webkit-scrollbar-thumb:hover {
                    background: #555
                }
                
                df-messenger {
                        z-index: 999;
                        position: fixed;
                        bottom: 16px;
                        right: 16px;
                        --df-messenger-chat-window-height: 800px;
                        --df-messenger-chat-window-width: 600px;
                        --df-messenger-table-border-radius:1;
                        --df-messenger-table-even-background:#C0C0C0;
                        --df-messenger-table-odd-background:#FFFFFF;
                }

                .wrapper {
                    right: 70px;
                    width: 400px;
                    height: 500px;
                    position: fixed;
                    background-color: #E5E8E8
                }

                .main {
                    background-color: #eee;
                    width: 400px;
                    position: relative;
                    border-radius: 8px;
                    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
                    padding: 6px 0px 0px 0px
                }

                .scroll {
                    overflow-y: scroll;
                    scroll-behavior: smooth;
                    height: 500px
                }

                .img1 {
                    border-radius: 50%;
                }

                .name {
                    font-size: 12px
                }

                .msg {
                    background-color: #fff;
                    font-size: 16px;
                    padding: 5px;
                    border-radius: 5px;
                    font-weight: 500;
                    color: #3e3c3c
                }

                .between {
                    font-size: 12px;
                    font-weight: 500;
                    color: #a09e9e
                }

                .navbar {
                    border-bottom-left-radius: 8px;
                    border-bottom-right-radius: 8px;
                    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)
                }

                .form-control {
                    font-size: 16px;
                    font-weight: 400;
                    width: 100%;
                    height: 30px;
                    border: none
                }

                form-control: focus {
                    box-shadow: none;
                    overflow: hidden;
                    border: none
                }

                .form-control:focus {
                    box-shadow: none !important
                }

                .icon1 {
                    color: #7C4DFF !important;
                    font-size: 18px !important;
                    cursor: pointer
                }

                .icon2 {
                    color: #512DA8 !important;
                    font-size: 18px !important;
                    position: relative;
                    left: 8px;
                    padding: 0px;
                    cursor: pointer
                }

                .icondiv {
                    border-radius: 50%;
                    width: 15px;
                    height: 15px;
                    padding: 2px;
                    position: relative;
                    bottom: 1px
                }
        
        """

        return css
