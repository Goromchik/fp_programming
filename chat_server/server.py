import asyncio
import tkinter as tk
from tkinter import scrolledtext
import threading

# Словарь для хранения подключенных клиентов
connected_clients = {}
# Словарь для хранения комнат чата
chat_rooms = {'main': set()}

# Функция для обновления виджета с сообщениями
def update_widget(widget, text):
    widget.insert(tk.END, text + "\n")
    widget.see(tk.END)

# Обработка подключения клиента
async def handle_client_connection(reader, writer, client_list_widget, log_widget):
    client_address = writer.get_extra_info('peername')
    update_widget(log_widget, f"Подключение от: {client_address}")

    writer.write("Введите ваше имя в поле ниже: ".encode())
    await writer.drain()

    client_name = (await reader.read(100)).decode().strip()
    connected_clients[writer] = client_name
    update_widget(client_list_widget, f"{client_name} ({client_address})")

    writer.write("Введите команду для управления комнатами (например, /join (название комнаты)): ".encode())
    await writer.drain()

    room_name = 'main'
    chat_rooms[room_name].add(writer)

    try:
        while True:
            message = await reader.read(100)
            if not message:
                break
            decoded_message = message.decode().strip()
            update_widget(log_widget, f"{client_name}@{room_name}: {decoded_message}")

            if decoded_message.startswith('/join'):
                room_name = decoded_message.split()[1]
                await join_room(writer, room_name, log_widget)
            elif decoded_message.startswith('/create'):
                room_name = decoded_message.split()[1]
                await create_room(writer, room_name, log_widget)
            elif decoded_message.startswith('/leave'):
                await leave_room(writer, log_widget)
            elif decoded_message.startswith('/listrooms'):
                await list_rooms(writer)
            elif decoded_message.startswith('/currentchat'):
                await show_current_chat(writer)
            else:
                await broadcast_message(writer, f"{client_name}: {decoded_message}", room_name)

    except Exception as e:
        update_widget(log_widget, f"Ошибка: {e}")
    finally:
        connected_clients.pop(writer, None)
        await leave_room(writer, log_widget)
        writer.close()
        await writer.wait_closed()
        update_widget(log_widget, f"Отключение: {client_address}")

# Присоединение к комнате
async def join_room(writer, room_name, log_widget):
    await leave_room(writer, log_widget)
    if room_name not in chat_rooms:
        chat_rooms[room_name] = set()
    chat_rooms[room_name].add(writer)
    writer.write(f"Вы присоединились к комнате: {room_name}\n".encode())
    await writer.drain()
    update_widget(log_widget, f"{connected_clients[writer]} присоединился к комнате: {room_name}")

# Создание новой комнаты
async def create_room(writer, room_name, log_widget):
    if room_name not in chat_rooms:
        chat_rooms[room_name] = set()
    await join_room(writer, room_name, log_widget)

# Покидание текущей комнаты
async def leave_room(writer, log_widget):
    for room_name, room_clients in chat_rooms.items():
        if writer in room_clients:
            room_clients.remove(writer)
            if not room_clients:
                del chat_rooms[room_name]
            writer.write(f"Вы покинули комнату: {room_name}\n".encode())
            await writer.drain()
            update_widget(log_widget, f"{connected_clients[writer]} покинул комнату: {room_name}")
            break

# Получение списка доступных комнат
async def list_rooms(writer):
    rooms_list = "Доступные комнаты: " + ", ".join(chat_rooms.keys())
    writer.write(rooms_list.encode())
    await writer.drain()

# Получение текущей комнаты
async def show_current_chat(writer):
    for room_name, room_clients in chat_rooms.items():
        if writer in room_clients:
            writer.write(f"Вы находитесь в комнате: {room_name}\n".encode())
            await writer.drain()
            break

# Отправка сообщения всем клиентам в текущей комнате
async def broadcast_message(writer, message, room_name):
    if room_name in chat_rooms:
        for client_writer in chat_rooms[room_name]:
            if client_writer != writer:
                client_writer.write(message.encode())
                await client_writer.drain()

# Запуск сервера
async def start_server(client_list_widget, log_widget):
    server = await asyncio.start_server(
        lambda r, w: handle_client_connection(r, w, client_list_widget, log_widget),
        '127.0.0.1', 8888
    )
    async with server:
        await server.serve_forever()

# Запуск сервера в отдельном потоке
def start_server_thread(client_list_widget, log_widget):
    asyncio.run(start_server(client_list_widget, log_widget))

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Сервер чата")

    client_list_widget = scrolledtext.ScrolledText(root, width=30, height=15)
    client_list_widget.pack(side=tk.LEFT, padx=10, pady=10)

    log_widget = scrolledtext.ScrolledText(root, width=50, height=15)
    log_widget.pack(side=tk.LEFT, padx=10, pady=10)

    threading.Thread(target=start_server_thread, args=(client_list_widget, log_widget), daemon=True).start()

    root.mainloop()