import socket
import os
from Enigma import Enigma

# Client can send and recive files to and from server
# Encryption and Decryption only work on TEXT FILES !


def Recv_File(s):

    filename = input("ENTER FILE NAME : ")

    if filename != 'q':
        #print("this far")
        s.send(filename.encode())
        #print("this far")
        data = s.recv(1024)
        #print(data[:6])
        #print("this far")
        if data[:6].decode() == "EXISTS":
            #print("this far4")
            filesize = int(data[6:])
            message = input(f"File EXISTS {filesize} bytes do you want to DOWNLOAD (Y/N) ")
            if message == 'Y':
                s.send('OK'.encode())
                f = open('new_' + filename,'wb')
                data = s.recv(1024)
                total_recv = len(data)
                #print("Data now is" + data.decode())
                f.write(data)
                while total_recv < filesize:
                    data = s.recv(1024)
                    total_recv += len(data)
                    #print("IN loop Data now is" + data.decode())
                    f.write(data)
                    progress = total_recv/float(filesize)*100
                    print(f"Progress {progress} % Done")


                print("DOWNLOAD COMPLETE")
            else: print("Exiting ...")
        else:
            print("FILE DOES NOT EXIST")



    s.close()

def Send_File(sock):
    filename = input("Enter file NAME: ")
    sock.send(filename.encode())
    if os.path.isfile(filename):
        print("File EXISTS")
        sock.send(("EXISTS" + str(os.path.getsize(filename))).encode())

        user_response = sock.recv(1024)

        if user_response[:2].decode() == 'OK':
            #print("this far")

            with open(filename,'rb') as f:
                #print("this far1")
                bytes_to_send = f.read(1024)
                sock.send(bytes_to_send)
                while bytes_to_send != "".encode():
                    #print("this far2")
                    bytes_to_send = f.read(1024)
                    #print(bytes_to_send)
                    sock.send(bytes_to_send)
                print("FILE SENT!")



        else:
            print("Error user_response not ok");
            sock.close()

    else:
        print("File does not EXIST")
        sock.send("FILE DOES NOT EXIST".encode())

    sock.close();

def Encrypt():
        disks = input("Enter disks position Must be from 0-3 d1[] d2[] d3[] \n Like this '012 or 212 or 000' : ") #enter like 000/012/222/333/011
        filename = input("Enter file name: ")


        while len(disks)>3:
            disks = input("Enter disks position 0-3 d1[] d2[] d3[] : ")

        if os.path.isfile(filename):
            f = open(filename,"r")
            LineString = f.read()
            f.close()
        else:
            print("File does not exist !")

        f = open("enc" + filename,"a")
        f.write(Enigma.encrypt(0,int(disks[0]),int(disks[1]),int(disks[2]),LineString))
        f.close()



def Decrypt():
    disks = input("Enter disks position 0-3 d1[] d2[] d3[] \n Like this '012 or 212 or 000' : ")
    filename = input("Enter file name: ")


    while len(disks)>3:
        disks = input("Enter disks position 0-3 d1[] d2[] d3[] : ")

    if os.path.isfile(filename):
        f = open(filename,"r")
        LineString = f.read()
        f.close()
    else:
        print("File does not exist !")

    f = open("dec" + filename,"a")
    f.write(Enigma.decrypt(0,int(disks[0]),int(disks[1]),int(disks[2]),LineString)) # iska oshte 1 parametur ?








def Main():
    host = '127.0.0.1'
    port = 5000

    s = socket.socket()
    s.connect((host,port))
    #print("CONNECTED to" + str(s))

    print(s.recv(1024).decode())
    choice = input("Enter your choice ")
    s.send(choice.encode())
    #print("thisfar0")
    if choice == "1":
        #print("thisfar1")
        print(s.recv(1024).decode())
        Send_File(s)
    elif choice == "2":
        print(s.recv(1024).decode())
        Recv_File(s)
    elif choice == "3":
        Encrypt()

    elif choice == "4":
        Decrypt()
    else:
        print("Choice error !")





    s.close()

if __name__ == '__main__':
    Main()
