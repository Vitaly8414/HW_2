"""
Задание
Написать программу, которая скачивает изображения с заданных URL-адресов и сохраняет их на диск. 
Каждое изображение должно сохраняться в отдельном файле, название которого соответствует названию 
изображения в URL-адресе.
Например, URL-адрес: https://example/images/image1.jpg -> файл на диске: image1.jpg
— Программа должна использовать многопоточный, многопроцессорный и асинхронный подходы.
— Программа должна иметь возможность задавать список URL-адресов через аргументы командной строки.
— Программа должна выводить в консоль информацию о времени скачивания каждого 
изображения и общем времени выполнения программы.
"""
import requests
import multiprocessing
import time


def download_image(url, filename):
    start_time = time.time()
    response = requests.get(url)
    with open(filename, "wb") as f:
        f.write(response.content)
    print(f"Скачано изображение {filename} за {time.time() - start_time:.2f} секунд")


def main():
    urls = [
        "https://example/images/image1.jpg",
        "https://example/images/image2.jpg",
        "https://example/images/image3.jpg",
    ]

    processes = []
    for url in urls:
        filename = url.split("/")[-1]
        process = multiprocessing.Process(target=download_image, args=(url, filename))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    print(f"Общее время выполнения: {time.time() - start_time:.2f} секунд")


if __name__ == "__main__":
    main()