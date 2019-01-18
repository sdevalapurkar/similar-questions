import uuid
rand64 = uuid.uuid4().int & (1<<64)-1
print(rand64)
