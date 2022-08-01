import json
import nltk
from nltk import bigrams, trigrams, word_tokenize
nltk.download('punkt')


def load_data():

    try :
        data = json.load(open('Source Code/Jaccard_Similarity/tokenised_question.json', encoding='utf-8'))
        return data

    except:
        print("Error loading data")
        return None

def generate_tokens(ques):
    tokens = nltk.word_tokenize(ques)
    return tokens


def jaccard_score(query_tokens, question_tokens):

    query_tokens = set(query_tokens)
    question_tokens = set(question_tokens)

    common = len(query_tokens & question_tokens)
    union = len(query_tokens | question_tokens)

    return common/union

def main_jaccard_search(candidates, query_question, threshold):

    data = load_data()

    query_tokens = generate_tokens(query_question)
    print(query_tokens)

    passed_candidates = []

    for ques_id in candidates:

        try :

            score = jaccard_score(query_tokens, data[ques_id])
            
            if score >= threshold :
                passed_candidates.append(ques_id)

        except:

            print("Key not founnd : " + ques_id)
            continue 

    return passed_candidates








