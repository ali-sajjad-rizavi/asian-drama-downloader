import requests, json
from bs4 import BeautifulSoup
import re as RegExp

my_headers = {}
my_headers['user-agent'] = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'





class DramaScraper:
	def __init__(self, url):
		soup = BeautifulSoup(requests.get(url, headers=my_headers).text, 'html.parser')
		self.dataDict = {}
		self.dataDict['drama-title'] = RegExp.sub('[<>?":/|]', '', soup.title.text.replace('full episodes english sub at Dramanice', '').strip())
		self.dataDict['drama-url'] = url
		#---
		self.dataDict['episodes'] = []
		for anchor in soup.find('ul', {'class':'list_episode'}).find_all('a'):
			episodeDict = {}
			episodeDict['episode-title'] = RegExp.sub('[<>?":/|]', '', '{} - {}'.format(self.dataDict['drama-title'], ' '.join(anchor.text.split())))
			episodeDict['episode-url'] = anchor['href']
			self.dataDict['episodes'].append(episodeDict)

	def scrapeEpisodes(self, start=1, end=1):
		self.dataDict['scraped-episodes'] = []
		for episodeDict in self.dataDict['episodes'][start-1:end]:
			scraped_episodeDict = episodeDict
			soup = BeautifulSoup(requests.get(episodeDict['episode-url'], headers=my_headers).text, 'html.parser')
			serversList = soup.find('div', id='w-server').find_all('div') # arranged in ascending order
			print(len(serversList))
			input()
			scraped_episodeDict['embed-servers'] = {}
			for div in serversList:
				server_name = div['class'][1].lower()
				embed_url = div['data-server']
				scraped_episodeDict['embed-servers'][server_name] = embed_url
			#------
			self.dataDict['scraped-episodes'].append(scraped_episodeDict)
			print('- Collected:', scraped_episodeDict['episode-title'])

	def saveJSON(self, filename='drama.json'):
		open(filename, 'w', encoding='utf-8').write(json.dumps(self.dataDict, indent=4, sort_keys=True, ensure_ascii=False))

	# STATIC METHOD
	def searchDrama(query='drama name'):
		response_text = requests.get('https://dramanice.video/?s={}'.format(query.replace(' ', '+'))).text
		figure_results = BeautifulSoup(response_text, 'html.parser').find('ul', class_='list-thumb').find_all('figure', class_='post-thumbnail')[:4]
		paired_results = [(figure.find('a')['title'], figure.find('a')['href']) for figure in figure_results]
		return paired_results # (title, url) pair list is returned





######
###### Example: https://dramanice.video/the-song-of-glory/
######

def main():
	searchInput = input('- Enter Drama Name/URL: ')
	if 'dramanice' in searchInput:
		drama_scraper = DramaScraper(searchInput)
	else:
		print('\n\tResults:\n')
		search_results = DramaScraper.searchDrama(query=searchInput)
		[print(f'\t {i+1}) {search_results[i][0]}') for i in range(len(search_results))]
		selected_index = int(input('\n- Select your option: ')) - 1
		drama_scraper = DramaScraper(search_results[selected_index][1])
	print('-------------------')
	drama_scraper.scrapeEpisodes()
	drama_scraper.saveJSON()
	print('- JSON saved!')

if __name__ == '__main__':
	main()