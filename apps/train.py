import numpy as np
import json
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from apps.nltk_utils import bag_of_words, tokenize, stemmingIndo, case_folding, clean_punct, stopwords_removal
from apps.model import NeuralNet
from sklearn.feature_extraction.text import CountVectorizer

with open('apps/intents.json', 'r') as f:
    intents = json.load(f)

all_words = [] # Semua Kata 
tags = [] # Tag 
patternresponse = [] # udh tokenize sm label
all_pattern_done = [] # semua kalimat udh di preprocessing

# loop through the tags (classes)
for intent in intents['intents']:
    tag = intent['tag']
    tags.append(tag)
    for pattern in intent['patterns']:
        pattern = case_folding(pattern)
        pattern = clean_punct(pattern)
        words = tokenize(pattern)
        words = stopwords_removal(words)
        w = [stemmingIndo(w) for w in words]
        all_words.extend(w)
        patternresponse.append((w, tag))
        all_pattern_done.append(w)

# stem and lower each word
ignore_words = ['?', '.', '!', ',', '-']
# all_words = [stemmingIndo(w) for w in all_words if w not in ignore_words]
# remove duplicates and sort
all_words = sorted(set(all_words))
tags = sorted(set(tags))
all_pattern_done = [ ' '.join(lst) for lst in all_pattern_done ]

print(len(all_pattern_done), "patterns")
print(len(tags), "tags:", tags)
print(len(all_words), "unique stemmed words:", all_words)

# create training data
X_train = []
Y_train = []

for (pattern_sentence, tag) in patternresponse:
        label = tags.index(tag)
        Y_train.append(label)

vectorizer = CountVectorizer(max_features = 1000, dtype=np.float32)
X = vectorizer.fit_transform(all_pattern_done)

X_train = X.toarray()
Y_train = np.array(Y_train)

# Hyper-parameters
num_epochs = 400
batch_size = 16
learning_rate = 0.004
input_size = len(X_train[0])
hidden_size = 22
output_size = len(tags)
dropout = 0.1

print(input_size, output_size)

class ChatDataset(Dataset):

    def __init__(self):
        self.n_samples = len(X_train)
        self.x_data = X_train
        self.y_data = Y_train

    # support indexing such that dataset[i] can be used to get i-th sample
    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    # we can call len(dataset) to return the size
    def __len__(self):
        return self.n_samples

dataset = ChatDataset()
train_loader = DataLoader(dataset=dataset,
                          batch_size=batch_size,
                          shuffle=True,
                          num_workers=0)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = NeuralNet(input_size, hidden_size, output_size).to(device)

# Loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

# Train the model
for epoch in range(num_epochs):
    for (words, labels) in train_loader:
        words = words.to(device)
        labels = labels.to(dtype=torch.long).to(device)

        # Forward pass
        outputs = model(words)
        # if y would be one-hot, we must apply
        loss = criterion(outputs, labels)

        # Backward and optimize
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    if (epoch+1) % 100 == 0:
        print (f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')


print(f'final loss: {loss.item():.4f}')

data = {
"model_state": model.state_dict(),
"input_size": input_size,
"hidden_size": hidden_size,
"output_size": output_size,
"all_words": all_words,
"tags": tags
}

FILE = "apps/data.pth"
torch.save(data, FILE)
print(f'training complete. file saved to {FILE}')