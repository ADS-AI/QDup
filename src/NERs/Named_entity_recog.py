import json
import nltk
import os
from nltk import word_tokenize
nltk.download('punkt')
import spacy

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
    ques_NERs = []



def jaccard_score(query_tokens, question_tokens):

    query_tokens = set(query_tokens)
    question_tokens = set(question_tokens)

    common = len(query_tokens & question_tokens)
    union = len(query_tokens | question_tokens)

    return common/union

def main_jaccard_search(candidates, query_question, threshold, duplicate_threshold = 0.99):

    data = load_data()

    query_tokens = generate_tokens(query_question)
    # print(query_tokens)

    passed_candidates = []
    duplicate_candidates = []

    for ques_id in candidates:

        try :

            score = jaccard_score(query_tokens, data[ques_id])

            if score >= duplicate_threshold :
                duplicate_candidates.append(ques_id)

            elif score >= threshold :
                passed_candidates.append(ques_id)

        except:

            # print("Key not found : " + ques_id)
            continue 

    return duplicate_candidates, passed_candidates

load_data()



# Good Examples 

# In a three column cash book	In a triple column cash book

# which ionic compound has the largest amount of lattice energy