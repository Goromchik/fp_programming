import asyncio
import threading
import tkinter as tk
from tkinter import scrolledtext

# Получение сообщений от сервера
async def receive_messages(reader, text_widget):
    while True:
        data = await reader.read(100)
        message = data.decode()
        text_widget.insert(tk.END, f"{message}\n")
        text_widget.see(tk.END)
        print(f"Получено сообщение: {message}")

# Отправка сообщений на сервер
async def send_messages(writer):
    while True:
        message = await get_input("")
        writer.write(message.encode())
        await writer.drain()

# Получение ввода от пользователя
async def get_input(prompt):
    loop = asyncio.get_event_loop()
    user_input = await loop.run_in_executor(None, input, prompt)
    return user_input

# Обработка нажатия кнопки "Отправить"
def on_send_button_click():
    global writer

    message = entry_widget.get()
    entry_widget.delete(0, tk.END)
    writer.write(message.encode())

# Основная функция клиента
async def main(text_widget):
    global reader
    global writer

    reader, writer = await asyncio.open_connection('127.0.0.1', 8888)
    print("Подключено к серверу")

    receive_task = asyncio.create_task(receive_messages(reader, text_widget))
    send_task = asyncio.create_task(send_messages(writer))

    await receive_task
    await send_task

# Запуск асинхронного цикла в отдельном потоке
def start_async_loop(text_widget):
    asyncio.run(main(text_widget))

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("600x400")
    root.title("Client")

    text_widget = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=20, width=50)
    text_widget.pack(padx=10, pady=10)

    entry_widget = tk.Entry(root, width=50)
    entry_widget.pack(padx=(110, 0), pady=10, side=tk.LEFT)

    send_button = tk.Button(root, text="Отправить", command=on_send_button_click)
    send_button.pack(padx=10, pady=10, side=tk.LEFT)

    asyncio_thread = threading.Thread(target=start_async_loop, args=(text_widget,))
    asyncio_thread.start()

    root.mainloop()

"""Создайте новую комнату:

Введите команду: /create newroom

Присоединитесь к новой комнате:

Введите команду: /join newroom

Посмотрите список комнат:

Введите команду: /listrooms

Посмотрите текущую комнату:

Введите команду: /currentchat

Покиньте текущую комнату:

Введите команду: /leave"""