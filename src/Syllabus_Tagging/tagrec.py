import pandas as pd
import os
import requests

import re
from formatting import output_color

def load_data():
    # try:
    path_file_ner = os.path.normpath(os.path.dirname(__file__) + os.sep + os.pardir)
    path_file_ner = os.path.join(path_file_ner, "Data-cache")
    path_file_ner = os.path.join(path_file_ner, "base_data_tagrec_tagged.csv")
    df = pd.read_csv(path_file_ner, index_col=0, low_memory=False)
    # except:
    #     print("Error loading tags data")
    #     return pd.DataFrame(columns = ["question_id", "tagrec++_predictions"])
    return df


def process_tagrec_result(response_tag):
    first_dict_tag = eval(response_tag)[0]["taxonomy"] 
    subject = first_dict_tag.split(">>")[2]
    return subject


def get_question_tag(ques, verbose):
    headers = {
        'accept': 'application/json',
    }
    json_data = {
        'content': ques,
    }
    # response = requests.post('http://localhost:8000/gettaxonomy', headers=headers, json=json_data)
    # pred_tag = process_tagrec_result(response.text)
    pred_tag = 'chemistry'
    return pred_tag


df_global = load_data()


def get_same_tag_candids(ques_text, curr_tag):
    ret = [str(i) for i in df_global['question_id']]
    return ret
    # print("CURR_TAG:", curr_tag)
    # return_ls = []
    # for index, row in df_global.iterrows():
    #     # spl = re.split("\W+", row["tagrec++_predictions"])
    #     # pred = spl[0]
    #     return_ls.append(str(row["question_id"]))
    #     # if pred == curr_tag:
    #     #     return_ls.append(str(row["question_id"]))
    #     # else:
    #     #     return_ls.append(str(row["question_id"]))
    # return return_ls
