from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import socket
import os
import threading

root = Tk()
root.title("File Transfer")
root.geometry("700x470+500+200")
root.configure(bg="#f4fdfe")
root.resizable(False, False)

# ICON for app
root_ico = PhotoImage(file='Image/app.png')
root.iconphoto(False, root_ico)

# Global variables
file_queue = []  # Queue for file transfer

def send_frame():
    window = Toplevel(root)
    window.title("Send File")
    window.geometry('450x700+1210+200')
    window.configure(bg='#f5ebe0')
    window.resizable(False, False)
    window_ico = PhotoImage(file='Image/send.png')
    window.iconphoto(False, window_ico)

    def choose_files():
        global file_queue
        files = filedialog.askopenfilenames(initialdir=os.getcwd(),
                                            title='Select Files',
                                            filetypes=(('all files', '*.*'), ('text files', '*.txt')))
        file_queue = list(files)
        messagebox.showinfo("Files Selected", f"{len(file_queue)} files added to queue.")

    def sender():
        if not file_queue:
            messagebox.showerror("Error", "No files selected to send.")
            return

        s = socket.socket()
        host = socket.gethostname()
        port = 8080
        s.bind((host, port))
        s.listen(1)
        print(f"Host: {host}")
        print("Waiting for any incoming connections...")
        conn, addr = s.accept()
        print(f"Connection established with {addr}")

        for file in file_queue:
            conn.send(os.path.basename(file).encode())  # Send file name
            with open(file, 'rb') as f:
                while (data := f.read(1024)):
                    conn.send(data)
            conn.send(b"<END>")  # Indicate file transfer completion
            print(f"{os.path.basename(file)} has been sent.")

        conn.close()
        print("All files have been transmitted successfully.")

    device_img = PhotoImage(file='Image/device.png')
    Label(window, image=device_img, bg='#f5ebe0').place(x=10, y=10)

    host = socket.gethostname()
    Label(window, text=f'{host}', bg='#f5ebe0', fg='black').place(x=55, y=15)

    add_btn = PhotoImage(file='Image/add.png')
    Button(window, image=add_btn, bg='#d4a373', width=150, height=40, command=choose_files).place(x=100, y=300)
    Button(window, text="SEND", font=('Acumin Variable Concept', 14, 'bold'), bg='#d4a373', command=sender).place(x=100, y=355)

    window.mainloop()

def receive_frame():
    main = Toplevel(root)
    main.title("Receive File")
    main.geometry('450x400+1210+200')
    main.configure(bg='#f5ebe0')
    main.resizable(False, False)

    main_ico = PhotoImage(file='Image/receive.png')
    main.iconphoto(False, main_ico)

    def receiver():
        s = socket.socket()
        host = SenderID.get()
        port = 8080
        try:
            s.connect((host, port))
            print(f"Connected to {host}")

            while True:
                # Receive file name
                file_name = s.recv(1024).decode()
                if not file_name:
                    break
                
                print(f"Receiving file: {file_name}")
                with open(file_name, 'wb') as f:
                    while True:
                        data = s.recv(1024)
                        if data.endswith(b"<END>"):
                            f.write(data[:-5])
                            break
                        f.write(data)
                print(f"File {file_name} received successfully.")

        except Exception as e:
            messagebox.showerror("Error", f"Connection error: {e}")
        finally:
            s.close()

    main_fr1 = Frame(main, width=300, height=200, bg='#d4a373')
    main_fr1.place(x=75, y=150)

    find_img = PhotoImage(file='Image/find.png')
    Label(main_fr1, image=find_img, bg='#d4a373').place(x=30, y=60)

    SenderID = Entry(main_fr1, width=30, bg='#ddb892')
    SenderID.place(x=30, y=100)

    rev_img = PhotoImage(file='Image/receive.png')
    Button(main_fr1, image=rev_img, bg='#d4a373', command=lambda: threading.Thread(target=receiver).start()).place(x=230, y=80)

    main.mainloop()

# Frame 1 - Heading
fr1 = Frame(root, width=700, height=100, bg="#f5ebe0")
fr1.place(x=0, y=0)
Label(fr1, text="FILE TRANSFER", font=('Acumin Variable Concept', 20, 'bold'), bg="#f5ebe0", fg='#d5bdaf', border=1).place(x=20, y=30)

sent_ico1 = PhotoImage(file='Image/profile.png')
Label(fr1, image=sent_ico1, bg="#f5ebe0").place(x=600, y=10)

# Frame 2 - Send Button
fr2 = Frame(root, width=300, height=100, bg="#d5bdaf")
fr2.place(x=200, y=150)
Button(fr2, text='SEND', width=13, height=1, font=('Acumin Variable Concept', 10, 'bold'), border=None, bg='#d6ccc2', command=send_frame).place(x=33, y=37)

sent_ico2 = PhotoImage(file='Image/send.png')
Label(fr2, image=sent_ico2, bg="#d5bdaf").place(x=200, y=36)

# Frame 3 - Receive Button
fr3 = Frame(root, width=300, height=100, bg="#d5bdaf")
fr3.place(x=200, y=280)
Button(fr3, text='RECEIVE', width=13, height=1, font=('Acumin Variable Concept', 10, 'bold'), border=None, bg='#d6ccc2', command=receive_frame).place(x=33, y=37)

sent_ico3 = PhotoImage(file='Image/receive.png')
Label(fr3, image=sent_ico3, bg="#d5bdaf").place(x=200, y=36)

# Loop frame
root.mainloop()
