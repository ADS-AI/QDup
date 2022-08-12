from Preprocessing import Punctuation
import pandas as pd
import csv
import re
from nltk.stem import WordNetLemmatizer
import os
import nltk
from tqdm import tqdm
import numpy as np
nltk.download("wordnet")
nltk.download("punkt")
nltk.download('omw-1.4')
lemmatizer = WordNetLemmatizer()

elements={} 

filename = os.path.normpath(os.path.dirname(__file__) + os.sep + os.pardir)
filename = os.path.join(filename, "Preprocessing")
filename = os.path.join(filename, "Elementlist.csv")

with open(filename, newline='') as csvfile: 
    elementreader = csv.reader(csvfile, delimiter=',') 
    for row in elementreader: 
        a,b,c = row 
        elements[b.lower()] = c.lower() 

greek_letters = {
    'alpha': 'α',
    'beta': 'β',
    'gamma': 'γ',
    'delta': 'δ',
    'epsilon': 'ε',
    'zeta': 'ζ',
    'eta': 'η',
    'theta': 'θ',
    'iota': 'ι',
    'kappa': 'κ',
    'lambda': 'λ',
    'mu': 'μ',
    'nu': 'ν',
    'xi': 'ξ',
    'omicron': 'ο',
    'pi': 'π',
    'rho': 'ρ',
    'sigma': 'σ',
    'tau': 'τ',
    'upsilon': 'υ',
    'phi': 'φ',
    'chi': 'χ',
    'psi': 'ψ',
    'omega': 'ω'
}

apostrophe_words = { "ain't" : "am not", "he'sn't" : "he is not", "i'dn't" : "i would not", "i'd" : "i would", "isn't" : "is not", "i'ven't" : "i have not", "mightn't" : "might not", "mustn't" : "must not","needn't" : "need not", "shan't" : "shall not", "she'sn't" : "she is not", "shouldn't" : "should not", "wasn't" : "was not", "weren't" : "were not", "we'ren't" : "we are not", "won't" : "will not", "wouldn't" : "would not", "i'm" :"i am", "you're" : "you are", "it's" : "it is", "i'd" : "i would", "let's" : "let us", "who's" : "who is", "they'd" : "they had" }

def replace_elements(A):
    for i in range(len(A)):
        if A[i] in elements:
            A[i] = elements[A[i]]

    return A

def replace_greek_letters(A):
    for i in range(len(A)):
        if A[i] in greek_letters:
            A[i] = greek_letters[A[i]]

    return A

def replace_apostrophe_words_custom(A):
        for i in range(len(A)):
            if A[i] in apostrophe_words:
                A[i] = apostrophe_words[A[i]]
    
        return A

def replace_apostrophe_words_general(A):

    for i in range(len(A)):
        phrase = A[i]

        if(phrase[0] == '\'' or phrase[-1] == '\''):   # 'dear' -> wouldear
            A[i] = phrase 
            continue 

        phrase = re.sub(r"ain\'t", "am not", phrase)
        phrase = re.sub(r"y\'all", "you all", phrase)
        phrase = re.sub(r"can\'t", "can not", phrase)
        phrase = re.sub(r"n\'t", " not", phrase)
        phrase = re.sub(r"\'re", " are", phrase)
        phrase = re.sub(r"\'s", " is", phrase)
        phrase = re.sub(r"\'d", " would", phrase)
        phrase = re.sub(r"\'ll", " will", phrase)
        phrase = re.sub(r"\'t", " not", phrase)
        phrase = re.sub(r"\'ve", " have", phrase)
        phrase = re.sub(r"\'m", " am", phrase)
        A[i] = phrase

    return A

def lemmatize_words(A):

    for i in range(len(A)):
        A[i] = lemmatizer.lemmatize(A[i])

    return A

def replace_elements_in_string(A):

    A = A.lower()

    A = list(A.split(" "))

    A = replace_elements(A)
    A = replace_greek_letters(A)
    A = lemmatize_words(A)
    A = replace_apostrophe_words_general(A)

    A = " ".join(A)
    
    return A


def preprocess(question):
    """
    Preprocesses the questions
    """
    question = question.lower()
    question = Punctuation.remove_punctuation(question)
    question = replace_elements_in_string(question.strip())

    return question
