import os
import re
from formatting import output_color
import json

def load_txt_data():
    # try :
    path_file_ner = os.path.normpath(os.path.dirname(__file__) + os.sep + os.pardir)
    path_file_ner = os.path.join(path_file_ner, "src")
    path_file_ner = os.path.join(path_file_ner, "Data-cache")
    path_file_ner = os.path.join(path_file_ner, "questiontext.json")
    data = json.load(open(path_file_ner, encoding="utf-8"))
    return data


def get_texts(id_ls):
    data = load_txt_data()
    res = []
    for id in id_ls: 
        res.append(data[id])
    return res

# get_texts(['23','23','23'])