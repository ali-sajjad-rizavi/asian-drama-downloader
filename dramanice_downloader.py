import requests as REQ
from bs4 import BeautifulSoup as BS
import re as REGEX
import os as OS
import subprocess as SP
import sys

#--------------------

class FailedContainer:
	failedCommandsList = []
	def addFailedCommand(cmd):
		FailedContainer.failedCommandsList.append(cmd)
	def retryFailedDownloads():
		if len(FailedContainer.failedCommandsList) == 0:
			return
		print("\n\n\n There were", len(FailedContainer.failedCommandsList), "failed downloads which can be resumed...")
		print(" If they fail again, there might be a server issue with these links.")
		while True:
			choice = input(" Do you want to retry downloading these Episodes? (Y/N): ")
			if choice == 'y' or choice == 'Y':
				break
			if choice == 'n' or choice == 'N':
				return
		i = 1
		for cmd in FailedContainer.failedCommandsList:
			print("\n===========[ Retrying download #", i, "]\n")
			OS.system(cmd)
			i += 1

#--------------------

class Drama:
	def __init__(self, pageurl):
		soup = BS(REQ.get(pageurl).text, 'html.parser')
		anchors = soup.find('ul', {'class':'list_episode'}).find_all('a')
		self.__title = soup.title.text.replace('at Dramanice', '').strip()
		self.__eptotal = len(anchors)
		self.__episodeList = []
		for a in anchors:
			eptitle = ' '.join(a.text.split())
			epurl = a['href']
			self.__episodeList.insert(0, Episode(eptitle, epurl))

	def getTotalEpisodeCount(self):
		return self.__eptotal

	def collectEpisodes(self, epstart, epend):
		if epstart < 1 or epend > self.__eptotal:
			print('- [ERROR]: Invalid episode range!')
			sys.exit()
		self.__episodeList = self.__episodeList[epstart - 1: epend]
		for epis in self.__episodeList:
			epis.prepareMp4uploadEmbed()

	def downloadEpisodes(self):
		for epis in self.__episodeList:
			epis.download()

	def finalizeDrama(self):
		for epis in self.__episodeList:
			isEpisFile = OS.path.isfile(OS.path.join("downloaded", epis.getTitle().replace(' ', '_') + ".mp4"))
			isAriaFile = OS.path.isfile(OS.path.join("downloaded", epis.getTitle().replace(' ', '_') + ".mp4.aria2"))
			if not isEpisFile or isAriaFile: return
		OS.rename("downloaded", self.__title)

#--------------------

class Episode:
	def __init__(self, title, pageurl):
		self.__title = title.replace('|', '-')
		self.__pageurl = pageurl

	def getTitle(self):
		return self.__title

	def prepareMp4uploadEmbed(self):
		embedsouplist = BS(REQ.get(self.__pageurl).text, 'html.parser').find_all('div', {'class':'serverslist Mp4upload'})
		if len(embedsouplist) == 0:
			self.__mp4uploadEmbed = 'not_found'
		else:
			self.__mp4uploadEmbed = embedsouplist[0]['data-server']

	def get_Mp4UploadDownloadLink(self):
		scripts = BS(REQ.get(self.__mp4uploadEmbed).text, 'html.parser').find_all('script', type="text/javascript")
		evalText = [script.text for script in scripts if "navigator" in script.text][0]
		evalItems = evalText.split('|')
		del evalItems[:evalItems.index('navigator')+1]
		videoID = [a for a in evalItems if len(a)>30][0]
		#
		evalItems = evalText.split('|')
		w3strPossiblesList = [s for s in evalItems if REGEX.match('s\d+$', s) or REGEX.match('www\d+$', s)]
		w3str = "www"
		if len(w3strPossiblesList) != 0:
			w3str = max(w3strPossiblesList, key=len)
		#
		retstr = "https://" + w3str + ".mp4upload.com:" + evalItems[evalItems.index(videoID)+1] + "/d/" + videoID + "/video.mp4"
		print("Got:-", retstr)
		return retstr

	def download(self):
		if self.__mp4uploadEmbed is "not_found":
			print("\n", "::: COULD NOT FIND ::: EPISODE:-", self.__title, "| Server=MP4-UPLOAD\n")
			return
		print("============================================================================")
		print(" DOWNLOADING EPISODE:", self.__title.replace(' ', '_'))
		print("============================================================================")
		options = " -x 10 --max-tries=5 --retry-wait=10 --check-certificate=false -d downloaded -o "
		episode_filename = self.__title.replace(' ', '_') + ".mp4"
		cmd = "aria2c " + self.get_Mp4UploadDownloadLink() + options + episode_filename
		if OS.path.isfile(OS.path.join("downloaded", episode_filename)) and not OS.path.isfile(OS.path.join("downloaded", episode_filename + ".aria2")):
			return
		if OS.name == 'posix':
			while True:
				try:
					SP.call(cmd.split())
					break
				except KeyboardInterrupt: input("\nDownloader is paused. PRESS [ENTER] TO CONTINUE...")
		else:
			while True:
				try:
					OS.system(cmd)
					break
				except KeyboardInterrupt: input("\nDownloader is paused. PRESS [ENTER] TO CONTINUE...")
		if OS.path.isfile(OS.path.join("downloaded", self.__title.replace(' ', '_') + ".mp4.aria2")):
			FailedContainer.addFailedCommand(cmd)

###----------------###
#### MAIN ROUTINE ####
###----------------###

def main():
	print("\t\t|=======================|")
	print("\t\t| DRAMA-NICE DOWNLOADER |")
	print("\t\t|=======================|\n")
	thedrama = Drama(input(" - Enter Drama main-page URL: "))
	print("\t -FOUND:", thedrama.getTotalEpisodeCount(), " Episodes in TOTAL!\n")
	thedrama.collectEpisodes(int(input("\t - Start From Episode: ")), int(input("\t - End At Episode: ")))
	print("\nStarting Download using aria2...\n")
	#thedrama.displayEpisodes()
	#thedrama.displayDownloadLinks()
	thedrama.downloadEpisodes()
	print("=======================================================")
	print("-------------------- COMPLETED !!! --------------------")
	print("=======================================================")
	FailedContainer.retryFailedDownloads()
	print("Checking downloads...")
	thedrama.finalizeDrama()
	print("Done!")

main()
#Drama('https://dramanice.video/bride-of-the-century/')
