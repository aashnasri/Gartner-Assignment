import requests
from typing import List, Union, Any, Dict, Optional

def download_and_load_book(url: str, 
                           output_folder : str = '_temp/book.txt') -> str:
    '''
    Downloads a book from a given URL and saves it to a specified output folder.
    '''
    response = requests.get(url)

    with open(output_folder, 'w', encoding='utf-8') as file:
        file.write(response.text)

    with open(output_folder, 'r', encoding='utf-8') as file:
        book_content = file.read()

    return book_content

# Example usage
# book_content = download_and_load_book(
#     'https://www.gutenberg.org/cache/epub/1342/pg1342.txt', '_temp/book.txt'
# )
# print(book_content)
