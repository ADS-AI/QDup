# Project 8. Question similarity.

### Pipeline of the model

<img src="./Project-8-workflow.drawio.svg">



java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -preload tokenize,ssplit,pos -status_port 9000 -port 9000 -timeout 15000 &

Download tagrec model from : https://drive.google.com/file/d/1T2-vV-ZxtqvUCcWmLng934dLXGgIVLPy/view?usp=drive_web
Extract folder from zip and add to "./src/Syllabus_Tagging/"
Run requirements.txt inside it
Run `uvicorn app.main:app` inside it