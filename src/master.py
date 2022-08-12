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
time.sleep(5)  # why is this here ?

import json
import os
from Preprocessing import main_preprocessing as pre
from Jaccard_Similarity import jaccard_search as jaccard
from NERs import Named_entity_recog as ner
from formatting import output_color
from Kw_generation.kw_runner import extract_kw_ques, kw_potential_candidates
from Sentence_embeddings.compare_embeds import embed_search
from Syllabus_Tagging.tagrec import get_question_tag, get_same_tag_candids
from return_questions import get_texts

print(
    "-------------------------------------------------------------------------------------------------------------"
)
print("Modules installed successfully!")
print()

print("Enter the question : ", end="")

def run_model(query_question): 

    #
    #   GLOBAL VARIABLES
    #
    GLOB_VERBOSE = 1
    KW_THRESHOLD = 0.8
    JACC_THRESHOLD = 0.3
    TOP_K_EMBEDS = 3
    EMBED_ONLY_NEW = True 
    # show only those sentences which have not yet been identified as duplicate when showing closest sentences by embeddings

    #
    #   Model
    #
    query_question = pre.preprocess(query_question)
    extract_kw_ques(
        query_question
    )  # this step is being called here to run simultaneously with next commands

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


    #
    # Getting extracted keywords
    #

    potential_candidates = kw_potential_candidates(
        potential_candidates, query_question, KW_THRESHOLD, verbose=GLOB_VERBOSE
    )


    #
    # Search based on embeddings
    #
    already_listed = potential_candidates+duplicate_questions
    embed_candids = embed_search(
        query_question,
        tag_potential_candidates,
        already_listed,
        TOP_K_EMBEDS,
        embed_only_new=EMBED_ONLY_NEW,
        verbose=GLOB_VERBOSE,
    )

    duplicate_questions_ques = get_texts(duplicate_questions)
    potential_candidates_ques = get_texts(potential_candidates)
    embed_candids_ques = get_texts(embed_candids)

    return (duplicate_questions_ques, potential_candidates_ques, embed_candids_ques)