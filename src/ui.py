import gradio as gr
from master import run_model

def master_of_masters(Question, Answer=""):
    return run_model(Question, Answer)

question_text = gr.Textbox(lines = 2, placeholder="Enter Question..")
answer_text = gr.Textbox(lines = 2, placeholder="Enter Answer or Leave it empty..")

output1 = gr.Textbox(label = "Exact Duplicates") 
output2 = gr.Textbox(label = "Duplicates - Definitions") 
output3 = gr.Textbox(label = "Most Related questions") 


desc = ("An application to prevent academicians from creating duplicate questions by suggesting near duplicates of a question present in the database.  \n"

        "Definition of Duplicacy : "

        )

article = ("Exact Duplicates :  \n"
        "Duplicates Definition :  \n"
        "Related Questions : "
        )

gui = gr.Interface(
    
    fn = master_of_masters,
    inputs=[question_text, answer_text],
    outputs=[output1, output2, output3],
    title = "Online Question Duplicity Finder",
    description = desc,
    article=article
)

gui.launch(share = True)
