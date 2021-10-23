import messages,updates,users
import time,uuid

def initusers(count=2):#Регистрирует пару пользователей и возвращает токены
    tokens,ids = [],[]
    for d in range(count):
        passw = uuid.uuid4()
        email = uuid.uuid4()
        user = users.reg(f'user{d}',email,passw)
        if 'id' in user:
            print(f'Зарегистрировано: {user}')
            auth = (
                users.auth(email,passw))
            if 'token' in auth:
                print(f'Авторизовано!: {user}')
                tokens.append(auth['token'])
                ids.append(auth['id'])
            else:
                print(f'Ошибка при авторизации:\n{auth}')
        else: print(f"Ключ 'id' отсутствует!\n{user}")
    return tokens,ids
def genmessages(tokens,ids):#генерирует сообщения от каждого к каждому
    for token in tokens:
        for id in ids:
            print(messages.send(token,'test message',id))

def getupdates(tokens):
    updatess = []
    for token in tokens:
        updatess.append(updates.get(token))
    return updatess

def delete(tokens):
    for token in tokens:
        users.delete(token)
if __name__ == "__main__":
    tokens,ids = initusers(10)
    print(tokens,ids)
    genmessages(tokens,ids)
    print(getupdates(tokens))
    delete(tokens)