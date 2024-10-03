# flibusta_downloader
This Python script allows users to search for books on the Flibusta website and download their PDF versions automatically. It leverages asynchronous programming with aiohttp and asyncio for efficient web scraping and file downloading. The script uses BeautifulSoup for parsing HTML and extracting book links.

* Asynchronous Downloads: The script fetches book pages and downloads PDFs concurrently, improving efficiency.
* Book Search: Users can input a book title, and the script will search for it on the Flibusta website.
* PDF Download: The script automatically finds and downloads available PDF versions of the books.
* User-Agent Handling: Custom user-agent header is included to mimic a browser request and avoid potential blocking by the website.
