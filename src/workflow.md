Create basic structure of our pipeline for demonstration of our model.

Decide threshold for separation based keywords

Decide how to calculate `keyword_score` : 
    i.  len(common_keyword)/len(union_keyword) OR
    ii. len(common_keyword)/len(keyword1) OR
    iii.len(common_keyword)/len(keyword2)
    (representative e.g. "what compounds has a zero dipole moment ", "the third ionization energy is maximum for ")

Before Monday: 



1. Replace word with dictionary
   1. Replace single elements with their full names (e.g. Cu -> Copper)
   2. Replace "pi" to pi symbol
   3. Replace negated abbreviations with "NOT VERB" (e.g. can't -> can not)
   4. Lemmatization
2. See which kw model works better
3. See which tags work better
4. Calculate sentence embeddings 
   1. Write code to calculate sentence embeddings for input question and compare it with data