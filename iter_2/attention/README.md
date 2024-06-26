poetry install 


poetry run flask --app attention run 

This app displays attention 
It allows user to input text 
It can output raw data on a separate page 

It uses partially the MIT licensed code by ....
More info in pyproject.toml file 

---
#to allow automatic update of HTML without restarting the app

poetry add flask-debugtoolbar 

Remember to not use debug mode or the debug toolbar in a production setting. They're intended for development use only.

##