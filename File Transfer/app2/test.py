from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import socket
import os
import uuid

"""Create root - window"""
""""""
root=Tk()
root.title("File Transefer")
root.geometry("700x470+500+200")
root.configure(bg="#f4fdfe")
root.resizable(False, False)
""""""


"""Set up ICON for app"""
""""""
root_ico = PhotoImage(file='Image/app.png')
root.iconphoto(False, root_ico)
""""""

"""Build define"""
""""""
def send_frame():
    window=Toplevel(root)
    window.title("Send File")
    window.geometry('450x700+1210+200')
    window.configure(bg='#f5ebe0')
    window.resizable(False, False)
    window_ico = PhotoImage(file='Image/send.png')
    window.iconphoto(False, window_ico)

    def choose_file():
        global filename 
        filename=filedialog.askopenfilename(initialdir=os.getcwd(),
                                            title='Select Image File',
                                            filetypes=(('all files', '*.*'), ('file_type','*.txt')))
        
    def sender():
        s = socket.socket()
        host = socket.gethostname()
        port = 8080
        s.bind((host, port))
        s.listen(1)
        print(f"Host: {host}")
        print("Waiting for any incoming connections...")
        conn, addr = s.accept()
        print(f"Connection established with {addr}")
        
        with open(filename, 'rb') as file:
            while (data := file.read(1024)):
                conn.send(data)
        conn.close()
        print("Data has been transmitted successfully.")

    device_img = PhotoImage(file='Image/device.png')
    Label(window, image=device_img, bg='#f5ebe0').place(x=10, y=10)

    host=socket.gethostname()
    Label(window, text=f'{host}', bg='#f5ebe0', fg='black').place(x=55, y=15)

    add_btn = PhotoImage(file='Image/add.png')
    Button(window, image=add_btn, bg='#d4a373', width=150, height=40, command=choose_file).place(x=100, y=300)
    Button(window, text="SEND", font=('Acumin Variable Concept', 14, 'bold'), bg='#d4a373', command=sender).place(x=100, y=355)


    window.mainloop()

def receive_frame():
    main=Toplevel(root)
    main.title("Send File")
    main.geometry('450x700+1210+200')
    main.configure(bg='#f5ebe0')
    main.resizable(False, False)

    main_ico = PhotoImage(file='Image/receive.png')
    main.iconphoto(False, main_ico)

    def receiver():
        ID = SenderID.get()
        filename1 = incoming_file.get()
        s = socket.socket()
        port = 8080
        s.connect((ID, port))
        
        with open(filename1, 'wb') as file:
            while (data := s.recv(1024)):
                file.write(data)
        s.close()
        print("File has been received successfully.")

    main_fr1 = Frame(main, width=300, height=400, bg='#d4a373')
    main_fr1.place(x=75, y=150)

    find_img = PhotoImage(file='Image/find.png')
    Label(main_fr1, image=find_img, bg='#d4a373').place(x=30, y=30)

    SenderID = Entry(main_fr1, width=30, bg='#ddb892')
    SenderID.place(x=30, y=70)

    type_img = PhotoImage(file='Image/type.png')
    Label(main_fr1, image=type_img, bg='#d4a373').place(x=30, y=110)

    incoming_file = Entry(main_fr1, width=30, bg='#ddb892')
    incoming_file.place(x=30, y=150)

    rev_img = PhotoImage(file='Image/receive.png')
    Button(main_fr1, image=rev_img, bg='#d4a373', command=receiver).place(x=175, y=190)

    main.mainloop()
""""""


"""Frame 1 - HEADDING"""
""""""
fr1 = Frame(root, width=700, height=100, bg="#f5ebe0")
fr1.place(x=0, y=0)
Label(fr1, text="FILE TRANSFER", font=('Acumin Variable Concept', 20, 'bold'), bg="#f5ebe0", fg='#d5bdaf', border=1).place(x=20, y=30)

sent_ico1 = PhotoImage(file='Image/profile.png')
Label(fr1, image=sent_ico1, bg="#f5ebe0").place(x=600, y=10)
""""""


"""Frame 2 - SEND & BUTTON & IMG BUTTON"""
""""""
fr2 = Frame(root, width=300, height=100, bg="#d5bdaf")
fr2.place(x=200, y=150)

Button(fr2, text='SEND', width=13, height=1, font=('Acumin Variable Concept', 10, 'bold'), border=None, bg='#d6ccc2', command=send_frame).place(x=33, y=37)

sent_ico2 = PhotoImage(file='Image/send.png')
Label(fr2, image=sent_ico2, bg="#d5bdaf").place(x=200, y=36)
""""""


"""Frame 3 - RECEIVE & BUTTON & IMG BUTTON"""
""""""
fr3 = Frame(root, width=300, height=100, bg="#d5bdaf")
fr3.place(x=200, y=280)

Button(fr3, text='RECEIVE', width=13, height=1, font=('Acumin Variable Concept', 10, 'bold'), border=None, bg='#d6ccc2', command=receive_frame).place(x=33, y=37)

sent_ico3 = PhotoImage(file='Image/receive.png')
Label(fr3, image=sent_ico3, bg="#d5bdaf").place(x=200, y=36)
""""""


"""Loop frame"""
root.mainloop()