import gradio as gr
from master import run_model

demo = gr.Interface(fn=run_model, inputs="text", outputs=["text","text","text"])
demo.launch()
