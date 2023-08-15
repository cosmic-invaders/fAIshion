from transformers import pipeline
import spacy
import nltk
from nltk.corpus import stopwords
# nltk.download('stopwords')
import json

# Load the zero-shot classification pipeline
# zero_shot_pipeline = pipeline("zero-shot-classification")
nlp = spacy.load("en_core_web_sm")

# Convert input text to lowercase and tokenize
input_text = input("user: ")
input_text = input_text.lower()
doc = nlp(input_text)

# Extract objects (direct objects) and events (occasions) from the sentence
keywords = []
dblabels = []
for chunk in doc.noun_chunks:
    keywords.append(chunk.text)



# Convert each term into single word terms
single_word_array = []
for term in keywords:
    single_words = term.split()
    single_word_array.extend(single_words)
print(single_word_array)

## read json rules obj
json_file_path = "class_mapping_list.json"
with open(json_file_path, "r") as json_file:
    class_mappings = json.load(json_file)
list_of_lists = class_mappings

class_mapping_list = [tuple(lst) for lst in list_of_lists]

# print(class_mapping_list)
    
# print(type(class_mapping_list))

mappings_for_word = []
output = []
# Iterate through each word in the normalized array
for word in single_word_array:
    mappings_for_word = [mapping[1] for mapping in class_mapping_list if word == mapping[0]]
    # print(mappings_for_word)
    if not mappings_for_word:
      mappings_for_word.append(word)
    for i in mappings_for_word:
      output.append(i)
    mappings_for_word.clear()
    
 ## merging inner lists of output kyoki wo sab innerlist mappings hai for each word
 
merged_list = []
for item in output:
    if isinstance(item, list):
        merged_list.extend(item)
    else:
        merged_list.append(item)

print(merged_list)

##filtering i tum hum mai etc

stop_words = set(stopwords.words('english'))
filtered_words = [word for word in merged_list if word.lower()
                  not in stop_words]
print(filtered_words)
