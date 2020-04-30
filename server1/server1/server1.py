import socket
import random
import json
import threading

MES_HALLO = 'Решите пример'
MES_LOSE = 'Вы проиграли '
MES_WRONG_ANS = 'Неправильно, попробуйте еще раз'
MES_WIN = 'Правильно! Вы выиграли!'

def messageToClient(message, expr):
    return {"message": message, "expression": expr}

def checkAns(a, b, znak, user_ans):
    if znak == 0:
        ans  = a + b
    if znak == 1:
        ans  = a - b
    if znak == 2:
        ans  = a * b
    if user_ans == ans:
        return True
    else:
        return False


def listenClient(client, address):
    event.wait()
    global flag
    print(address)
    data = json.dumps(messageToClient(MES_HALLO, expression)).encode("utf-8")
    client.send(data)
    while True:
        try:
            from_client = json.loads(client.recv(4096).decode("utf-8"))
            user_ans = int(from_client["answer"])
            if checkAns(a, b, znak, user_ans) and flag:
                flag = False
                client.send(json.dumps(messageToClient(MES_WIN, expression)).encode("utf-8"))
                client.close()
                print('client disconnected')
                return
            elif not checkAns(a, b, znak, user_ans) and flag:
                client.send(json.dumps(messageToClient(MES_WRONG_ANS, expression)).encode("utf-8"))
            else:
                client.send(json.dumps(messageToClient(MES_LOSE, expression)).encode("utf-8"))
                client.close()
                print('client disconnected')
                return
        except (ConnectionAbortedError, ConnectionResetError):
            print("Ошибка соединения")
            client.close()
            return


if __name__ == '__main__':
    znak_str = ["+", "-", "*"]
    a = random.randint(0, 100)
    b = random.randint(0, 100)
    znak = random.randint(0, 2)
    expression = f'{a} {znak_str[znak]} {b} ='
    if znak == 0:
        ans  = a + b
    if znak == 1:
        ans  = a - b
    if znak == 2:
        ans  = a * b
    flag = True
    client_count = int(input("Введите количество игроков: "))
    print("Ожидание игроков...")
    user_count = 0
    event = threading.Event()
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv.bind(('localhost', 8080))
    serv.listen(5)
    while True:
        try:
            client, address = serv.accept()
            threading.Thread(target=listenClient, args=(client, address)).start()
            user_count += 1
            if client_count == user_count:
                print("Подключились игроки: ")
                event.set()
                break
        except OSError:
            print("Ошибка коннекта!")
    serv.close()
