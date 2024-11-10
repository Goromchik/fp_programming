import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image
import multiprocessing as mp
import os
import tkinter as tk
from tkinter import messagebox, filedialog, Text

file_path = ""
processed_images_count = 0 #счётчик обработанных изображений

def analysing(image, number, queue):
    image_with_objects = image.copy()
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    image = cv2.filter2D(image, -1, kernel)

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
    _, binary_image = cv2.threshold(blurred_image, 200, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    space_objects = []

    font = ImageFont.truetype("font/arial.ttf", 14)

    for contour in contours:
        area = cv2.contourArea(contour)
        x, y, width, height = cv2.boundingRect(contour)
        center_x = x + width / 2
        center_y = y + height / 2
        brightness = np.sum(gray_image[y:y + height, x:x + width])
        object_type = classified(area, brightness)
        space_object = {
            "x": center_x,
            "y": center_y,
            "brightness": brightness,
            "type": object_type,
            "size": width * height
        }
        space_objects.append(space_object)
        cv2.rectangle(image_with_objects, (x, y), (x + width, y + height), (0, 255, 0), 2)
        (text_width, text_height) = cv2.getTextSize(object_type, cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, thickness=1)[0]
        cv2.rectangle(image_with_objects, (x, y - text_height - 5), (x + text_width // 2, y - 5), (0, 255, 0), cv2.FILLED)
        pil_image = Image.fromarray(image_with_objects)
        draw = ImageDraw.Draw(pil_image)
        draw.text((x, y - text_height - 10), object_type, font=font, fill=(0, 0, 0))
        image_with_objects = np.array(pil_image)

    queue.put((image_with_objects, number - 1, space_objects))
    return

def classified(area, brightness): #площадь и яркость
    return {
        area < 10 and brightness > 100: "звезда",
        area < 10 and brightness > 50: "комета",
        area < 10 and brightness > 0: "планета",
        area > 10000 and brightness > 1000000: "галактика",
        area < 10000 and brightness > 1000000: "квазар",
        area >= 10 and brightness > 0: "звезда"
    }[True]

#делим изображение на части для параллельной обработки
def split_image(image, num_parts):
    height, width, _ = image.shape
    part_width = (width // num_parts) + 1
    part_height = (height // num_parts) + 1
    parts = []
    for chunk_width in range(num_parts):
        for chunk_height in range(num_parts):
            part = image[chunk_height * part_height:min((chunk_height + 1) * part_height, len(image))]
            part = part[:, chunk_width * part_width:(chunk_width + 1) * part_width, :]
            parts.append(part)
    return parts

def parallel_processing(full_path_to_image, text_widget, processed_images_count):
    image = cv2.imread(full_path_to_image)
    if image is None:
        print(f"Не удалось прочитать изображение: {full_path_to_image}")
        return processed_images_count

    queue = mp.Queue()
    num_parts = 4
    mp_parts = split_image(image, num_parts)
    Processes = []
    number = 0
    for mp_part in mp_parts:
        number += 1
        Process = mp.Process(target=analysing, args=(mp_part, number, queue))
        Process.start()
        Processes.append(Process)
    sum_finish = 0
    image_parts = [0] * len(mp_parts)
    all_objects = []
    while sum_finish != len(Processes):
        if not queue.empty():
            sum_finish += 1
            image_part, part_index, space_objects = queue.get()
            image_parts[part_index] = image_part.copy()
            all_objects.extend(space_objects)
            text_widget.insert(tk.END, f"Выполнен процесс №{part_index + 1}\n")
    image_vstack = [image_parts[i] for i in range(0, num_parts ** 2, num_parts)]
    k = 0
    for i in range(num_parts):
        for j in range(1, num_parts):
            image_vstack[i] = np.vstack([image_vstack[i], image_parts[j + k]])
        k += num_parts
    image_with_objects = np.hstack(image_vstack)
    output_directory = "image_result"
    os.makedirs(output_directory, exist_ok=True)
    output2_directory = "image_crop"
    os.makedirs(output2_directory, exist_ok=True)
    image_name = os.path.basename(full_path_to_image)
    cv2.imwrite(f"{output2_directory}/{image_name}", image_with_objects)
    with open(f"{output_directory}/{image_name}.txt", "w", encoding="utf-8") as file:
        for object in all_objects:
            file.write(f"Координаты: ({object['x']}, {object['y']}); Яркость: {object['brightness']}; Размер: {object['size']}; Тип: {object['type']}\n")
    text_widget.insert(tk.END, f"Результат сохранен для изображения: {image_name}\n")
    print(f"Результат сохранен для изображения: {image_name}")
    return processed_images_count + 1

#обработка изображений из файла
def process_all_images_in_folder(folder_path, text_widget):
    global processed_images_count
    for image_name in os.listdir(folder_path):
        image_path = os.path.join(folder_path, image_name)
        if image_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            processed_images_count = parallel_processing(image_path, text_widget, processed_images_count)
            text_widget.insert(tk.END, f"Обработано изображений: {processed_images_count}\n")
    messagebox.showinfo("Готово", "Анализ завершен")

def select_folder(text_widget):
    global file_path
    file_path = filedialog.askdirectory()
    messagebox.showinfo("Готово", "Папка успешно выбрана")

def start_analysis(text_widget):
    if file_path:
        process_all_images_in_folder(file_path, text_widget)
    else:
        messagebox.showerror("Ошибка", "Сначала выберите папку")

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Параллельная обработка космических изображений")
    root.geometry("600x400")

    lbl = tk.Label(root, text="Добро пожаловать! Перед началом работы, ознакомьтесь с инструкцией:", font=("Arial", 10))
    lbl.pack(pady=(10, 0))
    lbl = tk.Label(root, text="1. Выберите папку с космическими изображениями.")
    lbl.pack()
    lbl = tk.Label(root, text="2. Нажмите на кнопку 'Провести анализ'.")
    lbl.pack()
    lbl = tk.Label(root, text="3. После завершения всех процессов результат будет доступен в папке 'image_result'.")
    lbl.pack()

    text_widget = Text(root, wrap=tk.WORD, width=70, height=10)
    text_widget.pack(pady=(20, 0))

    choose = tk.Button(root, text="Выбрать папку", width=30, bg="#DDDDDD", command=lambda: select_folder(text_widget))
    choose.pack(pady=(20, 10))

    start = tk.Button(root, text="Провести анализ", width=30, bg="#DDDDDD", command=lambda: start_analysis(text_widget))
    start.pack()

    root.mainloop()