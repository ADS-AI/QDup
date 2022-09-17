import gradio as gr
from master import run_model
import pandas as pd
import json

def list_to_string(list):
    string = ""
    count = 1
    for i in list:
        string += str(count) + ". " + i.capitalize() + "   \n"
        count += 1
    return string

def master_of_masters(Question, Answer=""):
    
    list1, list2 = run_model(Question, Answer)

    ans1 = list_to_string(list1)
    ans2 = list_to_string(list2)

    return ans1, ans2

def master_of_masters_file(question_file):

    df = pd.read_csv(question_file.name,delimiter=',')
    
    df.fillna("",inplace=True)
    
    questions = df['question'].tolist()
    answers = df['answer'].tolist()

    json_out = {}

    for i in range(len(questions)):
        
        list1, list2 = run_model(questions[i], answers[i])
        json_out[questions[i]] = {"duplicate" : list1, "related" : list2}

    with open("output.json", "w") as outfile:
        json.dump(json_out, outfile)

    return "output.json"

question_text = gr.Textbox(lines = 2, placeholder="Enter Question..")
answer_text = gr.Textbox(lines = 2, placeholder="Enter Answer or Leave it empty..")

output1 = gr.Textbox(label = "Question Duplicates") 
output2 = gr.Textbox(label = "Related questions") 

desc = ("An application to prevent academicians from creating duplicate questions by suggesting near duplicates of a question present in the database.  \n"

        "Definition of Duplicacy : "
        )

with gr.Blocks() as demo:

    gr.Markdown("## Online Question Duplicity Finder")
    gr.Markdown(desc)

    with gr.Tabs():
        
        with gr.TabItem("Add Question"):

            with gr.Row():

                with gr.Column() :
            
                    question_text = gr.Textbox(lines = 2, placeholder="Enter Question..", label="Question")
                    answer_text = gr.Textbox(lines = 2, placeholder="Enter Answer or Leave it empty..", label="Answer")

                    text_button = gr.Button("Submit")

                with gr.Column() :
                    output1 = gr.Textbox(label = "Question Duplicates") 
                    output2 = gr.Textbox(label = "Related questions")

        with gr.TabItem("Add CSV File"):

            with gr.Row():
                
                question_file = gr.File(type = "file" , label="Question File", interactive=True)
                output_file = gr.File(label="Duplicate and Related Questions File")

            csv_button = gr.Button("Submit")

        text_button.click(master_of_masters, inputs=[question_text, answer_text], outputs=[output1, output2])
        csv_button.click(master_of_masters_file, inputs=[question_file], outputs=[output_file])

demo.launch()