from transformers import AutoModelForCausalLM, AutoTokenizer, GPT2Tokenizer, GPT2Model
import torch
import numpy as np

#code below is a quote with minor changes till """ sign, check readme.md for source

def aggregate_attention(attn):
    '''Extract average attention vector'''
    avged = []
    for layer in attn:
        layer_attns = layer.squeeze(0)
        attns_per_head = layer_attns.mean(dim=0)
        vec = torch.concat((
            # We zero the first entry because it's what's called
            # null attention (https://aclanthology.org/W19-4808.pdf)
            torch.tensor([0.]),
            # usually there's only one item in attns_per_head but
            # on the first generation, there's a row for each token
            # in the prompt as well, so take [-1]
            attns_per_head[-1][1:],
            # add zero for the final generated token, which never
            # gets any attention
            torch.tensor([0.]),
        ))
        avged.append(vec / vec.sum())
    return torch.stack(avged).mean(dim=0)

def heterogenous_stack(vecs):
    '''Pad vectors with zeros then stack'''
    max_length = max(v.shape[0] for v in vecs)
    return torch.stack([
        torch.concat((v, torch.zeros(max_length - v.shape[0])))
        for v in vecs
    ])

tokenizer = AutoTokenizer.from_pretrained('EleutherAI/pythia-410m')
model = AutoModelForCausalLM.from_pretrained('EleutherAI/pythia-410m')

def decode(tokens):
    '''Turn tokens into text with mapping index'''
    full_text = ''
    chunks = []
    for i, token in enumerate(tokens):
        text = tokenizer.decode(token)
        full_text += text
        chunks.append(text)
    return full_text, chunks

def get_completion(prompt):
    '''Get full text, token mapping, and attention matrix for a completion'''
    tokens = tokenizer.encode(prompt, return_tensors="pt")
    top_k = 2
    outputs = model.generate(
        tokens,
        max_new_tokens=50,
        output_attentions=True,
        return_dict_in_generate=True,
        early_stopping=True,
        length_penalty=-1,
        temperature =1.2,
        top_k=top_k,
    )
    sequences = outputs.sequences
    attn_m = heterogenous_stack([
        torch.tensor([
            1 if i == j else 0
            for j, token in enumerate(tokens[0])
        ])
        for i, token in enumerate(tokens[0])
    ] + list(map(aggregate_attention, outputs.attentions)))
    decoded, tokenized = decode(sequences[0])
    return decoded, tokenized, attn_m

def show_matrix(xs):
    matrix_str = ""
    for x in xs:
        line = ''
        for y in x:
            line += '{:.4f}\t'.format(float(y))
        matrix_str += line + '\n'
    return matrix_str

#"""end of the quote
        
def calculate_summary_statistics(attn_data, tokenized_words):
    """
    Calculate summary statistics for attention data.

    Args:
        attn_data (torch.Tensor): Attention data for a completion.
        tokenized_words (List[str]): Tokenized words corresponding to the tokens.

    Returns:
        dict: Summary statistics, e.g., mean attention value for each token.
    """
    summary_stats = {}
    for i, (token_attention, word) in enumerate(zip(attn_data, tokenized_words)):
        mean_attention = torch.mean(token_attention).item()
        summary_stats[f'Token_{i} - {word}'] = mean_attention

    return summary_stats

def calculate_attention_distribution(attention_data):
    """
    Calculate attention distribution for each token.

    Args:
        attention_data (dict): Attention data containing tokens, attn_indices, and attn_values.

    Returns:
        dict: Attention distribution data for each token.
    """
    tokens = attention_data['tokens']
    attn_indices = attention_data['attn_indices']
    attn_values = attention_data['attn_values']

    # Assuming each token has a unique index, create a mapping between tokens and their attention values
    # Initialize with all tokens and empty lists
    token_attention_mapping = {token: [] for token in tokens}

    # Populate the attention values for each token
    for (i, j), value in zip(attn_indices, attn_values):
        token_attention_mapping[tokens[i]].append(value)

    # Calculate mean attention for each token
    token_distribution_data = {}
    for token, attention_values in token_attention_mapping.items():
        if attention_values:
            mean_attention = sum(attention_values) / len(attention_values)
            token_distribution_data[token] = mean_attention

    return token_distribution_data


def calculate_attention_alignment(attention_data):
    """
    Calculate attention alignment across tokens.

    Parameters:
    - attention_data (dict): Attention data structure containing tokens, attn_indices, and attn_values.

    Returns:
    - attention_alignment_data (dict): Dictionary with tokens and mean attention alignment values.
    """
    try:
        if 'tokens' not in attention_data or 'attn_indices' not in attention_data or 'attn_values' not in attention_data:
            return {"error": "Missing key(s) in attention_data - 'tokens', 'attn_indices', or 'attn_values'"}

        tokens = attention_data['tokens']
        attn_indices = attention_data['attn_indices']
        attn_values = attention_data['attn_values']

        num_tokens = len(tokens)

        if num_tokens == 0:
            return {"error": "Empty list in attention_data - 'tokens'"}

        # Initialize a dictionary to store attention alignment values
        attention_alignment_data = {f'{tokens[i]}': 0.0 for i in range(num_tokens)}

        # Calculate mean attention alignment for each token
        for token_idx in range(num_tokens):
            alignment_sum = 0.0

            # Sum attention values across all indices
            for i in range(len(attn_indices)):
                if isinstance(attn_values[i], list) and token_idx < len(attn_values[i]):
                    alignment_sum += attn_values[i][token_idx]

            # Calculate mean attention alignment
            mean_alignment = alignment_sum / len(attn_indices)
            attention_alignment_data[f'{tokens[token_idx]}'] = mean_alignment

        return attention_alignment_data

    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}
    
    # Inside attention.py

def get_attention_details_for_token(attn_data, token_index):
    """
    Get detailed attention information for a specific token index.

    Args:
        attn_data (torch.Tensor): Attention data for a completion.
        token_index (int): Index of the token for which detailed attention information is needed.

    Returns:
        dict: Detailed attention information for the specified token index.
    """
    # Extract attention values for the given token index
    token_attention = attn_data[token_index].tolist()

    # You can add more details based on your requirements
    details = {
        'token_index': token_index,
        'attention_values': token_attention,
        # Add other details as needed
    }

    return details

def calculate_median_attention(attn_data, tokenized_words):
    """
    Calculate median attention for each token.

    Args:
        attn_data (torch.Tensor): Attention data for a completion.
        tokenized_words (List[str]): Tokenized words corresponding to the tokens.

    Returns:
        dict: Median attention values for each token.
    """
    median_stats = {}
    for i, (token_attention, word) in enumerate(zip(attn_data, tokenized_words)):
        # Convert token_attention to a PyTorch tensor
        token_attention_tensor = torch.tensor(token_attention)
        median_attention = torch.median(token_attention_tensor).item()
        median_stats[f'Token_{i} - {word}'] = median_attention

    return median_stats

