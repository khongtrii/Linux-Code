from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import socket
import os

root=Tk()
root.title("File Transefer")
root.geometry("450x560+500+200")
root.configure(bg="#f4fdfe")
root.resizable(False, False)

def Send():
    window=Toplevel(root)
    window.title("Send")
    window.geometry('450x560+500+200')
    window.configure(bg='#f4fdfe')
    window.resizable(False, False)

    def select_file():
        global filename
        filename=filedialog.askopenfilename(initialdir=os.getcwd(),
                                            title='Select Image File',
                                            filetypes=(('file_type','*.txt'), ('all files', '*.*')))
        
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


    image_icon1=PhotoImage(file="Image/send.png")
    window.iconphoto(False, image_icon1)

    Mbackground=PhotoImage(file="Image/profile.png")
    Label(window, image=Mbackground, bg="#f4fdfe").place(x=100, y=260)

    host=socket.gethostname()
    Label(window, text=f'ID: {host}', bg='white', fg='black').place(x=150, y=270)

    Button(window, text="+ select file", width=10, height=1, font='arial 14 bold', bg="#fff", fg="#000", command=select_file).place(x=160, y=150)
    Button(window, text="SEND", width=8, height=1, font='arial 14 bold', bg='#000', fg='#fff', command=sender).place(x=300, y=150)

    window.mainloop()
    

def Receive():
    main=Toplevel(root)
    main.title("Receive")
    main.geometry('450x560+500+200')
    main.configure(bg='#f4fdfe')
    main.resizable(False, False)

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


    image_icon2=PhotoImage(file="Image/receive.png")
    main.iconphoto(False, image_icon2)

    logo=PhotoImage(file="Image/profile.png")
    Label(main, image=logo, bg="#f4fdfe").place(x=130, y=240)
    
    Label(main, text="Receive", font=('arial', 20), bg='#f4fdfe').place(x=100, y=280)

    Label(main, text='Input sender id', font=('arial', 10, 'bold'), bg='#f4fdfe').place(x=20, y=340)
    SenderID = Entry(main, width=25, fg='black', border=2, bg='white', font=('arial', 15))
    SenderID.place(x=20, y=370)
    SenderID.focus()

    Label(main, text='filename for the incoming file:', font=('arial', 10, 'bold'), bg='#f4fdfe').place(x=20, y=420)
    incoming_file = Entry(main, width=25, fg='black', border=2, bg='white', font=('arial', 15))
    incoming_file.place(x=20, y=450)

    imageicon=PhotoImage(file='Image/arrow.png')
    rr=Button(main, text="Receive", compound=LEFT, image=imageicon, width=130, bg="#39c790", font='arial 14 bold', command=receiver)
    rr.place(x=20,y=500)


    main.mainloop()


#icon
image_icon = PhotoImage(file="Image/icon.png")
root.iconphoto(False, image_icon)

Label(root, text="File Transfer", font=('Acumin Variable Concept', 20, 'bold'), bg="#f4fdfe").place(x=20, y=30)
Frame(root, width=400, height=2, bg="#f3f5f6").place(x=25, y=80)

send_image=PhotoImage(file="Image/send.png")
send=Button(root, image=send_image, bg="#f4fdfe", bd=0, command=Send)
send.place(x=80, y=100)

receive_image = PhotoImage(file="Image/receive.png")
receive=Button(root, image=receive_image, bg="#f4fdfe", bd=0, command=Receive)
receive.place(x=330, y=100)

#label
Label(root, text="Send", font=('Acumin Variable Concept', 17, 'bold'), bg="#f4fdfe").place(x=65, y=150)
Label(root, text="Receive", font=('Acumin Variable Concept', 17, 'bold'), bg="#f4fdfe").place(x=300, y=150)

# background=PhotoImage(file="Image/7156.jpg")
# Label(root, image=background).place(x=-2, y=323)



root.mainloop()