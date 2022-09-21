def check_negation(ques1, ques2) :
  wrong_spellings = {"cannot":"can not", "doesnot":"does not", "couldnot":"could not", "canot":"can not", "wouldnot":"would not", "should not":"should not", "havenot":"have not", "hasnot":"has not", "hadnot":"had not", "arenot":"are not"}
  articles = set(['a', 'the', 'an'])
  w1 = ques1.lower().split()
  w2 = ques2.lower().split()
  w1 = [w for w in w1 if w not in articles]
  w2 = [w for w in w2 if w not in articles]
  w1 = [wrong_spellings[w] if w in wrong_spellings else w for w in w1]
  w2 = [wrong_spellings[w] if w in wrong_spellings else w for w in w2]
  cnt1 = 0
  cnt2 = 0 
  for i in w1 :
    if ( i == 'not' ) | ( 'not' in i.split() ) :
      cnt1+=1
  for i in w2 :
    if ( i == 'not' ) | ( 'not' in i.split() ) :
      cnt2+=1
  if(cnt1 != cnt2) :
    return 1
  return 0

def negation_pairs(input, search_ques) :
  ans = [ ]
  other=[ ]
  for i in search_ques :
    if( check_negation(input, i) == 0 ) :
      ans.append(i) 
    else :
      other.append(i)
  return ans, other