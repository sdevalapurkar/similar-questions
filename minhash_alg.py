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
  words_list_new = list(set(word_list[1]))
  new_list = []

  for word in words_list_new:
    word = word.encode('utf-8')
    new_list.append(hash(word, bits=64))

  fnv_hashes[word_list[0]] = new_list

hash_tables_with_signature_as_key = [dict() for i in range(1, 15)]
hash_tables_with_qid_as_key = [dict() for i in range(1, 15)]
hash_sigs_list = dict()
index = 0

for hash_table in hash_tables_with_signature_as_key: # for each of 14 hash tables
  collect_sigs = dict()

  for i in range(6): # do it 6 times and generate minhashes
    ai = uuid.uuid4().int & (1<<64)-1
    bi = uuid.uuid4().int & (1<<64)-1

    for key, value in fnv_hashes.items(): # for each question
      list = []

      for fnv_hash in value: # for each fnv hash of each word in question
        min_hash_val = ((ai * fnv_hash) + bi) % p
        list.append(min_hash_val) # store these minhashes (all 6)

      if (collect_sigs.get(key) is not None):
        collect_sigs[key] += str(min(list))
      else:
        collect_sigs[key] = str(min(list))

  hash_tables_with_qid_as_key[index] = dict(collect_sigs)

  for key, value in collect_sigs.items():
    if (hash_table.get(value) is not None):
      hash_table[value].append(key)
    else:
      hash_table[value] = [key]

  index += 1

similar_questions_dict = dict()

for hash_table in hash_tables_with_signature_as_key:
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

words_in_questions_dict = dict()

for question in words_in_questions:
  question[0] = int(question[0])
  question[1] = set(question[1])
  words_in_questions_dict[question[0]] = question[1]

final_sim_questions_dict = dict()

for key, value in similar_questions_dict.items():
  int_key = int(key)

  for qid in value:
    int_qid = int(qid)

    if (compute_jaccard_similarity(words_in_questions_dict[int_key], words_in_questions_dict[int_qid]) >= 0.6):
      if (final_sim_questions_dict.get(int_key) is not None):
        final_sim_questions_dict[int_key].append(int_qid)
      else:
        final_sim_questions_dict[int_key] = [int_qid]

output_file = open('question_sim_4k.tsv','w+')

output_file.write('qid \t similar-qids \n')

for key in sorted(final_sim_questions_dict.keys()):
  if (len(final_sim_questions_dict[key]) > 1):
    output_file.write(str(key) + '\t' + (', '.join(str(e) for e in final_sim_questions_dict[key] if e != key)) + '\n')
  else:
    output_file.write(str(key) + '\t' + '\n')
