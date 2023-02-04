
import tkinter as tk
import socket
import threading



window = tk.Tk()
window.title("ChaD server Room")
window.geometry('400x400')
chat_history = tk.Text()
chat_history.place(x=100, y=0, height = 350, width = 300)
messages_frame = tk.Frame(window)
msg_list = tk.Listbox(messages_frame, height=15, width=50)
msg_list.pack()
"""log = []
window = tk.Tk()
window.title("ChaD server Room")
window.geometry('400x400')
text_box = tk.Text()
text_box.place(x=100, y=350, height = 40, width = 250)
chat_history = tk.Text()
chat_history.place(x=100, y=0, height = 350, width = 300)
messages_frame = tk.Frame(window)
my_msg = tk.StringVar()  # For the messages to be sent.
my_msg.set("Type your messages here.")
scrollbar = tk.Scrollbar(messages_frame)  # To navigate through past messages.
# Following will contain the messages.
msg_list = tk.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
msg_list.pack(side=tk.LEFT, fill=tk.BOTH)
msg_list.pack()
messages_frame.pack()
entry_field = tk.Entry(window, textvariable=my_msg)
entry_field.bind("<Return>", print('sendingf'))
entry_field.pack()
send_button = tk.Button(window, text="Send", command=print('sending'))
send_button.pack()"""


fobj = open("chat_log.txt", "w")
fobj.write("Initiating chat log... \n")
fobj.close()












server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
#host_ip = socket.gethostbyname(host_name) 
host_ip = '10.121.127.104'
print("Server IP: " + host_ip)
port = int(input("Enter Port: "))

server_socket.bind((host_ip, port))
server_socket.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        #log.append(message)
        #msg_list.insert(tk.END, message)
        #chat_history.insert(tk.END, message)
        #chat_history.insert(tk.END, '\n')
        #tk.mainloop()
        #tk.mainloop()
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            
            fobj = open("chat_log.txt", "a")
            fobj.write(str(message)+ '\n')
            fobj.close()
            
            #tk.mainloop()

            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(index)
            client.close()
            broadcast((nicknames[index] + " has left the chat").encode())
            nicknames.remove(index)
            break

def receive():
    while True:
        client, address = server_socket.accept()
        print("Connected with" + str(address))

        client.send('NICK'.encode())
        nickname = client.recv(1024).decode()
        nicknames.append(nickname)
        clients.append(client)

        print('Nickname of the client is: ' + nickname)
        broadcast((nickname + ' has joined the chat. \n ').encode())
        client.send(' connected to the server'.encode())

        thread = threading.Thread(target=handle, args=(client, ))
        thread.start()
        
        #tk.mainloop()


print('Server is starting!')

receive()