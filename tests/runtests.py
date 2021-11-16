from threading import Thread
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
def getchats(tokens):
    chats = []
    for token in tokens:
        chats.append(messages.chats(token))
    return chats

def delete(tokens):
    for token in tokens:
        users.delete(token)
def startt(count=1):
    tokens,ids = initusers(count)
    print(tokens,ids)
    genmessages(tokens,ids)
    print(getupdates(tokens))
    print(getchats(tokens))
    delete(tokens)
if __name__ == "__main__":
    for t in range(1):
        th = Thread(target=startt).start()
