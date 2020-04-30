# -*- coding: utf-8 -*-
import socket
import json
import os

MES_HALLO = 'Решите пример'
MES_LOSE = 'Вы проиграли '
MES_WRONG_ANS = 'Неправильно, попробуйте еще раз'
MES_WIN = 'Правильно! Вы выиграли!'

def messageToServer(ans):
    return {"answer": ans}

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 8080))
from_server = client.recv(4096)
data = json.loads(from_server.decode("utf-8"))
while True:
    print(data["message"])
    user_ans = input(data["expression"])
    client.send(json.dumps(messageToServer(user_ans)).encode("utf-8"))
    from_server = client.recv(4096)
    data = json.loads(from_server.decode("utf-8"))
    if data["message"] == MES_WIN or data["message"] == MES_LOSE:
        print(data["message"])
        break
os.system("pause")
client.close()
