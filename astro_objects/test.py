import requests
import os
from datetime import datetime, timedelta

API_KEY = 'JWcqRdCtwC4bwZs7e7rx5Ah0plI91yBQ0I3Rl2kj'

def download_image(url, save_path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)

def get_apod_images(save_dir, start_date, end_date):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')
        url = f'https://api.nasa.gov/planetary/apod?api_key={API_KEY}&date={date_str}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'url' in data and 'title' in data:
                image_url = data['url']
                image_title = data['title'].replace(' ', '_').replace(':', '')
                save_path = os.path.join(save_dir, f'{image_title}_{date_str}.jpg')
                download_image(image_url, save_path)
                print(f'Загружено изображение за {date_str}: {image_title}')
        current_date += timedelta(days=1)

if __name__ == '__main__':
    save_dir = 'nasa_images'
    end_date = datetime.today()
    start_date = end_date - timedelta(days=3 * 365)  # Приблизительно 3 года
    get_apod_images(save_dir, start_date, end_date)
    print("Загрузка завершена")