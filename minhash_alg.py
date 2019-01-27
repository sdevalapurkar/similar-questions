from fnv import *
import uuid

p = 15373875993579943603

def compute_jaccard_similarity(set_1, set_2):
  return len(set_1 & set_2) / len(set_1 | set_2)

lines = [line.rstrip('\n') for line in open('./question-dataset/question_150k.tsv')]

words_in_questions = []

for line in lines:
  if len(line.split('\t')) is 2:
    words_in_questions.append([line.split('\t')[0], line.split('\t')[1].lower().replace('?', '').split(' ')])

words_in_questions.pop(0)

fnv_hashes = dict()

for word_list in words_in_questions:
  list = []

  for word in word_list[1]:
    word = word.encode('utf-8')
    list.append(hash(word, bits=64))

  fnv_hashes[word_list[0]] = list

hash_tables = [dict() for i in range(1, 15)]
min_hash_sigs_dict = dict()

for hash_table in hash_tables:
  for i in range(6):
    ai = uuid.uuid4().int & (1<<64)-1
    bi = uuid.uuid4().int & (1<<64)-1

    for key, value in fnv_hashes.items():
      list = []
      hash_sigs_list = []

      for fnv_hash in value:
        min_hash_val = ((ai * fnv_hash) + bi) % p
        list.append(min_hash_val)
        hash_sigs_list.append(str(min(list)))

      signature = ','.join(hash_sigs_list)

      if (hash_table.get(signature) is not None):
        hash_table[signature].append(key)
      else:
        hash_table[signature] = [key]

similar_questions_dict = dict()

for hash_table in hash_tables:
  for key, value in hash_table.items():
    if (len(value) > 1):
      temp_qid_list = value

      for qid in value:
        if (similar_questions_dict.get(qid) is not None):
          for temp_qid in temp_qid_list:
            if temp_qid not in similar_questions_dict[qid]:
              similar_questions_dict[qid].append(temp_qid)
        else:
          similar_questions_dict[qid] = temp_qid_list

updated_similar_questions_dict = dict()

for key, value in similar_questions_dict.items():
  for elem in value:
    if (key is not elem):
      if (updated_similar_questions_dict.get(key) is not None):
        updated_similar_questions_dict[key].append(elem)
      else:
        updated_similar_questions_dict[key] = [elem]

words_in_questions_dict = dict()

for question in words_in_questions:
  question[0] = int(question[0])
  question[1] = set(question[1])
  words_in_questions_dict[question[0]] = question[1]

final_sim_questions_dict = dict()

for key, value in updated_similar_questions_dict.items():
  int_key = int(key)

  for qid in value:
    int_qid = int(qid)

    if (compute_jaccard_similarity(words_in_questions_dict[int_key], words_in_questions_dict[int_qid]) >= 0.6):
      if (final_sim_questions_dict.get(int_key) is not None):
        final_sim_questions_dict[int_key].append(int_qid)
      else:
        final_sim_questions_dict[int_key] = [int_qid]

output_file = open('question_sim_150k.tsv','w+')

output_file.write('qid \t similar-qids \n')

for q in words_in_questions:
  flag = False

  for key, value in final_sim_questions_dict.items():
    if int(key) == int(q[0]):
      flag = True
      output_file.write(str(key) + '\t' + (', '.join(str(e) for e in value)) + '\n')
  if not flag:
    output_file.write(str(q[0]) + '\t' + '\n')
