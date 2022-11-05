import socket 

print("Доступные команды:\n\
\tget <key> (получение значения по ключу)\n\
\tput <key> <value> (запись значения в переданный ключ)\n\
\tdelete <key> (удаление пары ключ-значение)\n\
\tsearch <value>(получение всех ключей через которые записано переданное значение)\n")

first = True
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 3434))
print("Для выхода введите exit!\n")
request = input("Введите запрос: ")
client.send(request.encode('utf-8'))
while request.lower() != 'exit':
    if(not first):
        request = input("Введите запрос: ")
        client.send(request.encode('utf-8'))
    first = False
    data = client.recv(1024).decode('utf-8')
    print(data)