from rich.console import Console

from lib.io import display_header, get_input, create_json_file, display_data, display_message
from lib.data import request_raw_data, processor

HEADERS = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0'}

API_URLS = {
    'posts': 'https://www.instagram.com/explore/tags/%s/?__a=1',
    'user_data': 'https://www.instagram.com/%s/?__a=1',
    'user_posts': 'https://www.instagram.com/%s/?__a=1',
    'search': 'https://www.instagram.com/web/search/topsearch/?query=%s'
}

def controller(console):
    input = get_input()

    with console.status('[bold green]Fetching Data...') as status:
        api_url = API_URLS[input['query_type']]%input['query']
        raw_data = request_raw_data(api_url, HEADERS)
        
        if len(raw_data) == 0:
            raise Exception("Requested returned no results")
        
        if 'post_type' in input:
            processed_data = processor[input['query_type']](raw_data, input['post_type'])
        else:
            processed_data = processor[input['query_type']](raw_data)

    if input['file_confirm']:
        file_name = create_json_file(input['query'], processed_data)
        display_message(f'\nFile created, File Name: [bold red]{file_name}')
    else:
        display_data(processed_data)
        display_message('\nDone! :thumbs_up:')

if __name__  == '__main__':
    console = Console()

    display_header()

    try:
        controller(console)
    except (KeyboardInterrupt, KeyError, SystemError):
        display_message("Bye :waving_hand:")
    except Exception as error:
        display_message(str(error), False)
