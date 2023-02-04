import random
import json
import torch
from apps.model import NeuralNet
from apps.nltk_utils import bag_of_words, tokenize, stem, case_folding, clean_punct, stopwords_removal, correction

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('apps/intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
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

bot_name = "Bot"

def get_response(msg):
    sentence = case_folding(msg)
    sentence = clean_punct(sentence)
    sentence = tokenize(sentence)
    sentence = [stem(w) for w in sentence]
    words = []
    for word in sentence:
        word = correction(word)
        words.append(word)

    # msg = case_folding(msg)
    # msg = clean_punct(msg)
    # sentence = tokenize(msg)
    # sentence = [stem(w) for w in sentence]

    # words = []
    # for word in sentence:
    #     word = correction(word)
    #     words.append(word)

    X = bag_of_words(words, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    print(prob)
    if prob.item() > 0.5:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                return random.choice(intent['responses'])

    return "Maaf, saya tidak mengerti pertanyaan anda..."