"""
Copyright 2023 Google. This software is provided as-is, without warranty or representation for any use or purpose.
Your use of it is subject to your agreement with Google.
"""

import html as htmlesc
from frontend.ui.base import UI


class NL2SQLUI(UI):
    """
    Generates a UI that has a textbox to ask question in Natural Language and display generated SQL
    as well as queired data. W

    When user clicks the query button a HTTP POST Request is sent to API endpoint in JSON format:

        {
            "query": "user query from the textbox"
        }

    Response is expected in JSON having following format and it is then returned to user:

        {
            "summary": "generated SQL query",
            "table_html": "html containing the table data"

        }
    """

    # Class Constructor
    def __init__(
        self,
        company_name: str = "Cymbal Solutions",
        default_question: str = "",
        helper_html: str = "",
        api_endpoint: str = "http://localhost:5000/process",
    ):
        """

        :param company_name: Name of the compnay
        :param default_question: Default question for the query box
        :param helper_html: Text displayed on webpage to provide more details about the schema or anything else
        :param api_endpoint: API endpoint to be called

        :return:
        """

        # Required to initialize the superclass. Creates the _ws and data.
        UI.__init__(self)

        # Initialize Variables
        self.company_name = company_name
        self.helper_html = helper_html
        self.default_question = default_question
        self.api_endpoint = api_endpoint

    # Returns the html to the server
    def html(self) -> str:
        """
        HTML for the NL2SQL UI

        :return: HTML for the NL2SQL UI
        """

        # Global HTML
        html = f"""
       
        <!-- Query bar -->
        
        <div class ="row">
            <div class = "col-md-2">
                <a class="navbar-brand col-sm-3 col-md-2 mr-0" href="#"><h3>{self.company_name}</h3></a>
            </div>
            <div class = "col-md-8">
                <input class="form-control form-control-dark" type="text" placeholder="Query" aria-label="Query" id="user_input" value="{self.default_question}">
            </div>
            <div class = "col-md-1">
                <ul class="navbar-nav px-3">
                    <li class="nav-item text-nowrap">
                    <button type="button" class="btn btn-primary" onclick="process_user_input();">
                        Query
                    </button>
                    </li>
                </ul>
            </div>
            <div class = "col-md-1">
                <ul class="navbar-nav px-3">
                    <li class="nav-item text-nowrap">
                    <button type="button" class="btn btn-success" onclick="toggle_help();">
                        Help
                    </button>
                    </li>
                </ul>
            </div>
            
        </div>
        
        <div class ="row"><div class = "col-md-12"><hr></br></div></div>
    
        <!-- Help -->
        <div class ="row" id="nl2sql_helper_html">
            <div class = "col-md-12">
                <div class="card">
                    <div class="card-body">
                        {self.helper_html}
                    </div>
                </div>  
            </div>
        </div>
       

        <!-- Wait -->
        <div class ="row" id="nl2sql_wait">
            <div class = "col-md-12 text-center">
                <div class="spinner-grow text-primary" role="status">
                    <span class="sr-only"></span>
                </div>
                <div class="spinner-grow text-secondary" role="status">
                    <span class="sr-only"></span>
                </div>
                <div class="spinner-grow text-success" role="status">
                    <span class="sr-only"></span>
                </div>
                <div class="spinner-grow text-danger" role="status">
                    <span class="sr-only"></span>
                </div>
                <div class="spinner-grow text-warning" role="status">
                    <span class="sr-only"></span>
                </div>
                <div class="spinner-grow text-info" role="status">
                    <span class="sr-only"></span>
                </div>
            </div>
        </div>
       
        <!-- Generative box -->
        <div class ="row" id="nl2sql_summary">
            <div class = "col-md-12">
                <div class="card">
                    <div class="card-body">
                        <div><b>Google GenAI Generated Answer</b></div>
                        </br>
                        <div id="nl2sql_summary_text"></div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class ="row"><div class = "col-md-12"></br></br></div></div>
            
        <!-- nl2sql Results -->
        <div class ="row">
            <div class = "col-md-12" id="nl2sql_results">
            </div>
        </div>
            
        """

        return html

    # Returns the JS code for the application to the server.
    def js(self) -> str:
        """
        returns js for the the NL2SQL UI

        - onApplicationReady() function is called at document ready. It must be declared.

        :return: JS for the NL2SQL UI
        """

        js = ""

        js += 'var company_name = "' + htmlesc.escape(str(self.company_name)) + '";\n'

        js += (
            """
        document.getElementById("user_input")
            .addEventListener("keyup", function(event) {
            event.preventDefault();
            if (event.keyCode === 13) {
                process_user_input();
            }
        });
        
        function toggle_help()
        {
            var x = document.getElementById("nl2sql_helper_html");
            if (x.style.display === "none") {
                x.style.display = "block";
            } else {
                x.style.display = "none";
            }
        }
        
        function onApplicationReady()
        {
            var nl2sql_wait = document.getElementById('nl2sql_wait');
            nl2sql_wait.style.display = "none";
            
            var nl2sql_summary = document.getElementById('nl2sql_summary');
            nl2sql_summary.style.display = "none";
            
            var nl2sql_results = document.getElementById('nl2sql_results');
            nl2sql_results.style.display = "none";
            
            var nl2sql_helper_html = document.getElementById('nl2sql_helper_html');
            nl2sql_helper_html.style.display = "none";
        }
        
        function process_user_input()
        {
            var nl2sql_wait = document.getElementById('nl2sql_wait');
            nl2sql_wait.style.display = "block";
            
            var nl2sql_summary = document.getElementById('nl2sql_summary');
            nl2sql_summary.style.display = "none";
            
            var nl2sql_results = document.getElementById('nl2sql_results');
            nl2sql_results.style.display = "none";
            
            var nl2sql_helper_html = document.getElementById('nl2sql_helper_html');
            nl2sql_helper_html.style.display = "none";
            
            var user_input = document.getElementById("user_input").value;
            
            post_request(user_input);
            
        }
        
        function post_request(user_input)
        {
            
            fetch(\""""
            + self.api_endpoint
            + """\", {
            method: "POST",
            body: JSON.stringify({
                query: user_input,
            }),
            headers: {
                "Content-type": "application/json; charset=UTF-8"
            }
            })
            .then((response) => response.json())
            .then((json) => process_json(json));
            
        }
        
        function process_json(nl2sql_results)
        {
            var nl2sql_summary_text = document.getElementById('nl2sql_summary_text');
            var nl2sql_result = document.getElementById('nl2sql_results');
            
            nl2sql_summary_text.innerHTML = nl2sql_results.summary;
            nl2sql_result.innerHTML = nl2sql_results.table_html;
                        
            var nl2sql_wait = document.getElementById('nl2sql_wait');
            nl2sql_wait.style.display = "none";
            
            var nl2sql_summary = document.getElementById('nl2sql_summary');
            nl2sql_summary.style.display = "block";
            
            var nl2sql_results = document.getElementById('nl2sql_results');
            nl2sql_results.style.display = "block";
        }
        
        """
        )

        return js
