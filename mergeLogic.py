import json
import spacy
from transformers import pipeline
import nltk
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from nltk.corpus import stopwords
import csv
import webbrowser
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re

nltk.download('stopwords')
cache = "/cache"
nlp = spacy.load("en_core_web_sm")

zero_shot_pipeline = pipeline("zero-shot-classification", model="cache/zero-shot")

# Load the sentiment analysis pipeline
sentiment_analysis_pipeline = pipeline("sentiment-analysis", model="cache/sentiment")


def statement_analyzer(user):
    input_labels = ["review", "query"]
    result = zero_shot_pipeline(user, input_labels)
    predicted_label = result['labels'][0]
    return predicted_label

def sentiment_analyzer(user):
    sentiment_result = sentiment_analysis_pipeline(user)[0]
    label = sentiment_result['label']
    return label

def target(user):
    doc = nlp(user)
    objects = [token.text for token in doc if token.pos_ == "NOUN"]
    return objects

def dbTags(input_text):
    input_text = input_text.lower()
    doc = nlp(input_text)

    # Extract objects (direct objects) and events (occasions) from the sentence
    keywords = []
    dblabels = []
    for chunk in doc.noun_chunks:
        keywords.append(chunk.text)

    print(keywords)

    # Load the class mapping list from the JSON file
    json_file_path = "class_mapping_list.json"
    with open(json_file_path, "r") as json_file:
        class_mapping_list = json.load(json_file)

    # Convert each term into single word terms
    single_word_array = []
    for term in keywords:
        single_words = term.split()
        single_word_array.extend(single_words)
    print(single_word_array)

    mappings_for_word = []
    output = []
    # Iterate through each word in the normalized array
    for word in single_word_array:
        mappings_for_word = [
            mapping[1] for mapping in class_mapping_list if word.lower() == mapping[0].lower()]
        if not mappings_for_word:
            mappings_for_word.append(word)
        for i in mappings_for_word:
            output.append(i)
        mappings_for_word.clear()
    merged_list = []
    ##merging inner lists
    for item in output:
        if isinstance(item, list):
            merged_list.extend(item)
        else:
            merged_list.append(item)

    ##removing hum tum i we
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in merged_list if word.lower()
                      not in stop_words]
    return filtered_words


def linker(id):
    file = open("data/images.csv", "r")
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        if row["filename"] == id:
            return row['link']
        
def output(tags, num_recommendations=5):
    
    df = pd.read_csv('data/styles.csv',sep=',', usecols=range(9), engine='python')
    # Read the last column separately
    df = df.astype(str)
    df = df.fillna('')
    last_column = pd.read_csv('data/styles.csv', sep=',', usecols=[9], engine='python')


        # Create a DataFrame from the sample data
    details_columns = ['gender', 'masterCategory', 'subCategory',
                    'articleType', 'baseColour', 'season', 'year', 'usage']
    df['details'] = df[details_columns].apply(lambda row: ' '.join(row), axis=1)
    df['productDisplayName'] = last_column['productDisplayName']
    
    
    # Create a TF-IDF vectorizer and fit on outfit details

    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(df['details'])

    # Fit a Nearest Neighbors model on the TF-IDF matrix
    num_neighbors = 5  # Number of neighbors to consider
    nn_model = NearestNeighbors(n_neighbors=num_neighbors, metric='cosine')
    nn_model.fit(tfidf_matrix)
    
    ##recommendation logic
    input_text = ' '.join(tags)
    input_tfidf = tfidf_vectorizer.transform([input_text])

    # Find nearest neighbors based on cosine similarity
    distances, indices = nn_model.kneighbors(
        input_tfidf, n_neighbors=num_recommendations)

    recommended_indices = indices[0]
    recommended_outfits = df.iloc[recommended_indices]

    return recommended_outfits
    

app = Flask(__name__)
cors = CORS(app)

socketio = SocketIO(app,cors_allowed_origins="*")
@app.route('/')
def index():
    return "Server is running."

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    
@socketio.on('message')
def handler(data):
    print(data)
    user = data['user_input']
    QorRev = statement_analyzer(user)
    if(QorRev=='query'):
        message='Here are some good ones !'
    else:
        message='ok i will keep that in mind'
    senti = sentiment_analyzer(user)
    targets = target(user)
    dbtags = dbTags(user)
    recommended_outfits = output(dbtags)
    links = []
    ids = []

    for index, row in recommended_outfits.iterrows():
        ids.append(str(row['id']) + '.jpg')

    for id in ids:
        links.append(linker(id))

    response = {
        'Message':message,
        'QorRev': QorRev,
        'senti': senti,
        'targets': targets,
        'dbtags': dbtags,
        'recommended_outfits': recommended_outfits[['gender', 'masterCategory', 'subCategory',
                                                    'articleType', 'baseColour', 'season', 'year', 'usage', 'productDisplayName']].to_dict(orient='records'),
        'links': links
    }
    print(response)

    emit('bot', response)
    


@app.route('/trends', methods=['GET'])
def get_trends():
    html_page = urlopen("https://www.flipkart.com/clothing-and-accessories/fashion-trends~brand/pr?sid=clo")
    soup = BeautifulSoup(html_page, 'html.parser')
    images = []
    
    for img in soup.findAll('img'):
        img_src = img.get('src')
        if img_src and img_src.startswith('https://') and img_src.endswith('.jpeg?q=90'):
            images.append(img_src)
    
    return jsonify(images)


if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=3000, debug=True)





# if __name__ == "__main__":
#     while(True):
#         user= input("user: ")
#         QorRev = statement_analyzer(user)
#         print(QorRev)
#         senti= sentiment_analyzer(user)
#         print(senti)
#         targets=target(user)
#         print(targets)
#         dbtags= dbTags(user)
#         print(dbtags)
#         recommended_outfits=output(dbtags)
#         print(recommended_outfits[['gender', 'masterCategory', 'subCategory',
#               'articleType', 'baseColour', 'season', 'year', 'usage', 'productDisplayName']])
        
#         links = []
#         ids =[]
#         # Iterate through recommended outfits and display images
#         for index, row in recommended_outfits.iterrows():
#             ids.append(str(row['id']) + '.jpg')
#             print(ids)  
#         for id in ids:
#             links.append(linker(id)) 
#         print(links)
#         for link in links:
#             webbrowser.open(link)
        

