from ctypes import pointer
import json
from Preprocessing import main_preprocessing as pre
from Jaccard_Similarity import jaccard_search as jaccard

print("Enter the question : ")
query_question = input()

query_question = pre.preprocess(query_question)

question_texts = json.load(open('Source Code/Datasets/questiontext.json', encoding='utf-8'))

potential_candidates = list(question_texts.keys())

# print(potential_candidates[:10])

# TODO Reduce search space to only those questions that have the same syllabus as the query question

'''
    Reduce the search space using jaccard similarity
'''

potential_candidates = jaccard.main_jaccard_search(potential_candidates,query_question, 0.7)

print("Potential_candidates")

for id in potential_candidates: 
    print(question_texts[id])



# 2072381










