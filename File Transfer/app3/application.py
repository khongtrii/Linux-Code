import threading
from tkinter import *
from tkinter import filedialog
import tkinter as tk
import os
import socket
import time
import tqdm

class open_conn():
    def __init__(self, SERVER_HOST:str='0.0.0.0', SERVER_PORT:int=5001, BUFFER_SIZE:int=64*1024, SEPARATOR:str="<SEPARATOR>"):
        self.SERVER_HOST = SERVER_HOST
        self.SERVER_PORT = SERVER_PORT
        self.BUFFER_SIZE = BUFFER_SIZE
        self.SEPARATOR = SEPARATOR
        
    def open(self):
        try:
            s = socket.socket()
            s.bind((self.SERVER_HOST, self.SERVER_PORT))
            s.listen(5)
            print(f"[*] Listening as {self.SERVER_HOST}:{self.SERVER_PORT}")

            s.settimeout(15)  # Đặt thời gian chờ là 30 giây

            try:
                # Nếu không có kết nối trong 30 giây, sẽ phát sinh exception
                client_socket, address = s.accept()
                print(f"[+] {address} is connected.")
            except socket.timeout:
                print("[!] No connection received within 30 seconds.")
                conn_label.configure(text=f"We don't have any connection now !!!")
                s.close()
                btn_send.config(state=tk.NORMAL)
                btn_open.config(state=tk.NORMAL)
                return

            received = client_socket.recv(self.BUFFER_SIZE).decode()
            filename, filesize = received.split(self.SEPARATOR)

            try:
                filesize = int(filesize)
            except ValueError:
                print("[!] Error: Filesize is not a valid integer.")
                client_socket.close()
                s.close()
                btn_send.config(state=tk.NORMAL)
                btn_open.config(state=tk.NORMAL)
                conn_label.configure(text=f"Error occurred!")
                time.sleep(2)
                conn_label.configure(text=f"We don't have any connection now !!!")
                return

            TARGET_DIR = "received_files"

            os.makedirs(TARGET_DIR, exist_ok=True)

            filename = os.path.basename(filename)

            filepath = os.path.join(TARGET_DIR, filename)

            progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
            with open(filepath, "wb") as f:
                while True:
                    bytes_read = client_socket.recv(self.BUFFER_SIZE)
                    if not bytes_read:
                        break
                    f.write(bytes_read)
                    progress.update(len(bytes_read))

            btn_open.config(state=tk.NORMAL)
            btn_send.config(state=tk.NORMAL)
            
            client_socket.close()
            s.close()
            conn_label.configure(text=f"File received successfully!")
            time.sleep(2)
            conn_label.configure(text=f"We don't have any connection now !!!")
        except Exception as e:
            print(f"Error: {str(e)}")
            client_socket.close()
            s.close()
            btn_open.config(state=tk.NORMAL)
            btn_send.config(state=tk.NORMAL)
            conn_label.configure(text=f"Error occurred!")

class send_method():
    def __init__(self, SEPARATOR:str='<SEPARATOR>', BUFFER_SIZE:int=64*1024):
        self.SEPARATOR = SEPARATOR
        self.BUFFER_SIZE = BUFFER_SIZE

    def send_file(self, filename, host, port):
        filesize = os.path.getsize(filename)
        s = socket.socket()
        btn_open.config(state=tk.DISABLED)
        btn_send.config(state=tk.DISABLED)
        print(f"[+] Connecting to {host}:{port}")
        s.connect((host, port))
        print("[+] Connected.")

        s.send(f"{filename}{self.SEPARATOR}{filesize}".encode())

        progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(filename, "rb") as f:
            while True:
                bytes_read = f.read(self.BUFFER_SIZE)
                if not bytes_read:
                    break
                s.sendall(bytes_read)
                progress.update(len(bytes_read))

        s.close()
        btn_open.config(state=tk.NORMAL)
        btn_send.config(state=tk.NORMAL)


def show_host():
    host = socket.gethostbyname(socket.gethostname())
    return host

host = show_host()

SERVER_HOST:str='0.0.0.0'
SERVER_PORT:int=5001
BUFFER_SIZE:int=64*1024
SEPARATOR:str="<SEPARATOR>"

def open_connection():
    conn = open_conn(SERVER_HOST, SERVER_PORT, BUFFER_SIZE, SEPARATOR)
    conn.open()

def open_connection_id():
    try:
        threading.Thread(target=open_connection, daemon=True).start()
        conn_label.configure(text=f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
        btn_open.config(state=tk.DISABLED)
        btn_send.config(state=tk.DISABLED)
        
    except:
        btn_open.config(state=tk.NORMAL)
        btn_send.config(state=tk.NORMAL)
    
def select_file():
    global filename
    filename = filedialog.askopenfilename(
        initialdir=os.getcwd(),
        title='Select File',
        filetypes=(('All files', '*.*'),)
    )
    entry2.delete(0, tk.END)
    entry2.insert(0, filename)

def send_our_file():
    send = send_method()
    rev_host = entry1.get()
    send_port = SERVER_PORT
    print(filename, rev_host, send_port)
    try:
        send.send_file(filename, rev_host, send_port)
        conn_label.configure(text=f"File sent successfully!")
        time.sleep(2)
        conn_label.configure(text=f"We don't have any connection now !!!")
    except:
        conn_label.configure(text=f"Error occurred!")
        time.sleep(2)
        btn_open.config(state=tk.NORMAL)
        btn_send.config(state=tk.NORMAL)
        conn_label.configure(text=f"We don't have any connection now !!!")

def send_our_file_tr():
    try:
        # Chạy việc gửi file trong một luồng riêng
        threading.Thread(target=send_our_file, daemon=True).start()

    except Exception as e:
        conn_label.configure(text=f"Error: {str(e)}")


root = Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

window_width = 920
window_height = 380
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

root.title('Transfer File Application')

root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
root.resizable(False, False)
root.configure(bg='#bc6c25')

frame = Frame(root, bg='#606c38', width=720, height=300)
frame.place(relx=0.1, rely=0.1)

Label(frame, text=f"My ID: {host}", font=("Arial", 12, "bold"), bg='#606c38', fg='#fefae0').place(relx=0.06, rely=0.06)

Label(frame, text='Host:', font=("Arial", 12), bg='#606c38', fg='#fefae0').place(relx=0.06, rely=0.17)
entry1 = Entry(frame, width=30, bg='#283618', fg='#fefae0')
entry1.place(relx=0.06, rely=0.25)

Label(frame, text='File:', font=("Arial", 12), bg='#606c38', fg='#fefae0').place(relx=0.06, rely=0.35)
entry2 = Entry(frame, width=30, bg='#283618', fg='#fefae0')
entry2.place(relx=0.06, rely=0.43)


Button(frame, text='Choose file', bg='#606c38', fg='#fefae0', command=select_file).place(relx=0.35, rely=0.41)
btn_send = Button(frame, text='Send file', bg='#606c38', fg='#fefae0',width=8, command=send_our_file_tr)
btn_send.place(relx=0.35, rely=0.52)



frame1 = Frame(frame, bg='#dda15e', width=330, height=260)
frame1.place(relx=0.5, rely=0.06)

btn_open = Button(frame1, text='Open', font=('Arial'), width=5, bg='#606c38', fg='#fefae0', command=open_connection_id)
btn_open.place(relx=0.8, rely=0.05)

conn_label = Label(frame1, text="We don't have any connection now !!!", font=('Arial', 10), bg='#dda15e', fg='black')
conn_label.place(relx=.05, rely=.05)


root.mainloop()