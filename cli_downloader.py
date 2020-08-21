import os, glob

from dramanice import DramaScraper as DramaniceScraper
import download_link_builder




class Downloader:
	def __init__(self, drama_dictionary):
		if os.path.isfile('failed.txt'):
			os.remove('failed.txt')
		self.drama_dict = drama_dictionary

	def __downloadEpisode(self, filename='episode.mp4', download_link='download-url'):
		print("============================================================================")
		print(" DOWNLOADING EPISODE:", filename)
		print("============================================================================")
		options = f'-x 10 --max-tries=5 --retry-wait=10 --check-certificate=false -d downloaded -o "{filename}"'
		cmd = f'aria2c {download_link} {options}'
		#..........
		if os.path.isfile(f'downloaded/{filename}') and not os.path.isfile(f'downloaded/{episode_filename}.aria2'):
			return
		#-------------#if os.name == 'posix': subprocess.call(cmd.split())
		while True:
			try:
				os.system(cmd)
				break
			except KeyboardInterrupt: input("\nDownloader is paused. PRESS [ENTER] TO CONTINUE...")
		#-------------
		if os.path.isfile("downloaded/" + filename + ".aria2"):
			open('failed.txt', 'a').write(cmd + '\n')

	def downloadDrama(self):
		for episodeDict in self.drama_dict['scraped-episodes']:
			download_link = download_link_builder.get_available_download_link(episodeDict)
			if download_link == 'unavailable':
				continue
			self.__downloadEpisode(filename=episodeDict['episode-title']+'.mp4', download_link=download_link)
		self.__retryFailedDownloads()

	def __retryFailedDownloads(self):
		if not os.path.isfile('failed.txt'):
			return
		print('-------------------------------------')
		print('- Retrying failed downloads')
		print('-------------------------------------')
		commands = open('failed.txt', 'r').read().strip().split('\n')
		for command in commands:
			while True:
				try:
					os.system(command)
					break
				except KeyboardInterrupt: input('\nDownloader is paused. PRESS [ENTER] TO CONTINUE...')

	def __del__(self):
		if len(glob.glob('downloaded/*.aria2')) != 0:
			return
		if os.path.isdir('downloaded'):
			os.rename('downloaded', self.drama_dict['drama-title'])
		#---
		if os.path.isfile('failed.txt'):
			os.remove('failed.txt')



###----------------###
#### MAIN ROUTINE #### Example: https://dramanice.video/the-song-of-glory/
###----------------###

def main():
    print("\t\t|======================|")
    print("\t\t| CLI DRAMA DOWNLOADER |")
    print("\t\t|======================|\n")
    #
    searchInput = input('- Enter Drama Name/URL: ')
    if 'dramanice' in searchInput:
    	drama_scraper = DramaniceScraper(searchInput)
    else:
    	print('\n\tResults:\n')
    	search_results = DramaniceScraper.searchDrama(query=searchInput)
    	[print(f'\t {i+1}) {search_results[i][0]}') for i in range(len(search_results))]
    	selected_index = int(input('\n- Select your option: ')) - 1
    	drama_scraper = DramaniceScraper(search_results[selected_index][1])
    #
    print("\t -FOUND:", drama_scraper.episode_count, " Episodes in TOTAL!\n")
    #-----
    start_ep = int(input("\t - Start From Episode: "))
    end_ep = int(input("\t - End At Episode: "))
    print('----------------------------------------------------------------------------------')
    print(f'- Scraping episode video links from {start_ep} to {end_ep}, wait for a while...')
    drama_scraper.scrapeEpisodes(start=start_ep, end=end_ep)
    #
    print("\nStarting Download using aria2...\n")
    downloader = Downloader(drama_scraper.dataDict)
    downloader.downloadDrama()
    print("=======================================================")
    print("-------------------- COMPLETED !!! --------------------")
    print("=======================================================")
    #
    print("Done!")
    input('- Press [ENTER] to quit...')

if __name__ == '__main__':
	main()