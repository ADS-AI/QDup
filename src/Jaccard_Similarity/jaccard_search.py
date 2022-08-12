import json
from formatting import output_color
import nltk
import os
from nltk import word_tokenize
import nltk
from nltk.stem import WordNetLemmatizer

nltk.download("wordnet")
nltk.download("punkt")


def load_data():
    # try :
    path_file_tkn = os.path.normpath(os.getcwd() + os.sep + os.pardir)
    path_file_tkn = os.path.join(path_file_tkn, "src")
    path_file_tkn = os.path.join(path_file_tkn, "Data-cache")
    path_file_tkn = os.path.join(path_file_tkn, "tokenised_question.json")
    data = json.load(open(path_file_tkn, encoding="utf-8"))
    return data


# except:
#     print("Error loading jaccard data")
#     return None


def load_txt_data():
    # try :
    path_file_tkn = os.path.normpath(os.getcwd() + os.sep + os.pardir)
    path_file_tkn = os.path.join(path_file_tkn, "src")
    path_file_tkn = os.path.join(path_file_tkn, "Data-cache")
    path_file_tkn = os.path.join(path_file_tkn, "questiontext.json")
    data = json.load(open(path_file_tkn, encoding="utf-8"))
    return data


# except:
#     print("Error loading jaccard data")
#     return None


def generate_tokens(ques, lemmatizer):
    tokens = nltk.word_tokenize(ques)
    tokens = [str(lemmatizer.lemmatize(tok)) for tok in tokens]
    return tokens


def jaccard_score(query_tokens, question_tokens):

    query_tokens = set(query_tokens)
    question_tokens = set(question_tokens)

    common = len(query_tokens & question_tokens)
    union = len(query_tokens | question_tokens)

    return common / union


def main_jaccard_search(
    candidates, query_question, threshold, duplicate_threshold=0.99, verbose=1
):
    data = load_data()
    lemmatizer = WordNetLemmatizer()
    query_tokens = generate_tokens(query_question, lemmatizer)
    passed_candidates = []
    duplicate_candidates = []

    for ques_id in candidates:
        try:
            score = jaccard_score(query_tokens, data[ques_id])
            if score >= duplicate_threshold:
                duplicate_candidates.append(ques_id)
            elif score >= threshold:
                passed_candidates.append(ques_id)
        except:
            continue

    if verbose == 1:
        question_texts = load_txt_data()
        print(output_color.GREEN + "(JACC)Duplicate questions : ")
        for id in duplicate_candidates:
            print(id + " : " + question_texts[id])
        print(output_color.END)

        print(output_color.DARKCYAN + "(JACC)Potential Candidates: ")
        for id in passed_candidates:
            print(id + " : " + question_texts[id])
        print(output_color.END)

    return duplicate_candidates, passed_candidates
