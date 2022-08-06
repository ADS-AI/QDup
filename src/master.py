import time
from formatting import EM_LOGO

print()
print('********************************* Online Question Duplication Demo ******************************************')
print()
print('Installing modules...')
print('-------------------------------------------------------------------------------------------------------------')
print(EM_LOGO)
time.sleep(5) # why is this here ?

import json
import os
from Preprocessing import main_preprocessing as pre
from Jaccard_Similarity import jaccard_search as jaccard
from NERs import Named_entity_recog as ner
from formatting import output_color
from Kw_generation.kw_runner import extract_kw_ques, kw_potential_candidates

print('-------------------------------------------------------------------------------------------------------------')
print('Modules installed successfully!')
print()

print("Enter the question : ", end = '')
query_question = input()

#
#   GLOBAL VARIABLES
#
GLOB_VERBOSE = 1
KW_THRESHOLD = 0.8
JACC_THRESHOLD = 0.4
#
#   Model
#
query_question = pre.preprocess(query_question)
extract_kw_ques(query_question) # this step is being called here to run simultaneously with next commands

path_file_qtxt = os.path.dirname(__file__)
path_file_qtxt = os.path.join(path_file_qtxt, 'Data-cache')
path_file_qtxt = os.path.join(path_file_qtxt, 'questiontext.json')
question_texts = json.load(open(path_file_qtxt, encoding='utf-8'))

potential_candidates = list(question_texts.keys())



# TODO Reduce search space to only those questions that have the same syllabus as the query question

'''
    Reduce the search space using jaccard similarity
'''

high_jaccard, potential_candidates = jaccard.main_jaccard_search(potential_candidates,query_question, JACC_THRESHOLD, verbose = 1)


# 
# Exact duplicates
#

duplicate_questions = high_jaccard



# print(output_color.PURPLE + "Potential_candidates : ")
# for id in potential_candidates: 
#     print(id + " : " + question_texts[id])
# print(output_color.END)

#
# Checking for NERs
#

potential_candidates = ner.check_NERs(potential_candidates, query_question, verbose=GLOB_VERBOSE)


#
# Getting extracted keywords
#

potential_candidates = kw_potential_candidates(potential_candidates, query_question, KW_THRESHOLD, verbose = GLOB_VERBOSE)

