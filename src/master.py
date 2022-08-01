import json
from multiprocessing.reduction import duplicate
import os
from Preprocessing import main_preprocessing as pre
from Jaccard_Similarity import jaccard_search as jaccard

print("Enter the question : ", end = '')
query_question = input()

query_question = pre.preprocess(query_question)

path_file_qtxt = os.getcwd()
path_file_qtxt = os.path.join(path_file_qtxt, 'src')
path_file_qtxt = os.path.join(path_file_qtxt, 'Datasets')
path_file_qtxt = os.path.join(path_file_qtxt, 'questiontext.json')
question_texts = json.load(open(path_file_qtxt, encoding='utf-8'))

potential_candidates = list(question_texts.keys())

duplicate_questions = []

# print(potential_candidates[:10])

# TODO Reduce search space to only those questions that have the same syllabus as the query question

'''
    Reduce the search space using jaccard similarity
'''

high_jaccard, potential_candidates = jaccard.main_jaccard_search(potential_candidates,query_question, 0.7)

duplicate_questions = duplicate_questions + high_jaccard

print("Duplicate questions : ")

for id in duplicate_questions: 
    print(id + " : " + question_texts[id])

print("Potential_candidates : ")

for id in potential_candidates: 
    print(id + " : " + question_texts[id])










