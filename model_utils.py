import torch
import os
import json
from neural_network import NeuralNet

def load_model(model_path):
    if not os.path.isfile(model_path):
        raise FileNotFoundError("Model file not found.")
    
    data = torch.load(model_path)
    model_state_dict = data["model_state_dict"]
    input_size = data["input_size"]
    hidden_size = data["hidden_size"]
    output_size = data["output_size"]
    all_words = data["all_words"]
    tags = data["tags"]

    model = NeuralNet(input_size, hidden_size, output_size)
    model.load_state_dict(model_state_dict)
    model.eval()

    # Load professor data
    with open('professors_data.json', 'r') as f:
        professors_data = json.load(f)

    return model, all_words, tags, professors_data
