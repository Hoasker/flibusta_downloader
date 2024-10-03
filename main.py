import asyncio
import aiohttp
import aiofiles
from bs4 import BeautifulSoup
import re
from urllib.parse import quote


BASE_URL = "http://flibusta.site"
SEARCH_URL = f"{BASE_URL}/booksearch?ask="
BOOK_PATTERN = re.compile(r'/b/\d+')
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}


async def fetch(session: aiohttp.ClientSession, url: str) -> str:
    """
    Fetches the HTML content of a given URL.

    Args:
        session (aiohttp.ClientSession): The client session used for making requests.
        url (str): The URL to fetch.

    Returns:
        str: The HTML content of the fetched page.
    """
    async with session.get(url, headers=HEADERS) as response:
        return await response.text()


async def download_file(session: aiohttp.ClientSession, url: str, filename: str) -> None:
    """
    Downloads a file from a given URL and saves it to the specified filename.

    Args:
        session (aiohttp.ClientSession): The client session used for making requests.
        url (str): The URL to download the file from.
        filename (str): The filename to save the downloaded file as.
    """
    async with session.get(url, headers=HEADERS) as response:
        if response.status == 200:
            async with aiofiles.open(filename, mode='wb') as f:
                await f.write(await response.read())
            print(f"Successfully downloaded book: {filename}")
        else:
            print(f"Failed to download book: {filename}. Status: {response.status}")


async def search_and_download(book_name: str) -> None:
    """
    Searches for books by name and downloads their PDF versions if available.

    Args:
        book_name (str): The name of the book to search for.
    """
    async with aiohttp.ClientSession() as session:
        search_query = quote(book_name)
        url = f"{SEARCH_URL}{search_query}"
        html = await fetch(session, url)
        soup = BeautifulSoup(html, 'lxml')

        # Find all book links on the search page
        book_links = soup.find_all('a', href=BOOK_PATTERN)
        if not book_links:
            print("No books found.")
            return

        # Process each book and try to find the PDF download link
        tasks = []
        for a in book_links:
            book_title = a.get_text(strip=True)
            book_url = f"{BASE_URL}{a['href']}"

            # Get the book page and search for PDF link
            book_page = await fetch(session, book_url)
            book_soup = BeautifulSoup(book_page, 'html.parser')

            pdf_link = book_soup.find('a', string=re.compile("скачать pdf", re.I))
            if pdf_link:
                pdf_url = f"{BASE_URL}{pdf_link['href']}"
                filename = f"{book_title}.pdf"
                tasks.append(download_file(session, pdf_url, filename))

        # Execute the download tasks for all found books
        if tasks:
            await asyncio.gather(*tasks)
        else:
            print("No books in PDF format found.")


async def main() -> None:
    """
    The main function that prompts the user for a book name and initiates the search and download process.
    """
    book_name = input("Enter the name of the book: ")
    await search_and_download(book_name)


if __name__ == '__main__':
    asyncio.run(main())
