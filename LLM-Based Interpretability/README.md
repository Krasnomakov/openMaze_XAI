# LLM-Based Interpretability

This directory contains backend components for interpreting the outputs of Large Language Models (LLMs). It is divided into two main parts: `gpt4backend` and `alterVectorDb`.

## gpt4backend

This component is responsible for processing text data to be used with the GPT-4 model.

### Files

-   `convertTxtToJson.py`: Converts text files to JSON format.
-   `gpt4ReadFile.py`: Reads files for processing with GPT-4.
-   `measureTokens.py`: Measures the number of tokens in a text file.
-   `user 0.txt`: Sample user data.
-   `attention_data.json`: Sample attention data.

## alterVectorDb

This component provides a data server and scripts to interact with LLMs using Ollama. It is designed to provide interpretations of LLM outputs.

### Files

-   `dataServer.py`: A server to provide data for the LLMs.
-   `ollamaAgent.py`: An agent to interact with LLMs using the Ollama library.
-   `ollamaWithData.py`: A script to use Ollama with custom data.
-   `prompt.txt`: A sample prompt file.
-   `context_data.json`: Sample context data.
-   `templates/`: A directory containing templates for the data server. 