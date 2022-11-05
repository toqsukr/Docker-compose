from base64 import decode
import redis
import socket


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', 3434))
server.listen(1)
print("Waiting")

client_socket, address = server.accept()
print("Connection success!")
redis_client = redis.Redis(host="my_data", port=6379, db=0)
first = True
request = (client_socket.recv(1024)).decode("utf-8")
while request.lower() != "exit":
    if(not first):  request = (client_socket.recv(1024)).decode('utf-8')
    first = False
    flag = True
    if(len(request) > 2):        
        if(request[:4] == "get " and len(request) > 4):
            answer = redis_client.get(request[4:])
            if(answer != None):   answer = answer.decode('utf-8')
            mess = f"Success getting\nAnswer: {answer}"
            print(f"request: {request}")
        elif(request[:4] == "put " and len(request) > 4):
            request = request[4:]
            scnd = request.find(" ")
            key = request[:scnd]
            value = request[scnd+1:]
            redis_client.set(key, value)
            mess = 'Success putting'
            print(f"request: put {request}")
        elif(request[:7] == "delete " and len(request) > 7):
            redis_client.delete(request[7:])
            mess = 'Success deleting'
            print(f"request: {request}")
        elif(request[:7] == "search " and len(request) > 7):
            spi_keys = redis_client.keys("*")
            print(spi_keys)
            answer = []
            for key in spi_keys:
                key = key.decode('utf-8')
                if(redis_client.get(key).decode('utf-8') == request[7:]):
                    answer.append(key)
            mess = f"Success searching!\nAnswer: {answer}"
            print(mess)
            print(f"request: {request}")
        elif(request.lower() != 'exit'):  flag = False
        else:
            print("Exiting")
            mess = 'Exiting'
    else:   flag = False
    if(not flag):
        mess = 'Incorrect request!'
        print(f"{request} - некорректный запрос!")
    client_socket.send(mess.encode('utf-8'))
server.close()
redis_client.close()
