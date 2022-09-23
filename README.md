# Project 8. Question similarity.

This repository is an implementation of the Question Duplicacy detection model developed for [Extramarks Ltd](https://www.extramarks.com). Demonstration video [here](https://www.youtube.com/watch?v=loh0_-7XLW4).

### Pipeline of the model

<img src="./Project-8-workflow.drawio.svg">


### Running the model

In order to setup the model please follwo the following steps:
1. Clone this repo from GitHub using `git clone https://github.com/VenkteshV/Question_duplicate_detection`
2. Navigate to the cloned folder : `cd Question_duplicate_detection`
3. Create a new virtual environment: `python3 -m venv venv_new`
4. Run the virtual environment just created: `source venv_new/bin/activate`
5. Install the required packages: `pip install -r requirements.txt`
6. Download the folder of data ("Data-cache") required to run the model from [here](https://drive.google.com/drive/folders/1CkCtTPEgiYcyn7iLKbx0-CruiDRRi538?usp=sharing)
7. Move the "Data-cache" folder inside `./src/`
8. Download full [Stanford CoreNLP Tagger version 3.8.0](http://nlp.stanford.edu/software/stanford-corenlp-full-2018-02-27.zip) and rename it to "stanford"
9. Move the "stanford" folder to `./src/Kw_generation/`
10. Navigate to "stanford folder": `cd src/Kw_generation/stanford`
11. Run `java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -preload tokenize,ssplit,pos -status_port 9000 -port 9000 -timeout 15000 &`
12. cd to the `cd src/Kw_generation/Unsupervised-keyphrase-extraction/src` and run `python3 app.py`
13. Download the tagging API folder from [here](https://drive.google.com/file/d/1T2-vV-ZxtqvUCcWmLng934dLXGgIVLPy/view), unzip it, rename to  "taxonomy_predictor_api" and move to `./src/Syllabus_Tagging/`
14. Open a new terminal and navigate to "taxonomy_predictor_api" folder: `cd src/Syllabus_Tagging/taxonomy_predictor_api`
15. Download the required libraries: `pip install -r requirements.txt`
16. Run `uvicorn app.main:app`
17. Open a new terminal and navigate to "src" folder: `cd src`
18. Run `python3 ui.py`

##### Development details

| Syntax                     | Description                                                                      |
| -----------                | -----------                                                                      |
| Period of development      | 15 May 2022 - 22 August 2022                                                     |
| Developed by               | [Maksimjeet Chowdhary](mailto:chowdharymaksimjeet@gmail.com), [Sanyam Goyal](mailto:sgoyal2508@gmail.com), [Venktesh V](mailto:venkteshv@iiitd.ac.in)|
| Guidance of                | [Dr. Mukesh Mohania](mailto:mukesh@iiitd.ac.in), [Dr. Vikram Goyal](mailto:vikram@iiitd.ac.in), [Mr. Deep Dwivedi](mailto:deepd@iiitd.ac.in), [Mr. Gaurav Sharma](mailto:gaurav.sharma@extramarks.com)|


 

