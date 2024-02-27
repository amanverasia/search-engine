import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request

app = Flask(__name__)

class WebCrawler:
    def __init__(self, seed_url, max_depth=1):
        self.seed_url = seed_url
        self.max_depth = max_depth
        self.visited_urls = set()
        self.links_to_crawl = set()
        self.crawled_links = set()

    def crawl(self, url, depth=0):
        if depth > self.max_depth or url in self.visited_urls:
            return

        try:
            response = requests.get(url)
            if response.status_code == 200:
                self.visited_urls.add(url)
                links = self.extract_links(response.text)
                self.links_to_crawl.update(links)
                
                for link in links:
                    absolute_url = self.make_absolute_url(url, link)
                    self.crawl(absolute_url, depth + 1)
        except Exception as e:
            print(f"Error crawling {url}: {e}")

    def extract_links(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        links = [a['href'] for a in soup.find_all('a', href=True)]
        return links

    def make_absolute_url(self, base_url, relative_url):
        return requests.compat.urljoin(base_url, relative_url)

    def start_crawling(self):
        self.crawl(self.seed_url)

        # Continue crawling until all links are processed
        while self.links_to_crawl:
            url = self.links_to_crawl.pop()
            if url not in self.crawled_links:
                self.crawl(url)
                self.crawled_links.add(url)

crawler = WebCrawler(seed_url='https://facebook.com')
crawler.start_crawling()

# En un escenario del mundo real, guardaría los datos cortados, lo indexaría e implementaría un algoritmo de clasificación.

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    # Implement search logic using the crawled data
    # For simplicity, let's just return the query as the result
    return render_template('search_results.html', query=query)

if __name__ == '__main__':
    app.run(debug=True)
