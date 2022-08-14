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

def process_tagrec_result(txt):


    return txt


def get_question_tag(ques, verbose):
    

    headers = {
        'accept': 'application/json',
    }
    json_data = {
        'content': 'when mercury ii chloride is treated with excess of stannous chloride the products obtained are',
    }
    response = requests.post('http://localhost:8000/gettaxonomy', headers=headers, json=json_data)
    pred_tag = process_tagrec_result(response.text)

    if verbose > 0:
        print(output_color.BLUE + "(Tag) Question belongs to category : ", pred_tag)
        print(output_color.END)

    return pred_tag


def get_same_tag_candids(ques_text, curr_tag):
    df = load_data()
    return_ls = []
    for index, row in df.iterrows():
        spl = re.split("\W+", row["tagrec++_predictions"])
        pred = spl[0]
        if pred == curr_tag:
            return_ls.append(str(row["question_id"]))
    return return_ls
