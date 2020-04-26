# py-dramanice-downloader

Downloads the specified range of drama episodes from DramaNice ( https://dramanice.video/ ) using the Drama URL provided.

# Packages needed

requests, bs4 (BeautifulSoup), os, subprocess, re.
Some of them are available by default, especially if you have anaconda installed. If not, you can insatll them using pip.

# Dependencies

This program uses aria2 cli downloader. https://aria2.github.io/
The aria2c.exe must also be inside PATH environment variable.

# For Linux users

- Install python3.
- Use pip to install needed packages if they aren't installed already.
- Install aria2 using 'sudo apt-get install aria2'
- Run downloader.py using python3 and enjoy!!!

# For Windows users

- Install python3.
- Install the required packages using the command 'pip install package-name' (for each package) on your command-prompt.
- Download aria2 from official site: https://aria2.github.io/
- In C: drive, make a folder named 'aria2' and paste the contents of downloaded aria2 zip.
- Add the path to aria2c.exe in system environment variable PATH. (e.g. 'C:\aria2')
- Run downloader.py using python3 and enjoy!!!

# Important note!

I am not responsible for the content you download using this script. The downloaded videos will by present in "CurrentWorkingDirectory/downloaded" folder.
Please report if there are any issues so that this tool can be further improved!

# HOW TO USE?

Just copy the link of the Drama you want to download, from the site DramaNice ( https://dramanice.video/ ).
For example: https://dramanice.video/bride-of-the-century/

After link is copied:

Run downloader.py using python3.
Paste the Drama link in the terminal/command-prompt and press ENTER.
Provide the range of episodes you want to download.
PAUSE AN ONGOING DOWNLOADE: Press [Ctrl+C] to pause download. To exit, press [Ctrl+C] again.

RESUME DOWNLOADS: Run program again, already downloaded episodes will not be downloaded again. The episodes which are partially downloaded, will automatically resume from where they stopped.

Note:- The drama episodes will be downloaded in a folder inside the current working directory where the downloader.py exists. You can move it somewhere else later!
