**Full-stack XAI app:**
- full-stack application to run LLMs locally,
- get output and explore attention patterns with visualisation,
- interactive tools and statistical methods (mean/median distribution, matrix)
- Backend: Python, Flask, Poetry, Transformers (AutoModelForCausalLM, AutoTokenizer), torch, NumPy
- Frontend: HTML/CSS, JavaScript
- Tested LLMs on interpreting raw attention data and got positive results with short inputs.

--
**Quickstart**

git clone [https://github.com/Krasnomakov/openMaze_XAI](https://github.com/Krasnomakov/openMaze_XAI.git)

cd openMaze_XAI/iter_2/Explainability/attention

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

Parts of the code copied from https://github.com/mattneary/attention
