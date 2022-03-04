from transformers import AutoModelForSequenceClassification
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer
import numpy as np
from scipy.special import softmax
import csv
import torch
import urllib.request
import numpy as np

# Preprocess text (username and link placeholders)
# def preprocess(text):
#     new_text = []
#     for t in text.split(" "):
#         t = '@user' if t.startswith('@') and len(t) > 1 else t
#         t = 'http' if t.startswith('http') else t
#         new_text.append(t)
#     return " ".join(new_text)

task='sentiment'
MODEL = f"cardiffnlp/twitter-roberta-base-{task}"

labels=[]
mapping_link = f"https://raw.githubusercontent.com/cardiffnlp/tweeteval/main/datasets/{task}/mapping.txt"
with urllib.request.urlopen(mapping_link) as f:
    html = f.read().decode('utf-8').split("\n")
    csvreader = csv.reader(html, delimiter='\t')
labels = [row[1] for row in csvreader if len(row) > 1]

tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)
#tokenizer.save_pretrained(MODEL)
#model.save_pretrained(MODEL)


def get_sentiment(cleanedtweets):
    loader = torch.utils.data.DataLoader(cleanedtweets, batch_size=25)

    transformer_sentiments = []
    transformer_probs = []
    for tweets in loader:
        
        encoded_input = tokenizer(tweets, return_tensors = 'pt', padding = True)
        output = model(**encoded_input)
        scores = output[0].detach().numpy()
        scores = softmax(scores)
        indexes = np.argmax(scores, axis = 1)
        
        prob = [np.round(scores[no][index],2) for no,index in enumerate(indexes)] 
        sentiment = [labels[index] for index in indexes]
        
        transformer_sentiments.append(sentiment)
        transformer_probs.append(prob)
    
    transformer_sentiments = [senti for setoftweets in transformer_sentiments for senti in setoftweets]
    transformer_probs = [prob for setoftweets in transformer_probs for prob in setoftweets]
    transformer_result = [[sent,prob] for sent,prob in zip(transformer_sentiments, transformer_probs)]
    return transformer_result