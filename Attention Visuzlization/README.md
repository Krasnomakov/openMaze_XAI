**Full-stack XAI app:**
- full-stack application to run LLMs locally,
- get output and explore attention patterns with visualisation,
- interactive tools and statistical methods (mean/median distribution, matrix)
- Backend: Python, Flask, Poetry, Transformers (AutoModelForCausalLM, AutoTokenizer), torch, NumPy
- Frontend: HTML/CSS, JavaScript
- Tested LLMs on interpreting raw attention data and got positive results with short inputs.


**Quickstart**

git clone [https://github.com/Krasnomakov/openMaze_XAI](https://github.com/Krasnomakov/openMaze_XAI.git)

cd openMaze_XAI/iter_2/Explainability/attention

poetry install 
poetry run flask --app attention run 


This app displays attention 
It allows user to input text 
It can output raw data on a separate page 

The idea was to use it with **LLM-Based Interpretability** backend and interpret it with GPT-4 or llama2/mistral.
However, at the time of testing the input exceeded GPT-4 capacity and local LLMs with vector DB were not productive enough on raw attention data (MacBook M1 10 core 16GB RAM). 

Yet, Claude AI sometimes managed to handle all input and analyse attention correctly, provide insights into weights and token values.

Demo: https://vimeo.com/907273901/2297f9efb1
---

#to allow automatic update of HTML without restarting the app

poetry add flask-debugtoolbar 

Remember to not use debug mode or the debug toolbar in a production setting. They're intended for development use only.

##

Parts of the code copied from https://github.com/mattneary/attention
