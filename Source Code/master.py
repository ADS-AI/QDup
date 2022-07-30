from Preprocessing import main_preprocessing as pre

print("Enter the question : ")
query_question = input()

query_question = pre.preprocess(query_question)

print(query_question)

