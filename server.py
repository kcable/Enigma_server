import socket
import os
import threading

#сървъра на който пращам и изпращам файлове може няколко клиента да се свържат едновременно стига да
# са избрали какво действие да извършат
#тестван със txt jpg rar 

def RetriveFile(name,sock):
    filename = sock.recv(1024)
    if os.path.isfile(filename):
        sock.send(("EXISTS" + str(os.path.getsize(filename))).encode())
        #print("this far -1")
        user_response = sock.recv(1024)
        print(user_response[:2].decode())
        #print("this far 0")

        if user_response[:2].decode() == 'OK':
            #print("this far 1")
            with open(filename,'rb') as f:
                #print("this far 2")
                bytes_to_send = f.read(1024)
                sock.send(bytes_to_send)
                #print("this far 3")
                while bytes_to_send != "".encode():
                    bytes_to_send = f.read(1024)
                    sock.send(bytes_to_send)
                f.close()
        else:
            print("Error user_response not ok");sock.close();

    else:
        sock.send("FILE DOES NOT EXIST".encode())

    sock.close();

def AcceptFile(name,sock):

    filename = sock.recv(1024)
    flilename = filename.decode()

    #print("this far")
    #s.send(filename.encode())
    #print("this far")
    data = sock.recv(1024)
    #print(data[:6])
    #print("this far")
    if data[:6].decode() == "EXISTS":
        #print("this far4")
        filesize = int(data[6:])
        print(f"File EXISTS {filesize} bytes downloading ... ")

        sock.send('OK'.encode())
        f = open('client_' + filename.decode(),'wb')
        data = sock.recv(1024)
        total_recv = len(data)
        #print("Data now is" + data.decode())
        f.write(data)
        while total_recv < filesize:
            data = sock.recv(1024)
            total_recv += len(data)
            #print("IN loop Data now is" + data.decode())
            f.write(data)
            progress = total_recv/float(filesize)*100
            print(f"Progress {progress} % Done")


        print("DOWNLOAD COMPLETE")
        f.close()

    else:
        print("File does not exist stoping ...")





    sock.close()





def Main():
    host ='127.0.0.1'
    port = 5000

    s = socket.socket()
    s.bind((host,port))

    s.listen(5)

    print("SERVER STARTED")


    while True:
        c, address = s.accept()
        print(f"CLIENT CONNECTED <{address}>")
        c.send("Hello you have connected to the server what would you like to do:\n 1.Send a flile  2.Download File 3.Encrypt a file 4.Decript a file ".encode())
        client_anwser = c.recv(1024).decode()
        print(client_anwser)

        if client_anwser == "1":
            #print("thisfar0")
            c.send("You have chosen to send a file".encode())
            #print("thisfar1")
            t = threading.Thread(target = AcceptFile, args =("retrThread",c))
            t.start()



        elif client_anwser == "2":
            c.send("You have chosen to Download a file".encode())
            t = threading.Thread(target = RetriveFile, args =("acceptThread",c))
            t.start()

        else:
            c.send("Error!".encode())
            print("Client entered wrong choice or chose to Encrypt/Decrypt")



    s.close()

if __name__ == '__main__':
    Main()
