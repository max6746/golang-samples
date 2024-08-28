"""
Copyright 2023 Google. This software is provided as-is, without warranty or representation for any use or purpose.
Your use of it is subject to your agreement with Google.
"""

from frontend.ui.base import UI
import html as htmlesc


class ChatbotUI(UI):
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
        api_endpoint: str = "http://localhost:5000/process",
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
        self.api_endpoint = api_endpoint
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
                    <div class="d-flex align-items-center text-right justify-content-end"><img src='static/img/chat_main.png' width='150' onclick="toggle_chat_messages();"/></div>
                    <div class="main" id="chat_block">
                        <div class="px-2 scroll" id = "chat_messages">
                                            
                            <div class='d-flex align-items-center'>
                                <div class='text-left pr-1'><img src='static/img/chat1.png' width='30' class='img1' /></div>
                                <div class='pr-2 pl-1'> <span class='name'>{bot_name}</span>
                                    <p class='msg'>Hello, how can I help today?</p>
                                </div>
                            </div>
                            
                        </div>
                        <nav class="navbar bg-white navbar-expand-sm d-flex justify-content-between"> 
                            <input type="text number" name="user_input" id="user_input" class="form-control" placeholder="Type a message...">
                        </nav>
                    </div>
                </div>
            </div> <!-- col -->
        </div> <!-- row -->
            
        """.format(bot_name=self.bot_name, helper_html=self.helper_html)

        return html

    def js(self) -> str:
        """
        returns js for the chat bot.

        - onApplicationReady() function is called at document ready. It must be declared.

        :return: JS for the the chat bot
        """

        js = ""

        js += 'var botname = "' + htmlesc.escape(str(self.bot_name)) + '";\n'

        js += (
            """
        document.getElementById("user_input")
            .addEventListener("keyup", function(event) {
            event.preventDefault();
            if (event.keyCode === 13) {
                process_user_input();
            }
        });
        
        function onApplicationReady()
        {
            var x = document.getElementById('chat_block');
            x.style.display = "none";
        }
        
        function  process_user_input(){
            var chat_messages = document.getElementById("chat_messages");
            var user_input = document.getElementById("user_input").value;
            document.getElementById("user_input").value = "";
            chat_messages.innerHTML += human_chat_html(user_input);
            chat_messages.scrollTop = chat_messages.scrollHeight;
            post_request(user_input);
        }
        
        function bot_chat_html(user_input)
        {
            var t_html =  "<div class='d-flex align-items-center'>";
            t_html += "<div class='text-left pr-1'><img src='static/img/chat1.png' width='30' class='img1' /></div>";
            t_html += "<div class='pr-2 pl-1'> <span class='name'>";
            t_html += botname;
            t_html += "</span>";
            t_html += "<p class='msg'>";
            t_html += user_input;
            t_html += "</p></div></div>";
            
            return t_html;
        }
        
         function human_chat_html(user_input)
        {
            var t_html =  "<div class='d-flex align-items-center text-right justify-content-end '>";
            t_html += "<div class='pr-2'> <span class='name'>";
            t_html += "You";
            t_html += "</span><p class='msg'>";
            t_html += user_input;
            t_html += "</p></div><div><img src='static/img/chat2.png' width='30' class='img1' /></div></div>";
            
            return t_html;
        }
        
        function post_request(user_input)
        {
            
            fetch(\""""
            + self.api_endpoint
            + """\", {
            method: "POST",
            body: JSON.stringify({
                user_input: user_input,
            }),
            headers: {
                "Content-type": "application/json; charset=UTF-8"
            }
            })
            .then((response) => response.json())
            .then((json) => process_json(json));
            
        }
        
        function process_json(user_input)
        {
            var bot_response = user_input.bot_response;
            var chat_messages = document.getElementById("chat_messages");
            chat_messages.innerHTML += bot_chat_html(bot_response);
            chat_messages.scrollTop = chat_messages.scrollHeight;
        }
        
        function toggle_chat_messages()
        {
            console.log("Here");
            var x = document.getElementById('chat_block');
            
            if (x.style.display === "none") {
                x.style.display = "block";
            } else {
                x.style.display = "none";
            }          
        }
                        
        """
        )

        return js

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
