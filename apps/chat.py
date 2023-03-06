import random
import json
import torch
from apps.model import NeuralNet
from apps.nltk_utils import bag_of_words, tokenize, case_folding, clean_punct, stopwords_removal, correction, de_tokenize, stemmingIndo
from apps.train import vectorizer

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

bot_name = "Bot"

def get_response(msg):
    sentence = case_folding(msg)
    sentence = clean_punct(sentence)
    words = tokenize(sentence)
    words = stopwords_removal(words)

    wordss = []
    for w in words:
        w = correction(w)
        wordss.append(w)

    w = [stemmingIndo(w) for w in wordss]    

    X = vectorizer.transform([de_tokenize(w)])
    X = X.toarray()
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]
    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]   

    print(prob)
    if prob.item() > 0.8:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                return random.choice(intent['responses'])

    return "Maaf, saya tidak mengerti pertanyaan anda..."