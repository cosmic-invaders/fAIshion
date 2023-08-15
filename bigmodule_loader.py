
# Define candidate labels for review or query

import spacy
from transformers import pipeline
cache = "/cache"
# Load the zero-shot classification pipeline
zero_shot_pipeline = pipeline(
    "zero-shot-classification", model="K:/grid/Backend/backend/cache/zero-shot")
nlp = spacy.load("en_core_web_sm")

# Load the sentiment analysis pipeline
sentiment_analysis_pipeline = pipeline(
    "sentiment-analysis", model="K:/grid/Backend/backend/cache/sentiment")

# Analyze sentiment of a review


def analyze_sentiment(review_text):
    sentiment_result = sentiment_analysis_pipeline(review_text)[0]
    label = sentiment_result['label']
    return label



input_labels = ["review", "query"]

# Define candidate labels for product categories
# category_labels = ["upperwear", "bottomwear",
#                    "accessories", "wearables", "outfit", "FootWear"]

# Load the English language model for spaCy

input_text = input("user :  ")

# Perform zero-shot classification for review or query
result = zero_shot_pipeline(input_text, input_labels)

# Get the label with the highest score
predicted_label = result['labels'][0]

if predicted_label == input_labels[0]:  # Review
    sentiment = analyze_sentiment(input_text)
    print("its a review!!")
    print("Sentiment:", sentiment)
    doc = nlp(input_text)
    objects = [token.text for token in doc if token.pos_ == "NOUN"]

    ## This method is no more being used because team decided that inference is better than classification
    # Perform zero-shot classification for product categories
    # for obj in objects:
    #     category_result = zero_shot_pipeline(obj, category_labels)
    #     category_label = category_result['labels'][0]
    #     confidence_score = category_result['scores'][0]

    #     print(f"Object: {obj}")
    #     print("Classified as:", category_label)
    #     print("Confidence Score:", confidence_score)

else:  # Query
    print("Classified as:", predicted_label)
    # Process the input text with spaCy
    doc = nlp(input_text)

    # Extract objects (direct objects) and events (occasions) from the sentence
    objects = []
    events = []
    keywords = []
    for chunk in doc.noun_chunks:
        keywords.append(chunk.text)

    for token in doc:
        if "obj" in token.dep_ and token.head.pos_ == "VERB":
            objects.append(token.text)
        elif "nsubj" in token.dep_ and token.head.pos_ == "VERB":
            events.append(token.text)

    # for obj in objects:
    #     category_result = zero_shot_pipeline(obj, category_labels)
    #     category_label = category_result['labels'][0]
    #     confidence_score = category_result['scores'][0]

    #     print(f"Object: {obj}")
    #     print("Classified as:", category_label)
    #     print("Confidence Score:", confidence_score)

    print(keywords)
    for obj in objects:
        print(f"Object: {obj}")
