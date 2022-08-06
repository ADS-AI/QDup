import pandas as pd
from time import time
from sentence_transformers import SentenceTransformer
import os
from numpy.linalg import norm
import json
import numpy as np
from formatting import output_color

def load_ids():
    # try:
        path_file_embd = os.path.normpath(os.getcwd() + os.sep + os.pardir)
        path_file_embd = os.path.join(path_file_embd, 'QUESTION_DUPLICATE_DETECTION')
        path_file_embd = os.path.join(path_file_embd, 'src')
        path_file_embd = os.path.join(path_file_embd, 'Data-cache')
        path_file_embd = os.path.join(path_file_embd, 'all_ids.json')
        data = json.load(open(path_file_embd, encoding='utf-8'))
        return data
    # except:
    #     print("Error loading embeddings data")
    #     return None


def load_data():
    # try:
        path_file_embd = os.path.normpath(os.getcwd() + os.sep + os.pardir)
        path_file_embd = os.path.join(path_file_embd, 'QUESTION_DUPLICATE_DETECTION')
        path_file_embd = os.path.join(path_file_embd, 'src')
        path_file_embd = os.path.join(path_file_embd, 'Data-cache')
        path_file_embd = os.path.join(path_file_embd, 'questions_embeddings.json')
        data = json.load(open(path_file_embd, encoding='utf-8'))
        return data
    # except:
    #     print("Error loading embeddings data")
    #     return None

def load_txt_data():
    # try :
        path_file_txt = os.path.normpath(os.getcwd() + os.sep + os.pardir)
        path_file_txt = os.path.join(path_file_txt, 'QUESTION_DUPLICATE_DETECTION')
        path_file_txt = os.path.join(path_file_txt, 'src')
        path_file_txt = os.path.join(path_file_txt, 'Data-cache')
        path_file_txt = os.path.join(path_file_txt, 'questiontext.json')
        data = json.load(open(path_file_txt, encoding='utf-8'))
        return data
    # except:
    #     print("(Embedding) Error loading txt data")
    #     return None

def generate_embeddings(data_ls):
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    embeddings = model.encode(data_ls)
    return embeddings

def cos_sim(ques1, ques2):
  A = np.array(ques1)
  B = np.array(ques2)
  cosine_sim = np.dot(A,B)/(norm(A)*norm(B))
  return cosine_sim

def sort_list(list1, list2):
    zipped_pairs = zip(list2, list1)
    z = [x for _, x in sorted(zipped_pairs, reverse=True)]
    return z

def embed_search(query_question, top_k, verbose = 1):
    candidates = load_ids()
    data = load_data()
    embeds = generate_embeddings([query_question])
    passed_candidates = []
    ls_cos_sim = []
    for ques_id in candidates:
        try:
            score = cos_sim(embeds[0], data[str(ques_id)])
            ls_cos_sim.append(score)
        except:
            print("key missing: ", ques_id)
            ls_cos_sim.append(0)

    passed_candidates = sort_list(candidates ,ls_cos_sim)[:top_k]
    question_texts = load_txt_data()
    if verbose == 1:
        print(output_color.DARKCYAN + "(EMBED)Potential Candidates: ")
        for id in passed_candidates: 
            print(id, " : " , str(question_texts[str(id)]))
        print(output_color.END)

    return passed_candidates