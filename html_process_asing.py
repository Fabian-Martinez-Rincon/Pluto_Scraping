import aiohttp
import asyncio

async def fetch_and_save(url, headers, filename):
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            if response.status == 200:
                html_content = await response.text()
                with open(filename, "w", encoding="utf-8") as file:
                    file.write(html_content)
                print(f"Contenido guardado en {filename}")
            else:
                print(f"Error: {response.status}")

async def main():
    url = "https://pluto.tv/latam/on-demand/619043246d03190008131b89/6245c1e23ca9b400078727bc?lang=en"
    headers = {
        "User-Agent": "python-requests/2.32.3"
    }
    filename = "pluto_page.html"

    await fetch_and_save(url, headers, filename)

if __name__ == "__main__":
    asyncio.run(main())

