from Preprocessing import Punctuation


def preprocess(question):

    """
    Preprocesses the questions
    """
    question = question.lower()
    question = Punctuation.remove_punctuation(question)

    return question
