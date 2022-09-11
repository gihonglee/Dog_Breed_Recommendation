import requests
from bs4 import BeautifulSoup
from os.path  import basename

headers_list = [{"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'},
{"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'},
{"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'},
{"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'},
 {"User-Agent": 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1'},
 {"User-Agent" : 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36'}]
name_list = []

def name_extract(page):
    # page 1 ~ 24
    url = f'https://www.akc.org/dog-breeds/page/{page}/'
    r = requests.get(url, headers= headers_list[(page)%6])
    soup = BeautifulSoup(r.content, 'html.parser')
    divs = soup.find_all(class_ = "breed-type-card mla mra bpm-mx2 contents-filter")
    for div in divs:
        with open('img/' + str(basename(div['data-title']).replace(' ','-') + '.jpg'), "wb") as f: #div.img['data-src']
            f.write(requests.get(div.img['data-src']).content)
    
def main():
    for i in range(1,25): #1,24
        name_extract(i)

if __name__ == "__main__":
    main()
