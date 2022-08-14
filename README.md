# Project 8. Question similarity.

### Pipeline of the model

<img src="./Project-8-workflow.drawio.svg">



java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -preload tokenize,ssplit,pos -status_port 9000 -port 9000 -timeout 15000 &
