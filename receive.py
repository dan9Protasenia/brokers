import threading
import tkinter as tk
from tkinter import scrolledtext

import pika


class ChatClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Client")

        self.chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD)
        self.chat_area.pack(fill=tk.BOTH, expand=True)

        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='chat')

        self.receive_messages()

    def receive_messages(self):
        def callback(ch, method, properties, body):
            self.chat_area.insert(tk.END, f"{body.decode()}\n")
            self.chat_area.see(tk.END)

        self.channel.basic_consume(queue='chat', on_message_callback=callback, auto_ack=True)

        receive_thread = threading.Thread(target=self.channel.start_consuming)
        receive_thread.daemon = True
        receive_thread.start()


if __name__ == "__main__":
    root = tk.Tk()
    client = ChatClient(root)
    root.mainloop()
