import re
import json
import random
import TTS1 as j_v

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

with open('intents.json') as intents_file:
    data= json.load(intents_file)

bot_name="jarvis"

texts=[]
labels=[]

for item in data['intents']:
    intent=item['intent']
    for example in item["examples"]:
        texts.append(example)
        labels.append(intent)

#Intent Detector
vectorizer = TfidfVectorizer()
x = vectorizer.fit_transform(texts)

clf = LogisticRegression()  # correct classifier
clf.fit(x, labels)

def predict_intent(text):
    x=vectorizer.transform([text])
    return clf.predict(x)[0]

def get_response(intent_name,context={}):
    for item in data["intents"]:
        context.setdefault("bot_name",bot_name)
        if item["intent"]==intent_name:
            response_template= random.choice(item["responses"])
            return response_template.format(**context)            
        

def extract_entities(text):
    entities = {}

    # Define regex patterns
    patterns = {
    "date": r"\b(?:\d{1,2}[/-]\d{1,2}(?:[/-]\d{2,4})?|\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:t)?(?:ember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s\d{1,2}(?:,\s?\d{2,4})?)\b",
    "time": r"\b\d{1,2}(:\d{2})?\s?(AM|PM|am|pm)?\b",
    "email": r"\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b",
    "phone": r"\b(?:\+?\d{1,3})?[-.\s]?(?:\(?\d{3}\)?[-.\s]?){1,2}\d{4}\b",
    "url": r"https?://(?:www\.)?\S+|www\.\S+",
    "money": r"\$\d+(?:\.\d{2})?|\d+\s?(dollars|USD|rupees|INR|euros|EUR|£|₹)",
    "number": r"\b\d+(?:\.\d+)?\b",
    "name": r"\b(?:Mr\.|Mrs\.|Ms\.|Dr\.)?\s?[A-Z][a-z]+(?:\s[A-Z][a-z]+)?\b",
    "location": r"\b(?:in|at|to|from)\s([A-Z][a-z]+(?:\s[A-Z][a-z]+)?)\b",
    "datetime": r"\b(?:on\s)?(?:\d{1,2}[/-]\d{1,2}(?:[/-]\d{2,4})?|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s\d{1,2}(?:,\s?\d{4})?)\s?(at\s)?\d{1,2}(:\d{2})?\s?(AM|PM|am|pm)?\b",
    "hashtag": r"#\w+",
    "mention": r"@\w+",
    "tag": r"\[(.*?)\]"
}

    for entity, pattern in patterns.items():
        matches = re.findall(pattern, text)
        if matches:
            entities[entity] = matches

    return entities

import re

def normalize_contractions(text):
    # Lowercase for consistency
    text = text.lower()

    # Replace common contractions and their misheard/mistyped forms
    text = re.sub(r"\bi['’`]m\b|\bi\s*@\b|\bi\s+at\b|\bim\b", "i am", text)
    text = re.sub(r"\byou['’`]re\b|\byoure\b|\byou\s+re\b", "you are", text)
    text = re.sub(r"\bhe['’`]s\b|\bhes\b|\bhe\s+s\b", "he is", text)
    text = re.sub(r"\bshe['’`]s\b|\bshes\b|\bshe\s+s\b", "she is", text)
    text = re.sub(r"\bit['’`]s\b|\bits\b|\bit\s+s\b", "it is", text)
    text = re.sub(r"\bwe['’`]re\b|\bwere\b|\bwe\s+re\b", "we are", text)
    text = re.sub(r"\bthey['’`]re\b|\btheyre\b|\bthey\s+re\b", "they are", text)

    text = re.sub(r"\bi['’`]ll\b|\bill\b", "i will", text)
    text = re.sub(r"\byou['’`]ll\b|\byoull\b", "you will", text)
    text = re.sub(r"\bhe['’`]ll\b|\bhell\b", "he will", text)
    text = re.sub(r"\bshe['’`]ll\b|\bshell\b", "she will", text)
    text = re.sub(r"\bthey['’`]ll\b|\btheyll\b", "they will", text)
    text = re.sub(r"\bwe['’`]ll\b|\bwell\b", "we will", text)

    text = re.sub(r"\bcan['’`]t\b|\bcant\b", "cannot", text)
    text = re.sub(r"\bdon['’`]t\b|\bdont\b", "do not", text)
    text = re.sub(r"\bwon['’`]t\b|\bwont\b", "will not", text)
    text = re.sub(r"\bdidn['’`]t\b|\bdidnt\b", "did not", text)
    text = re.sub(r"\bshouldn['’`]t\b|\bshouldnt\b", "should not", text)
    text = re.sub(r"\bcouldn['’`]t\b|\bcouldnt\b", "could not", text)
    text = re.sub(r"\bwouldn['’`]t\b|\bwouldnt\b", "would not", text)
    text = re.sub(r"\bhaven['’`]t\b|\bhavent\b", "have not", text)
    text = re.sub(r"\bhasn['’`]t\b|\bhasnt\b", "has not", text)
    
    return text


# Example usage
def chat_func(query):
    user_input = query
    intent = predict_intent(user_input)
    entities = extract_entities(user_input)

    response=get_response(intent)
    final_response=normalize_contractions(response)
    j_v.say(final_response)

