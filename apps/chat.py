import random
import json
import torch
from apps.model import NeuralNet
from apps.nltk_utils import tokenize, case_folding, clean_punct, stopwords_removal, correction, de_tokenize, stemmingIndo, bag_of_words

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('apps/intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "apps/data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

def get_response(msg):
    sentence = case_folding(msg)
    sentence = clean_punct(sentence)
    words = tokenize(sentence)
    print("after tokenize", words)
    words = stopwords_removal(words)

    wordss = []
    for w in words:
        w = correction(w)
        wordss.append(w)
    print("after spell checker", wordss)

    w = [stemmingIndo(w) for w in wordss]
    print("after stemming", w)

    X = bag_of_words(w, all_words)
    X = X.reshape(1, X.shape[0])
    # X = torch.from_numpy(X).to(device)
    # X = X.toarray()
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]
    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]   

    print(prob, tag)
    if prob.item() > 0.9:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                return random.choice(intent['responses'])
    elif prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                return f"Sepertinya jawaban yang cocok untuk pertanyaan kamu adalah {random.choice(intent['responses'])}"
        # Create a list of (probability, tag) pairs
        prob_tag_pairs = [(probs[0][i].item(), tags[i]) for i in range(len(tags))]

        # Sort the list in descending order based on probability
        prob_tag_pairs = sorted(prob_tag_pairs, reverse=True)

        # Print the top three sorted probabilities and tags
        # Create a string to store the top three sorted probabilities and tags
        top_three_text = ""
        for prob, tag in prob_tag_pairs[:3]:
            top_three_text += f"Probability: {prob}, Tag: {tag}\n"
        print(top_three_text)
        
    else:
        return "Maaf, saya tidak mengerti pertanyaan anda..."
            
    #  # Create a list of (probability, tag) pairs
    # prob_tag_pairs = [(probs[0][i].item(), tags[i]) for i in range(len(tags))]

    # # Sort the list in descending order based on probability
    # prob_tag_pairs = sorted(prob_tag_pairs, reverse=True)

    # # Print the sorted probabilities and tags
    # for prob, tag in prob_tag_pairs:
    #     print(prob, tag)

    # return "Maaf, saya tidak mengerti pertanyaan anda..."
    