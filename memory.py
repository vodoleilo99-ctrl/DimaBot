# Простая память для диалога
memory = {}

def remember(user_id, message):
    if user_id not in memory:
        memory[user_id] = []
    memory[user_id].append(message)

def get_history(user_id):
    return "\n".join(memory.get(user_id, []))
