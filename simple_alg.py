def compute_jaccard_similarity(set_1, set_2):
  if set_1 == set_2:
    return 0

  return len(set_1 & set_2) / len(set_1 | set_2)

lines = [line.rstrip('\n') for line in open('./question-dataset/question_4k.tsv')]

words_in_questions = []

for line in lines:
  if len(line.split('\t')) is 2:
    words_in_questions.append([line.split('\t')[0], line.split('\t')[1].lower().replace('?', '').split(' ')])

words_in_questions.pop(0)

for question in words_in_questions:
  question[0] = int(question[0])
  question[1] = set(question[1])

similar_questions = []

for question in range(0, len(words_in_questions)):
  for compare_question in range(0, len(words_in_questions)):
    if (compute_jaccard_similarity(words_in_questions[question][1], words_in_questions[compare_question][1]) >= 0.6):
      similar_questions.append([words_in_questions[question][0], words_in_questions[compare_question][0]])

sim_questions_dict = dict()

for q in range(0, len(similar_questions)):
  if similar_questions[q][0] in sim_questions_dict:
    sim_questions_dict[similar_questions[q][0]].append(similar_questions[q][1])
  else:
    sim_questions_dict[similar_questions[q][0]] = [similar_questions[q][1]]

output_file = open('question_sim_4k.tsv','w+')

output_file.write('qid \t similar-qids \n')

for q in words_in_questions:
  flag = False
  for key, value in sim_questions_dict.items():
    if int(key) == int(q[0]):
      flag = True
      output_file.write(str(key) + '\t' + (', '.join(str(e) for e in value)) + '\n')
  if not flag:
    output_file.write(str(q[0]) + '\t' + '\n')
