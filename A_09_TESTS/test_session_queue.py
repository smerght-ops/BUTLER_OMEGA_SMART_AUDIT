from A_03_ORCHESTRATION.session_queue import SessionQueue

q = SessionQueue()

q.push("создай картинку")
q.push("напиши код")
q.push("проанализируй фото")

print("SIZE =", q.size())

while not q.is_empty():
    print(q.pop())
