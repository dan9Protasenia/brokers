import tkinter as tk
from datetime import datetime
from tkinter import scrolledtext

import pika


class ChatClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Client")

        self.chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD)
        self.chat_area.pack(fill=tk.BOTH, expand=True)

        self.message_entry = tk.Entry(root)
        self.message_entry.pack(fill=tk.X, padx=10, pady=10)
        self.message_entry.bind("<Return>", self.send_message)

        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='chat')

    def send_message(self, event):
        message = self.message_entry.get()
        if message:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            message_with_timestamp = f"{timestamp} You: {message}"
            self.channel.basic_publish(exchange='', routing_key='chat', body=message_with_timestamp)
            self.chat_area.insert(tk.END, f"{message_with_timestamp}\n")
            self.message_entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    client = ChatClient(root)
    root.mainloop()
