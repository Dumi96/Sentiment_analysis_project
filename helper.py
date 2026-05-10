import numpy as np
import pandas as pd
import re
import string
import pickle
from nltk.stem import PorterStemmer

ps = PorterStemmer()

# Load model
with open('static/model/model.pickle', 'rb') as f:
    model = pickle.load(f)

# Stopwords
with open('static/model/corpora/stopwords/english', 'r') as file:
    sw = set(file.read().splitlines())

# Vocabulary
vocab = pd.read_csv('static/model/vocabulary.txt', header=None)
tokens = vocab[0].tolist()


def remove_punctuations(text):
    return text.translate(str.maketrans('', '', string.punctuation))


def preprocessing(text):
    text = text.lower()

    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'\d+', '', text)
    text = remove_punctuations(text)

    words = text.split()
    words = [w for w in words if w not in sw]
    words = [ps.stem(w) for w in words]

    return " ".join(words)


def vectorizer(text):
    vector = np.zeros(len(tokens))

    for word in text.split():
        if word in tokens:
            vector[tokens.index(word)] = 1

    return np.array([vector], dtype=np.float32)


def get_prediction(vectorized_text):
    prediction = model.predict(vectorized_text)[0]

    return "negative" if prediction == 1 else "positive"