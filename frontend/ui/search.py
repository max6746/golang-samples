"""
Copyright 2023 Google. This software is provided as-is, without warranty or representation for any use or purpose.
Your use of it is subject to your agreement with Google.
"""

import html as htmlesc
from frontend.ui.base import UI


class SearchUI(UI):
    """
    Creates a geenrative search experience using GenAI.

    When user clicks search button a HTTP POST Request is sent to API endpoint in JSON format:

        {
            "query": "user query from the textbox"
        }

    Response is expected in JSON having following format and it is then rendered on the UI:

        {
            "summary": "Summary of the search generated through GenAI",
            "results": [
                {
                    "title": "Document 1",
                    "link": "http://localhost/document1.html",
                    "text": "This is document 1. This document talks about type 1 details. Type 1 is very important"
                },
                {
                    "title": "Document 2",
                    "link": "http://localhost/document2.html",
                    "text": "This is document 2. This document talks about type 1 details. Type 2 is very important"
                },
            ]
        }

    """

    def __init__(
        self,
        company_name: str = "Cymbal Solutions",
        default_question: str = "",
        api_endpoint: str = "http://localhost:5000/process",
    ):
        """

        :param company_name: Name of the compnay
        :param default_question: Default question for the query box
        :param api_endpoint: API endpoint to be called

        :return:
        """

        # Initialize the superclass.
        UI.__init__(self)

        # Initialize Variables
        self.company_name = company_name
        self.default_question = default_question
        self.api_endpoint = api_endpoint

    def html(self) -> str:
        """
        HTML for Generative Search UI

        :return: HTML for Generative Search UI
        """

        html = f"""
       
        <!-- Search bar -->
        
        <div class ="row">
            <div class = "col-md-2">
                <a class="navbar-brand col-sm-3 col-md-2 mr-0" href="#"><h3>{self.company_name}</h3></a>
            </div>
            <div class = "col-md-9">
                <input class="form-control form-control-dark" type="text" placeholder="Search" aria-label="Search" id="user_input" value="{self.default_question}">
            </div>
            <div class = "col-md-1">
                <ul class="navbar-nav px-3">
                    <li class="nav-item text-nowrap">
                    <button type="button" class="btn btn-primary" onclick="process_user_input();">
                        Search
                    </button>
                    </li>
                </ul>
            </div>
        </div>
        
        <div class ="row"><div class = "col-md-12"><hr></br></div></div>
    
        <!-- Wait -->
        <div class ="row" id="search_wait">
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
        <div class ="row" id="search_summary">
            <div class = "col-md-12">
                <div class="card">
                    <div class="card-body">
                        <div><b>Google GenAI Generated Answer</b></div>
                        </br>
                        <div id="search_summary_text"></div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class ="row"><div class = "col-md-12"></br></br></div></div>
            
        <!-- Search Results -->
        <div class ="row">
            <div class = "col-md-12" id="search_results">
            </div>
        </div>
            
        """

        return html

    def js(self) -> str:
        """
        returns js for Generative Search UI.

        - onApplicationReady() function is called at document ready. It must be declared.

        :return: JS for Generative Search UI
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
        
        function onApplicationReady()
        {
            var search_wait = document.getElementById('search_wait');
            search_wait.style.display = "none";
            
            var search_summary = document.getElementById('search_summary');
            search_summary.style.display = "none";
            
            var search_results = document.getElementById('search_results');
            search_results.style.display = "none";
        }
        
        function process_user_input()
        {
            var search_wait = document.getElementById('search_wait');
            search_wait.style.display = "block";
            
            var search_summary = document.getElementById('search_summary');
            search_summary.style.display = "none";
            
            var search_results = document.getElementById('search_results');
            search_results.style.display = "none";
            
            var user_input = document.getElementById("user_input").value;
            
            post_request(user_input);
            
        }
        
        function post_request(user_input)
        {
            
            fetch( \""""
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
        
        function process_json(search_results)
        {
            var search_summary_text = document.getElementById('search_summary_text');
            var search_items = document.getElementById('search_results');
            
            search_summary_text.innerHTML = search_results.summary;
            search_items.innerHTML = "";
            
            for (search_item in search_results.results) {
                search_items.innerHTML += search_item_html(search_results.results[search_item]); 
            }
            
            var search_wait = document.getElementById('search_wait');
            search_wait.style.display = "none";
            
            var search_summary = document.getElementById('search_summary');
            search_summary.style.display = "block";
            
            var search_results = document.getElementById('search_results');
            search_results.style.display = "block";
        }
        
        function search_item_html(search_item)
        {
            var t_html =  "<div>";
            t_html += "<p class='h5'><a href='";
            t_html += search_item.link;
            t_html += "' target='_blank'>";
            t_html += search_item.title;
            t_html += "</a></p><p>";
            t_html += search_item.text;
            t_html += "</p></br><div>";   
            
            return t_html;        
        }
       
        """
        )

        return js
