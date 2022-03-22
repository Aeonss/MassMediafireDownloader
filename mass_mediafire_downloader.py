from tkinter import *
from urllib.request import Request, urlopen, urlretrieve
from pathlib import Path
import subprocess
import os

urls = [] # URLs to get downloaded rars from
download_path = str(Path.home() / "Downloads") # Download path

# On submit button
def submit():

    print("\n\n\n")
    print("=====================================================================================================================")
    print("|      __  __              __  __        _ _       __ _           ___                  _              _             |")
    print("|     |  \/  |__ _ ______ |  \/  |___ __| (_)__ _ / _(_)_ _ ___  |   \ _____ __ ___ _ | |___  __ _ __| |___ _ _     |")
    print("|     | |\/| / _` (_-<_-< | |\/| / -_) _` | / _` |  _| | '_/ -_) | |) / _ \ V  V / ' \| / _ \/ _` / _` / -_) '_|    |")
    print("|     |_|  |_\__,_/__/__/ |_|  |_\___\__,_|_\__,_|_| |_|_| \___| |___/\___/\_/\_/|_||_|_\___/\__,_\__,_\___|_|      |")
    print("====================================================================================================================|")
    print()

    # Get links from URL and add to urls list
    urls = text.get("1.0", "end-1c").split("\n")

    # For each url in the list
    for url in urls:

        # Remove white spaces
        url = url.strip().replace(" ", "")

        # If url is empty, skip it
        if (url == ''):
            continue
        
        print("\n\n\nPage: " + url)

        # Get the html of the page
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

        # See if the page is from mrcong.com and if it is a valid website
        try:
            page = urlopen(req).read()
        except:
            print("\nInvalid URL: " + url)
        
        # Translate page from bytes to string
        page_html = page.decode('utf-8')

        # Get the mediafire link from the page
        page_start = page_html.find("mediafire.com/")
        page_end = page_html.find(".rar/file", page_start, len(page_html)) + 9

        # Mediafire link
        mediafire_url = "https://" + page_html[page_start:page_end]

        print("Mediafire URL: " + mediafire_url)
        
        # Get the file name from the URL
        file_name = mediafire_url.split("/")[5]

        # Get the html of the mediafire page
        req = Request(mediafire_url, headers={'User-Agent': 'Mozilla/5.0'})
        mediafire = urlopen(req).read()
        mediafire_html = mediafire.decode('utf-8')

        # Get the direct mediafire download link
        mediafire_start = mediafire_html.find("Download file")
        mediafire_end = mediafire_html.find(".rar", mediafire_start, len(mediafire_html)) + 4

        # Direct download link
        direct_url = mediafire_html[mediafire_start:mediafire_end].strip().replace(" ", "").replace("\n", "")[19:]

        print("Direct Download Link: " + direct_url)
        print("\nDownloading...")

        # Download directly to pc
        file_path = os.path.join(download_path, file_name)
        urlretrieve(direct_url, filename=file_path)

        # For each file in download folder
        for f in os.listdir(download_path):

            # Check if file is rar file
            if f.endswith(".rar"):
                
                # Extract rar file with password
                subprocess.run(["unrar", "x", "-p" + password.get("1.0", 'end-1c'), "-op" + download_path, os.path.join(download_path,f)])

                # Delete rar file
                os.remove(file_path)
    
    # Exit program after finished operations
    print("\n\n\nThank you for using Mass Mediafire Downloader")
    exit()
        
        

# Open window with text area for input
window = Tk()
window.eval('tk::PlaceWindow . center')
window.title("Mass Mediafire Downloader")
window.resizable(False, False)

# Create frames
topFrame = Frame(window, bg="#191919")
topFrame.pack(side=TOP)
bottomFrame = Frame(window, bg="#191919")
bottomFrame.pack(side=BOTTOM, fill=BOTH, expand=True)

# Create text field
text = Text(window, bg="#191919", font=("Arial", 14), height=25, width=50, fg="white", padx=10, pady=10)
text.pack(in_=topFrame)

# Create password field
password = Text(window, bg = "#191919", font=("Arial", 10), height=1, width=25, fg="white")
password.pack(in_=bottomFrame, side=LEFT, padx=10, pady=5)

# Create button
button = Button(window, text="Get Images", command=submit)
button.pack(in_=bottomFrame, side=LEFT, padx=50)

window.mainloop()
