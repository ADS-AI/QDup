Create basic structure of our pipeline for demonstration of our model.

Dataset Requirements :

- Basedataset.csv 
    
    -> Preprocessing : questiontext.json
    -> Tagrac : syllabus.json 
    -> NLTK : Tokenised_question.json
    -> Spacy : NER.json
    -> Embedrank : Keywords.json

question_id will be used as primary key in all three files

1) questiontext.json : [ questionID, questionText ]

2) syllabus.json : [ questionId , syllabus ] 

3) Tokenised_question.json : For jaccard similarilty [ questionId, questionTokens ]

4) question_ners.json : [ questionId, questionNERs ]

5) Keywords.json : [ questionId, questionKeywords ]

Preprocessing - Correction spellings, elements name Cu -> copper, can't -> cannot, pi symbol to pi , combinations - combination ?


Decide threshold for separation based keywords

Decide how to calculate `keyword_score` : 
    i.  len(common_keyword)/len(union_keyword) OR
    ii. len(common_keyword)/len(keyword1) OR
    iii.len(common_keyword)/len(keyword2)
    (representative e.g. "what compounds has a zero dipole moment ", "the third ionization energy is maximum for ")