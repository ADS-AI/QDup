import pandas as pd
from time import time
from sentence_transformers import SentenceTransformer
import os
from numpy.linalg import norm
import json
import numpy as np
import scann
# from ..formatting import output_color
class output_color:
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"

def load_data():
    path_file_embd = os.path.normpath(os.getcwd() + os.sep + os.pardir)
    path_file_embd = os.path.join(path_file_embd, "src")
    path_file_embd = os.path.join(path_file_embd, "Data-cache")
    path_file_embd = os.path.join(path_file_embd, "embedding_df.csv")
    data = pd.read_csv(path_file_embd, index_col = 0)
    return data


data = load_data()
k = int(np.sqrt(data.shape[0]))
searcher = scann.scann_ops_pybind.builder(data, 10, "dot_product").tree(num_leaves=k, num_leaves_to_search=int(k/20), training_sample_size=2500).score_brute_force(2).reorder(7).build()


def load_txt_data():
    path_file_txt = os.path.normpath(os.getcwd() + os.sep + os.pardir)
    path_file_txt = os.path.join(path_file_txt, "src")
    path_file_txt = os.path.join(path_file_txt, "Data-cache")
    path_file_txt = os.path.join(path_file_txt, "questiontext.json")
    data = json.load(open(path_file_txt, encoding="utf-8"))
    return data


def generate_embeddings(data_ls):
    model = SentenceTransformer("paraphrase-MiniLM-L6-v2")
    embeddings = model.encode(data_ls)
    return embeddings


def cos_sim(ques1, ques2):
    A = np.array(ques1)
    B = np.array(ques2)
    cosine_sim = np.dot(A, B) / (norm(A) * norm(B))
    return cosine_sim


def sort_list(list1, list2):
    zipped_pairs = zip(list2, list1)
    z = [x for _, x in sorted(zipped_pairs, reverse=True)]
    return z


def embed_search_v2(
    predicted_duplicate_id, candidates, already_listed, top_k, embed_only_new=True, verbose=1
):
    # data = load_data()
    embeds = data.loc[int(predicted_duplicate_id)]
    x = searcher.search(embeds, final_num_neighbors=6)
    if(len(x)> 0):
        x = x[0]
        print("X: ", x)
        index_to_ques_id_ls = []
        for index in x:
            index_to_ques_id_ls.append(data.iloc[index].name)
        print("index_to_ques_id_ls: ", index_to_ques_id_ls)

        return_candidates = []
        for id in index_to_ques_id_ls:
            if str(id) not in already_listed:
                return_candidates.append(id)
            if len(return_candidates) >= top_k:
                break

        return return_candidates
    else:
        print("Didnt make it")
        return []
    # passed_candidates = []
    # ls_cos_sim = []
    # for ques_id in candidates:
    #     try:
    #         score = cos_sim(embeds, data.loc[int(ques_id)])
    #         ls_cos_sim.append(score)
    #     except:
    #         print("key missing: ", ques_id)
    #         ls_cos_sim.append(0)

    # closest_candidates = sort_list(candidates, ls_cos_sim)

    # if embed_only_new:
    #     return_candidates = []
    #     for id in closest_candidates:
    #         if str(id) not in already_listed:
    #             return_candidates.append(id)
    #         if len(return_candidates) >= top_k:
    #             break
    # else:
    #     return_candidates = closest_candidates[:top_k]

    # question_texts = load_txt_data()
    # if verbose == 1:
    #     print(output_color.DARKCYAN + "(EMBED)Related questions: ")
    #     for id in return_candidates:
    #         print(id, " : ", str(question_texts[str(id)]))
    #     print(output_color.END)

    # return return_candidates