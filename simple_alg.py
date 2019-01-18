def compute_jaccard_similarity(set_1, set_2):
  return len(set_1 & set_2) / len(set_1 | set_2)

# read the file
lines = [line.rstrip('\n') for line in open('./question-dataset/question_4k.tsv')]

# store for our list of sets
words_in_questions = []

# generate the list of sets of words in each question
for line in lines:
  if len(line.split('\t')) is 2:
    words_in_questions.append([line.split('\t')[0], line.split('\t')[1].lower().replace('?', '').split(' ')])

# remove first element because it will always be qid: question
words_in_questions.pop(0)

for question in words_in_questions:
  question[0] = int(question[0])
  question[1] = set(question[1])

similar_questions = []

for question in range(0, len(words_in_questions)):
  for compare_question in range(question + 1, len(words_in_questions)):
    if (compute_jaccard_similarity(words_in_questions[question][1], words_in_questions[compare_question][1]) >= 0.6):
      similar_questions.append([words_in_questions[question][0], words_in_questions[compare_question][0]])

for similar_question in similar_questions:
  
