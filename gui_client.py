import socket
import threading
import queue
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox


class ChatGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Client - Broadcast + Private")
        self.root.geometry("750x500")

        self.sock = None
        self.running = False
        self.recv_thread = None
        self.msg_queue = queue.Queue()

        conn_frame = tk.Frame(root)
        conn_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(conn_frame, text="Server IP:").grid(row=0, column=0, sticky="w")
        self.ip_entry = tk.Entry(conn_frame, width=15)
        self.ip_entry.grid(row=0, column=1, padx=5)
        self.ip_entry.insert(0, "127.0.0.1")

        tk.Label(conn_frame, text="Port:").grid(row=0, column=2, sticky="w")
        self.port_entry = tk.Entry(conn_frame, width=8)
        self.port_entry.grid(row=0, column=3, padx=5)
        self.port_entry.insert(0, "3000")

        tk.Label(conn_frame, text="Username:").grid(row=1, column=0, sticky="w")
        self.username_entry = tk.Entry(conn_frame, width=15)
        self.username_entry.grid(row=1, column=1, padx=5)

        tk.Label(conn_frame, text="Status:").grid(row=0, column=4, padx=(10, 0))
        self.status_label = tk.Label(conn_frame, text="Disconnected", fg="red")
        self.status_label.grid(row=0, column=5, sticky="w")

        self.connect_btn = tk.Button(conn_frame, text="Connect", command=self.connect_server)
        self.connect_btn.grid(row=1, column=4, padx=5)

        self.disconnect_btn = tk.Button(conn_frame, text="Disconnect", state=tk.DISABLED, command=self.disconnect_server)
        self.disconnect_btn.grid(row=1, column=5, padx=5)

        # chat display 
        self.chat_box = ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED, height=20)
        self.chat_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # message input 
        bottom_frame = tk.Frame(root)
        bottom_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        tk.Label(bottom_frame, text="Private target:").grid(row=0, column=0, sticky="w")
        self.target_entry = tk.Entry(bottom_frame, width=15)
        self.target_entry.grid(row=0, column=1, padx=5)

        tk.Label(bottom_frame, text="Message:").grid(row=1, column=0, sticky="w")
        self.msg_entry = tk.Entry(bottom_frame)
        self.msg_entry.grid(row=1, column=1, columnspan=3, padx=5, sticky="we")
        self.msg_entry.bind("<Return>", self.send_broadcast)

        self.broadcast_btn = tk.Button(bottom_frame, text="Send Broadcast", command=self.send_broadcast)
        self.broadcast_btn.grid(row=1, column=4, padx=5)

        self.private_btn = tk.Button(bottom_frame, text="Send Private", command=self.send_private)
        self.private_btn.grid(row=1, column=5, padx=5)

        bottom_frame.columnconfigure(3, weight=1)

        self.root.after(100, self.check_queue)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    # connect to server
    def connect_server(self):
        if self.running is True:
            return

        ip = self.ip_entry.get().strip()
        port_text = self.port_entry.get().strip()
        username = self.username_entry.get().strip()

        if ip == "" or port_text == "" or username == "":
            messagebox.showwarning("Error", "Please enter IP, port, and username.")
            return

        try:
            port = int(port_text)
        except:
            messagebox.showwarning("Error", "Port must be a number.")
            return

        # try connecting
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port))
            s.send(username.encode())
        except Exception:
            messagebox.showerror("Connection Error", "Could not connect to server.")
            return

        self.sock = s
        self.running = True

        self.recv_thread = threading.Thread(target=self.receive_loop, daemon=True)
        self.recv_thread.start()

        self.set_status("Connected", "green")
        self.append_chat("[Connected to server]")

        self.ip_entry.config(state=tk.DISABLED)
        self.port_entry.config(state=tk.DISABLED)
        self.username_entry.config(state=tk.DISABLED)
        self.connect_btn.config(state=tk.DISABLED)
        self.disconnect_btn.config(state=tk.NORMAL)

    # disconnect from server
    def disconnect_server(self):
        self.running = False

        if self.sock is not None:
            try:
                self.sock.close()
            except:
                pass
            self.sock = None

        self.set_status("Disconnected", "red")
        self.append_chat("[Disconnected]")

        self.ip_entry.config(state=tk.NORMAL)
        self.port_entry.config(state=tk.NORMAL)
        self.username_entry.config(state=tk.NORMAL)
        self.connect_btn.config(state=tk.NORMAL)
        self.disconnect_btn.config(state=tk.DISABLED)

    def receive_loop(self):
        while self.running is True:
            try:
                data = self.sock.recv(1024)
            except:
                break

            if not data:
                break

            msg = data.decode()
            self.msg_queue.put(msg)

        self.msg_queue.put("__DISCONNECT__")
        self.running = False

    # broadcast message
    def send_broadcast(self, event=None):
        if self.running is False:
            messagebox.showwarning("Error", "Not connected.")
            return

        msg = self.msg_entry.get().strip()
        if msg == "":
            return

        # quit client
        if msg.lower() == "quit":
            self.disconnect_server()
            return

        try:
            self.sock.send(msg.encode())
        except:
            messagebox.showerror("Error", "Could not send message.")
            self.disconnect_server()
            return

        self.append_chat("You (broadcast): " + msg)
        self.msg_entry.delete(0, tk.END)

    # private message
    def send_private(self):
        if self.running is False:
            messagebox.showwarning("Error", "Not connected.")
            return

        target = self.target_entry.get().strip()
        msg = self.msg_entry.get().strip()

        if target == "":
            messagebox.showwarning("Error", "Enter target username.")
            return
        if msg == "":
            return

        full_msg = "@" + target + " " + msg

        try:
            self.sock.send(full_msg.encode())
        except:
            messagebox.showerror("Error", "Could not send message.")
            self.disconnect_server()
            return

        self.append_chat("You -> " + target + ": " + msg)
        self.msg_entry.delete(0, tk.END)


    def set_status(self, text, color):
        self.status_label.config(text=text, fg=color)

    # append to chat
    def append_chat(self, text):
        self.chat_box.config(state=tk.NORMAL)
        self.chat_box.insert(tk.END, text + "\n")
        self.chat_box.yview(tk.END)
        self.chat_box.config(state=tk.DISABLED)

    # incoming message queue
    def check_queue(self):
        while not self.msg_queue.empty():
            msg = self.msg_queue.get()
            if msg == "__DISCONNECT__":
                self.disconnect_server()
            else:
                self.append_chat(msg)

        self.root.after(100, self.check_queue)

    # close window
    def on_close(self):
        self.disconnect_server()
        self.root.destroy()


def main():
    root = tk.Tk()
    gui = ChatGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
