import json
import nltk
import spacy
from nltk.corpus import stopwords
nltk.download('stopwords')
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
    mappings_for_word = [mapping[1] for mapping in class_mapping_list if word == mapping[0]]
    if not mappings_for_word:
      mappings_for_word.append(word)
    for i in mappings_for_word:
      output.append(i)
    mappings_for_word.clear()
print(output)
merged_list = []
for item in output:
    if isinstance(item, list):
        merged_list.extend(item)
    else:
        merged_list.append(item)

print(merged_list)
stop_words = set(stopwords.words('english'))
filtered_words = [word for word in merged_list if word.lower()
                  not in stop_words]
print(filtered_words)
