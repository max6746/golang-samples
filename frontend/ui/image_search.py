"""
Copyright 2023 Google. This software is provided as-is, without warranty or representation for any use or purpose.
Your use of it is subject to your agreement with Google.
"""

import html as htmlesc
from frontend.ui.base import UI


class ImageSearchUI(UI):
    """
    Creates a image editor UI with ability to specify Mask.

    User can provide prompt or, upload an image. When user clicks Search
    button, a HTTP POST request is made to the api_endpoint. The request contains JSON paylod with following
    parameters:

        {
            "prompt" : "user specified prompt",
            "neg_prompt_input" : "user specified negative prompt",
            "image: "Image string in base64 format",
            "image_width" : "Image height",
            "image_height" : "Image width",
        }

    The HTTP reponse contains JSON with following parameters:

        {
            "images": [
                "base64 of image 1",
                "base64 of image 2",
                "base64 of image n",
            ]
        }

    """

    def __init__(
        self, negative_prompt=False, api_endpoint: str = "http://localhost:5000/process"
    ):
        """

        :param negative_prompt: Toggle for negative prompt text box
        :param api_endpoint: API endpoint to be called
        :return:
        """

        # Initialize the superclass.
        UI.__init__(self)

        # Initialize Variables
        self.negative_prompt = negative_prompt
        self.api_endpoint = api_endpoint

    def html(self) -> str:
        """
        HTML for Image Editor UI
        :return: HTML fot the Image Editor UI
        """

        html = """
        
                    <div class="row">
                        <div class="col-12"><h4>EzyAI Reverse Lookup Search</h4></div>
                    </div>
                    
                    <div class="row">
                        <div class="col-12"><p><i>Choose an image file for finding similar products or Enter a prompt and click "Search".</i></p></div>
                    </div>    
                    
                    <div class="row">
                        <div class="col-12">&nbsp;</div>
                    </div>        
                        
                    
                    <div class="row">
                        <div class="col-3">
                        	<input type="file" accept="image/*" onchange="loadFile(event)">
                        </div>
                        <div class = "col-md-4">
                            <input class="form-control form-control-dark" type="text" placeholder="Prompt" aria-label="Prompt" id="user_input" required>
                        </div>
                        <div class = "col-md-4">
                        """
        if self.negative_prompt:
            html += """ <input class="form-control form-control-dark" type="text" placeholder="Negative Prompt(Optional)" aria-label="Negative Prompt" id="neg_prompt_input" optional>"""
        else:
            html += """ <input class="form-control form-control-dark" type="text" placeholder="Negative Prompt(Optional)" aria-label="Negative Prompt" id="neg_prompt_input" optional hidden>"""

        html += """
                        </div>
                        <div class="col-1">
                        	<ul class="navbar-nav px-3">
			                    <li class="nav-item text-nowrap">
			                    <button type="button" class="btn btn-primary" id="gen_button" onclick="process_user_input();">
			                        Search
			                    </button>
			                    </li>
			                </ul>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-12"><hr></div>
                    </div>
                    
                    <div class="row">
                        <div class="col-12">
                        	<img id="scream" src="" hidden>
							<canvas id="canvas" width=800 height=600></canvas>               	
                        </div>
                    </div>
                    
                    <!-- Wait -->
                    <div class ="row" id="search_wait">
                        <div class="row">
                            <div class="col-12">&nbsp;</div>
                        </div>
                        <div class="row">
                            <div class="col-12">&nbsp;</div>
                        </div>
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
                    
                    <div id = "results">
                        <div class="row">
                            <div class="col-12">&nbsp;</div>
                        </div>
                        
                        <div class="row">
                            <div class="col-12"><h5>Results</h5></div>
                        </div>
                        
                        <div class="row">
                            <div class="col-12"><hr></div>
                        </div>
                        
                        <div id="result_images">
                            
                        </div>
                        
                    </div>
        """

        return html

    def js(self) -> str:
        """
        returns js for the Image Editor UI.
        - onApplicationReady() function is called at document ready. It must be declared.
        :return: JS for the Image Editor UI.
        """

        js = (
            """
            // get references to the canvas and context
			var canvas = document.getElementById("canvas");
			var ctx = canvas.getContext("2d");
			var img = document.getElementById("scream");
			var base64String;
			drawImage();
   
            //Document Ready Function
            function onApplicationReady()
            {
                var results = document.getElementById('results');
                results.style.display = "none";
                
                var search_wait = document.getElementById('search_wait');
                search_wait.style.display = "none";
            }
			//Function to upload image and convert to base64
			var loadFile = function(event) {
	            var image = document.getElementById('scream');
	            image.src=URL.createObjectURL(event.target.files[0]);
	            image.onload = function () {
	            	drawImage();
	            }
                //Convert to base64
	            let reader = new FileReader();
	            reader.onload = function () {
	              	base64String = reader.result.replace("data:", "").replace(/^.+,/, "");
	            }
	            reader.readAsDataURL(event.target.files[0]);
          	};
			function drawImage() {
				canvas.style.height = img.height;
				canvas.style.width = img.width;
				canvas.height = img.height;
				canvas.width = img.width;
                
                //By default set the whole image as mask
                endX = img.width;
                endY = img.height;
				ctx.clearRect(0, 0, canvas.width, canvas.height);
				ctx.drawImage(img, 0, 0);
				// style the context
				ctx.strokeStyle = "blue";
				ctx.lineWidth = 2;
			}
   
            function process_user_input()
            {
                var user_input = document.getElementById("user_input").value;
                var neg_prompt_input = document.getElementById("neg_prompt_input").value;
                
                if (!base64String && !user_input ){
                    alert("Please upload an image or provide the prompt");
                    return;
                }
                if (base64String && user_input ){
                    alert("Either an image or prompt should be provided, Not both");
                    return;
                }
                if(!base64String){
                    base64String = ""
                }
                if(!user_input){
                    user_input = ""
                }
                var results = document.getElementById('results');
                results.style.display = "none";
                
                var search_wait = document.getElementById('search_wait');
                search_wait.style.display = "block";
                
                document.getElementById("gen_button").disabled = true;
                document.getElementById("user_input").disabled = true;              
                document.getElementById("neg_prompt_input").disabled = true;
                
                post_request(user_input, neg_prompt_input);
                
            }
            
            function post_request(user_input, neg_prompt_input)
            {
               
                fetch( \""""
            + self.api_endpoint
            + """\", {
                method: "POST",
                body: JSON.stringify({
                    prompt: user_input,
                    image: base64String,
                    image_width: canvas.width,
                    image_height: canvas.height,
                    neg_prompt_input: neg_prompt_input,
                }),
                headers: {
                    "Content-type": "application/json; charset=UTF-8"
                }
                })
                .then((response) => response.json())
                .then((json) => process_json(json));
                
            }
            
            function process_json(generated_images)
            {
                
                var results = document.getElementById('results');
                results.style.display = "block";
                
                var result_images = document.getElementById('result_images');
                result_images.innerHTML = "";
                
                for (image_item in generated_images.images) {
                result_images.innerHTML += generared_image_html(generated_images.images[image_item]); 
                }
                
                var search_wait = document.getElementById('search_wait');
                search_wait.style.display = "none";
                
                document.getElementById("gen_button").disabled = false;
                document.getElementById("user_input").disabled = false;
                document.getElementById("neg_prompt_input").disabled = false;
            }
            
            function generared_image_html(image)
            {
                var t_html =  "<div class='row'>";
                t_html += "<div class='col-md-12'>"; 
                t_html += "<img src='data:image/png;base64, " + image + "' />"; 
                t_html += "<br>"; 
                t_html += "</div>"; 
                t_html += "</div>"; 
                  
                return t_html;        
            }
			
        """
        )

        return js

    def css(self) -> str:
        """
        returns CSS required for the Image Editor UI.

        :return: CSS for the Image Editor UI.
        """

        css = """
        canvas{
			  border: 1px solid gray;
			  
			}        
        """
        return css
