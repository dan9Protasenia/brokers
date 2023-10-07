import tkinter as tk

from client.send.send import ChatClient as SendClient
from server.receive.receive import ChatClient as ReceiveClient

if __name__ == "__main__":
    root = tk.Tk()

    send_client = SendClient(root)
    receive_client = ReceiveClient(root)

    root.mainloop()
