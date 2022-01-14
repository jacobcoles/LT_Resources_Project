# LT_Resources_Project
Follow these instructions to get it working :)

## Python server
- In terminal/bash navigate to /python_server (which is in my project folder)
- Run the following lines:
pip install -U flask-cors
pip install flask lxml bs4
export FLASK_APP=parser_python_server
flask run
- Now hopefully the server should be running!


## Chrome extension
- Go to the chrome extensions page at chrome://extensions/
- Enable developer options using the switch in the top right
- Click "Load unpacked near the upper left"
- Navigate to the folder named LT_extension (in my project folder)
- Load it in! It should appear if you click on your chrome extensions in the upper right