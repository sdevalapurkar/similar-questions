from fnv import *
import uuid

p = 15373875993579943603

lines = [line.rstrip('\n') for line in open('./question-dataset/question_10.tsv')]

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

print(hash_tables)
