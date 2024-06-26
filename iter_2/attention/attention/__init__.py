import traceback
from flask import Flask, request, render_template, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from .attention import get_completion, calculate_summary_statistics, calculate_attention_distribution, calculate_attention_alignment, get_attention_details_for_token, calculate_median_attention, show_matrix
import json

import numpy as np


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'asdsadsad332e32dsa././dasd'
app.config['TEMPLATES_AUTO_RELOAD'] = True

toolbar = DebugToolbarExtension(app)

# Initialize a variable to store user input
user_input_data = {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/process_input", methods=["POST"])
def process_input():
    user_input = request.form["user_input"]
    result, tokenized, attn_m = get_completion(user_input)
    sparse = attn_m.to_sparse()

    # Save attention data to a global variable for later retrieval
    global attention_data
    attention_data = {
        'tokens': tokenized,
        'attn_indices': sparse.indices().T.numpy().tolist(),
        'attn_values': sparse.values().numpy().tolist(),
        'attention_matrix': show_matrix(sparse.to_dense().numpy().tolist())  # Add the attention matrix
    }

    # Save attention data to a JSON file
    with open('attention_data.json', 'w') as file:
        json.dump(attention_data, file)

    # Save user input to the global variable
    global user_input_data
    user_input_data['user_input'] = user_input

    return jsonify({
        'tokens': tokenized,
        'attn_indices': sparse.indices().T.numpy().tolist(),
        'attn_values': sparse.values().numpy().tolist(),
        'attention_matrix': attention_data['attention_matrix']  # Include the attention matrix in the response
    })


@app.route("/display_attention")
def display_attention():
    global attention_data
    return render_template("attention.html", attention_data=attention_data)

# __init__.py

@app.route("/summary_statistics")
def summary_statistics():
    # Get user input from the global variable
    global user_input_data
    user_input = user_input_data.get('user_input', 'No input')

    # Process user input and get attention data
    result, tokenized, attn_m = get_completion(user_input)

    # Calculate summary statistics with token numbers and words
    summary_data = calculate_summary_statistics(attn_m, tokenized)

    # Pass the summary data, user input, and tokenized words to the template
    return render_template("summary_statistics.html", summary_data=summary_data, user_input=user_input, tokenized=tokenized)

@app.route("/attention_distribution")
def attention_distribution():
    global attention_data
    attention_distribution_data = calculate_attention_distribution(attention_data)
    return render_template("attention_distribution.html", attention_distribution_data=attention_distribution_data)

@app.route("/attention_alignment")
def attention_alignment():
    global attention_data
    attention_alignment_data = calculate_attention_alignment(attention_data)

    if "error" in attention_alignment_data:
        # Handle the error case
        return render_template("error.html", error_message=attention_alignment_data["error"])

    return render_template("attention_alignment.html", attention_alignment_data=attention_alignment_data)

@app.route("/get_attention_details")
def get_attention_details():
    try:
        token_index = int(request.args.get('token_index', 0))

        # Fetch detailed attention information based on the token index
        details = get_attention_details_for_token(attention_data, token_index)

        return jsonify(details)

    except Exception as e:
        error_message = f"Error fetching attention details: {str(e)}"
        # Print detailed error information to the server logs
        traceback.print_exc()
        return jsonify({"error": error_message}), 500
    
def get_attention_details_for_token(attention_data, token_index):
    try:
        tokens = attention_data.get('tokens', [])
        attn_indices = attention_data.get('attn_indices', [])
        attn_values = attention_data.get('attn_values', [])

        if not tokens or not attn_indices or not attn_values:
            return {"error": "Incomplete attention data"}

        if token_index < 0 or token_index >= len(tokens):
            return {"error": f"Invalid token index: {token_index}"}

        token = tokens[token_index]
        indices = attn_indices[token_index]
        values = attn_values[token_index]

        details = {"token": token, "indices": indices, "values": values}

        return details

    except Exception as e:
        error_message = f"Error fetching attention details for token index {token_index}: {str(e)}"
        # Print detailed error information to the server logs
        traceback.print_exc()
        return {"error": error_message}
    
@app.route("/median_attention")
def median_attention():
    global attention_data
    median_attention_data = calculate_median_attention(attention_data['attn_values'], attention_data['tokens'])
    return render_template("median_attention.html", median_attention_data=median_attention_data)

@app.route("/matrix")
def matrix():
    global attention_data
    return render_template("matrix.html", attention_matrix=attention_data.get('attention_matrix', 'No attention matrix available'), tokens=attention_data.get('tokens', []))

    
if __name__ == "__main__":
    app.run(port=5010, debug=True)
