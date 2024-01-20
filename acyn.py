import requests
import asyncio


async def download_image(url, filename):
    start_time = time.time()
    response = await requests.get(url)
    with open(filename, "wb") as f:
        f.write(response.content)
    print(f"Скачано изображение {filename} за {time.time() - start_time:.2f} секунд")


async def main():
    urls = [
        "https://example/images/image1.jpg",
        "https://example/images/image2.jpg",
        "https://example/images/image3.jpg",
    ]

    tasks = [download_image(url, filename) for url, filename in zip(urls, urls.split("/")[-1])]
    await asyncio.wait(tasks)

    print(f"Общее время выполнения: {time.time() - start_time:.2f} секунд")


if __name__ == "__main__":
    asyncio.run(main())