import time
from formatting import EM_LOGO
import gradio as gr

print()
print(
    "********************************* Online Question Duplication Demo ******************************************"
)
print()
print("Installing modules...")
print(
    "-------------------------------------------------------------------------------------------------------------"
)
print(EM_LOGO)

import json
import os
from Preprocessing import main_preprocessing as pre
from Jaccard_Similarity import jaccard_search as jaccard
from NERs import Named_entity_recog as ner
from formatting import output_color
from Kw_generation.kw_runner import kw_potential_candidates
from Sentence_embeddings.compare_embeds import embed_search_v2
from Syllabus_Tagging.tagrec import get_question_tag, get_same_tag_candids
from return_questions import get_texts, get_texts_v2
from Kw_generation.ans_kw_checker import get_ans_potential_candidates_v2
from negation import negation_pairs

print(
    "-------------------------------------------------------------------------------------------------------------"
)
print("Modules installed successfully!")
print()

print("Enter the question : ", end="")

def run_model(query_question, query_question_ans): 
    t1 = time.time()

    #
    #   GLOBAL VARIABLES
    #
    GLOB_VERBOSE = 1
    KW_THRESHOLD = 0.7
    JACC_THRESHOLD = 0.6
    TOP_K_EMBEDS = 3
    EMBED_ONLY_NEW = True 
    ANS_KW_THRESHOLD = 0.4
    # show only those sentences which have not yet been identified as duplicate when showing closest sentences by embeddings

    #
    #   Model
    #
    query_question = pre.preprocess(query_question)

    #
    # Get tags and potential candidates list
    #
    tag_pred = get_question_tag(ques=query_question, verbose=GLOB_VERBOSE)
    tag_potential_candidates = get_same_tag_candids(
        ques_text=query_question, curr_tag=tag_pred
    )
    potential_candidates = (
        tag_potential_candidates  # tag_potential_candidates  latere used for embeddings
    )
    #
    # Get jaccard similarity questions
    #
    high_jaccard, potential_candidates = jaccard.main_jaccard_search(
        potential_candidates, query_question, JACC_THRESHOLD, verbose=1
    )
    #
    # Exact duplicates
    #
    duplicate_questions = high_jaccard


    #
    # Checking for NERs
    #

    potential_candidates = ner.check_NERs(
        potential_candidates, query_question, verbose=GLOB_VERBOSE
    )

    after_ner_potential_candidates= [] 
    for i in potential_candidates:
        after_ner_potential_candidates.append(i)


    #
    # Getting extracted keywords
    #
    potential_candidates = list(kw_potential_candidates(
        potential_candidates, query_question, KW_THRESHOLD, verbose=GLOB_VERBOSE
    ))

    if len(query_question_ans) > 0:
        print(query_question_ans)
        ans_also_same = get_ans_potential_candidates_v2(
            potential_candidates, query_question_ans, ANS_KW_THRESHOLD, verbose=GLOB_VERBOSE
        )
    else:
        print("(ANS) No answer provided")
        ans_also_same = potential_candidates

    # duplicates
    duplicate_questions_ques_ids = []
    for i in duplicate_questions: 
        duplicate_questions_ques_ids.append(i)
    for i in ans_also_same: 
        duplicate_questions_ques_ids.append(i)

    duplicate_questions_ques = get_texts(duplicate_questions_ques_ids)
    #
    # Search based on embeddings
    #
    already_listed = potential_candidates+duplicate_questions_ques_ids
    if(len(duplicate_questions_ques_ids) > 0):
        embed_candids = embed_search_v2(
            duplicate_questions_ques_ids[0],
            tag_potential_candidates,
            already_listed,
            TOP_K_EMBEDS,
            embed_only_new=EMBED_ONLY_NEW,
            verbose=GLOB_VERBOSE,
        )
    else:
        embed_candids = []
    related_questions = get_texts_v2(embed_candids)



    #related questions
    # related_questions = get_texts(embed_candids_ques)
    all_questions = []
    for j in potential_candidates:
        all_questions.append(j)
    all_questions = list(set(all_questions).difference(set(duplicate_questions_ques_ids)))
    related_questions.extend(get_texts(all_questions))

    neg_removed_duplicates, dropped_sentence = negation_pairs(query_question, duplicate_questions_ques)
    related_questions.extend(dropped_sentence)

    print("Total time ", time.time() - t1)

    return (neg_removed_duplicates, related_questions)