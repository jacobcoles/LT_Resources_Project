# LT_Resources_Project

In this project we create a web-extension which does word replacement for prepositions on Wikipedia. We have a fixed vocabulary in the code, from which the words on Wikipedia are replaced. Note that it was designed for use with Wikipedia, so it might have to be updated so that it plays nicely with other sites (basically how it processes the HTML elements). This is a proof of concept. 

This project consists of two parts:
- A chrome-extension (front-end) which works in the chrome browser. Basically just displays some HTML. 
- A python (back-end) server which communicates with the chrome extension to deliver the word replacements. (or rather, new HTML code to be displayed in the browser via the chrome extension). 

The chrome (web-browser) extension is adapted from the example given on https://developer.chrome.com/docs/extensions/mv3/getstarted/. It is quite rough and includes extra code that may not be used in my project. (Could be deleted). 

The python server retreives the website HTML from the chrome extension (via a POST request), uses the Sparv API to get linguistic information, modifies the HTML, then returns the new HTML to the chrome extension which then displays it. Utlimately the python server does most of the processing, and the chrome extension is for the interface/web-browser integration. 

There is a bug with how the python server retreives and re-compiles the HTML. It seems to delete one of the HTML elements and I'm not sure why (usually corresponds to the first paragraph on a wikipedia page). It think it's something to do with either the 'etree' component or the 'BeautifulSoup' component (if it's not an error in my code). Can look further into this if needed/requested. 

## Follow these instructions to get it working :)

### Python server
- In terminal/bash navigate to /python_server (which is in my project folder)
- Run the following lines:
    
    pip install -U flask-cors
    pip install flask lxml bs4
    export FLASK_APP=parser_python_server
    flask run
    
- Now hopefully the server should be running!


### Chrome extension
- Go to the chrome extensions page at chrome://extensions/
- Enable developer options using the switch in the top right
- Click "Load unpacked near the upper left"
- Navigate to the folder named LT_extension (in my project folder)
- Load it in! It should appear if you click on your chrome extensions in the upper right


Let me know if you have any problems :)
