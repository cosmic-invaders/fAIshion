import spacy
from transformers import pipeline
import pickle

zero_shot_pipeline = pipeline("zero-shot-classification")
nlp = spacy.load("en_core_web_sm")

# Load the sentiment analysis pipeline
sentiment_analysis_pipeline = pipeline("sentiment-analysis")
zero_shot_pipeline.save_pretrained("K:/grid/Backend/backend/cache/zero-shot")
sentiment_analysis_pipeline.save_pretrained("K:/grid/Backend/backend/cache/sentiment")

