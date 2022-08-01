import json
import nltk
import os
import spacy
import re
from nltk.stem import WordNetLemmatizer 
nltk.download('omw-1.4')
nltk.download('wordnet')

# spacy download en 

articles = set(['a', 'the', 'an', 's'])
nlp = spacy.load("en_core_web_sm")
lemmatizer = WordNetLemmatizer()

def load_data():

    try :
        path_file_qtxt = os.getcwd()
        path_file_qtxt = os.path.join(path_file_qtxt, 'src')
        path_file_tkn = os.path.join(path_file_qtxt, 'Datasets')
        path_file_tkn = os.path.join(path_file_tkn, 'questions_ners.json')
        data = json.load(open(path_file_tkn, encoding='utf-8'))
        return data

    except:
        print("Error loading data")
        return None
    


def generate_NER(ques):

    words = nltk.word_tokenize(ques)
    words = [word if word not in articles else '' for word in words]

    lemmatized_words = ' '.join([lemmatizer.lemmatize(w) for w in words])
    lemmatized_words = re.sub(' +', ' ', lemmatized_words)
    lemmatized_words = re.sub("'s", '',lemmatized_words )

    NERs_tokens = nlp(lemmatized_words)

    ques_NERs = []

    for token in NERs_tokens.ents:
        ques_NERs.append(str(token.text))
    
    return ques_NERs

def Evaluate_NERs(query_NERs, question_NERs):    # Can add word embeddings, synonyms, etc checks here

    print(query_NERs)
    print(question_NERs)

    if len(query_NERs) == 0 or len(question_NERs) == 0:
        return True

    for NERs in question_NERs:
        if NERs not in query_NERs:           
            return False

    for NERs in query_NERs:
        if NERs not in question_NERs:
            return False

    return True

def check_NERs(candidates, query_question):

    data = load_data()

    query_NERs = generate_NER(query_question)
    
    passed_candidates = []

    for ques_id in candidates:

        try :

            result = Evaluate_NERs(query_NERs, data[ques_id])

            if result == True :
                passed_candidates.append(ques_id)

        except:

            print("Key not found : " + ques_id)
            continue 

    return passed_candidates

# data = load_data()
# print(data['2016891'])

# print(generate_NER("in a triple column cash book"))



# Good Examples 

# In a three column cash book	In a triple column cash book

# which ionic compound has the largest amount of lattice energy