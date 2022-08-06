import json
import nltk
import os
import spacy
import re
from formatting import output_color
from nltk.stem import WordNetLemmatizer 
nltk.download('omw-1.4')
nltk.download('wordnet')

# spacy download en 

articles = set(['a', 'the', 'an', 's'])
nlp = spacy.load("en_core_web_sm")
lemmatizer = WordNetLemmatizer()

def load_data():
    # try :
        path_file_ner = os.path.normpath(os.path.dirname(__file__) + os.sep + os.pardir)
        path_file_ner = os.path.join(path_file_ner, 'Data-cache')
        path_file_ner = os.path.join(path_file_ner, 'questions_ners.json')
        data = json.load(open(path_file_ner, encoding='utf-8'))
        return data

    # except:
    #     print("Error loading data")
    #     return None
    
def load_txt_data():
    # try :
        path_file_txt = os.path.normpath(os.path.dirname(__file__) + os.sep + os.pardir)
        path_file_txt = os.path.join(path_file_txt, 'Data-cache')
        path_file_txt = os.path.join(path_file_txt, 'questiontext.json')
        data = json.load(open(path_file_txt, encoding='utf-8'))
        return data
    # except:
    #     print("Error loading jaccard data")
    #     return None


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

    # print(query_NERs)
    # print(question_NERs)

    if len(query_NERs) == 0 or len(question_NERs) == 0:
        return True

    for NERs in question_NERs:
        if NERs not in query_NERs:           
            return False

    for NERs in query_NERs:
        if NERs not in question_NERs:
            return False

    return True

def check_NERs(candidates, query_question, verbose = 0):

    data = load_data()

    query_NERs = generate_NER(query_question)
    question_texts = load_txt_data()
    passed_candidates = []

    for ques_id in candidates:
        try :
            result = Evaluate_NERs(query_NERs, data[ques_id])
            if result == True :
                passed_candidates.append(ques_id)
        except:
            print("Key not found : " + ques_id)
            continue 

    if(verbose == 1):
        print(output_color.PURPLE + "(NER) Potential_candidates : ")
        for id in passed_candidates: 
            print(id + " : " + question_texts[id])
        print(output_color.END)

    return passed_candidates

# data = load_data()
# print(data['2016891'])

# print(generate_NER("in a triple column cash book"))



# Good Examples 

# In a three column cash book	In a triple column cash book

# which ionic compound has the largest amount of lattice energy