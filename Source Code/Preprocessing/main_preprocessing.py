
from Preprocessing import Punctuation

def preprocess(question):

    '''
    Preprocesses the questions
    '''

    question = Punctuation.remove_punctuation(question)


    return question

