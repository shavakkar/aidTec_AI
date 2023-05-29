import random

import json
import nltk
import numpy as np
import pickle
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD

# Load intents data from JSON file
with open('intents.json') as file:
    intents = json.load(file)

# Preprocess the data
words = []
classes = []
documents = []
ignore_words = ['?', '!']

for intent in intents['intents']:
    for pattern in intent['patterns']:
        # Tokenize each word in the pattern
        w = nltk.word_tokenize(pattern)
        words.extend(w)
        # Add the pattern and associated class/tag to documents list
        documents.append((w, intent['tag']))
        # Add the class/tag to the classes list
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# Perform lemmatization and remove duplicates
words = [nltk.stem.WordNetLemmatizer().lemmatize(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))

# Save words and classes to files for future use
pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

# Create training data
training_data = []
output_empty = [0] * len(classes)

for doc in documents:
    bag = []
    pattern_words = doc[0]
    pattern_words = [nltk.stem.WordNetLemmatizer().lemmatize(word.lower()) for word in pattern_words]
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1
    training_data.append([bag, output_row])

# Shuffle the training data
random.shuffle(training_data)
training_data = np.array(training_data)

# Split the training data into X and y
X_train = list(training_data[:, 0])
y_train = list(training_data[:, 1])

# Build the model
model = Sequential()
model.add(Dense(128, input_shape=(len(X_train[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(y_train[0]), activation='softmax'))

# Compile the model
sgd = SGD(learning_rate=0.01,  momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

# Train the model
model.fit(np.array(X_train), np.array(y_train), epochs=200, batch_size=5, verbose=1)

# Save the trained model
model.save('chatbot_model.h5')
print('Model saved.')
