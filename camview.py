from ast import arguments
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import climage
import os
import cv2
from time import sleep
from multiprocessing import Process
import argparse

# global setup for selenium
chrome_options = Options()
chrome_options.headless = True
driver = webdriver.Chrome(options=chrome_options)

urls = []
pics = []

parser = argparse.ArgumentParser(description='Find and stream online CCTV footage.')
parser.add_argument(
   	'-c', '--cli',
   	action='store_true',
   	help='Optional: Draws images to the terminal, as opposed to streaming.'
)

_args = parser.parse_args()

# clears console for re-writing
def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def header():
    print("""
============================================================================
____   ________   ___ __ __   __   __   ________  ______   __ __ __      
/_____/\ /_______/\ /__//_//_/\ /_/\ /_/\ /_______/\/_____/\ /_//_//_/\     
\:::__\/ \::: _  \ \\::\| \| \ \\:\ \\ \ \\__.::._\/\::::_\/_\:\\:\\:\ \    
 \:\ \  __\::(_)  \ \\:.      \ \\:\ \\ \ \  \::\ \  \:\/___/\\:\\:\\:\ \   
  \:\ \/_/\\:: __  \ \\:.\-/\  \ \\:\_/.:\ \ _\::\ \__\::___\/_\:\\:\\:\ \  
   \:\_\ \ \\:.\ \  \ \\. \  \  \ \\ ..::/ //__\::\__/\\:\____/\\:\\:\\:\ \ 
    \_____\/ \__\/\__\/ \__\/ \__\/ \___/_( \________\/ \_____\/ \_______\/ 

                                By: BLUND3R

============================================================================
    """)
"""
first, we present user with logo
then, we get their input (preset string or custom)
we use this string with selenium in order to grab urls
check urls with requests lib to see if 200 OK. If so, GET them
use JS via selenium to grab stream img element, and then render in console.
"""

def display_stream(*args):
    cls()
    header()

    if type(args) is tuple:
        print('*** Press esc to escape ***')
        cap = cv2.VideoCapture(args[0])

        while True:
            try:
                ret, frame = cap.read()
                resized = cv2.resize(frame, (250, 250))   
                cv2.imshow('Video', resized)

                if cv2.waitKey(1) == 27:
                    cap.release()
            except:
                return

    else:
        for pic in pics:
            # convert stream to image, and print
            # to terminal.

            # open cv get current frame of stream 
            try:
                cap = cv2.VideoCapture(pic)
                ret, frame = cap.read()

                # write frame to stream.jpg to render later
                cv2.imwrite("stream.jpg",frame)

                cap.release()

                image = climage.convert('stream.jpg', is_unicode=True)

                print(image)
            except:
                return

        print("*** CTRL+C to exit at any time ***")

    if _args.cli is True:
        while True:
            # update the images
            sleep(10)

            display_stream(pics)

    cv2.destroyAllWindows()
    return

def check_status(url):
    try:
        r = requests.get(url, timeout=10)
    except:
        # return False ontimeout
        return False

    if r.status_code == 200:
        return True
    else:
        return False

def run_query(query):
    driver.get("https://www.google.com/search?q=inurl:"+query)

    sleep(1)

    # now we get all results
    results = driver.find_elements_by_xpath("//div[@class='yuRUbf']//a")

    cls()
    print("loading...\n\nPlease be patient - it can take a while to connect to cams...")

    for result in results:
        urls.append(result.get_attribute('href'))

    for result in urls:
        #print("checking")
        res = check_status(result)

        if res == True:
            #print("getting stream")
            driver.get(result)

            loaded = False
            while loaded == False:
                if (driver.execute_script("return document.readyState") == "complete"):
                    loaded = True

            try:
                stream_link = driver.execute_script("""
                var imgs = document.querySelectorAll('img');
                var elem;
                var stream = 0;
                var hstream = 0;

                for (var i=0; i<imgs.length; i++) {
                    if ((imgs[i].clientWidth > stream)&&(imgs[i].clientHeight > hstream)) {
                        elem = imgs[i].src;
                        stream = imgs[i].clientWidth;
                        hstream = imgs[i].clientHeight;
                    }
                }

                return elem;
                """)

                pics.append(stream_link)

                if _args.cli is True:
                    stream_thread = Process(target = display_stream)

                    if result == urls[0]:
                        stream_thread.start()
                else:
                    # use more modern multithreading here
                    stream_thread = Process(target = display_stream, args=(stream_link, ))
                    stream_thread.start()

            except:
                pass

    return

def presets():
    cls()
    header()

    query = input("""
1. /view.shtml
2. /view/index.shtml
3. /mjpg/video.mjpg
4. /cgi-bin/camera?resolution=

99. go back

>>> """)

    if query == "1":
        run_query("/view.shtml")
    elif query == "2":
        run_query("/view/index.shtml")
    elif query == "3":
        run_query("/mjpg/video.mjpg")
    elif query == "4":
        run_query("/cgi-bin/camera?resolution=")
    elif query == "99":
        start_screen()
    else:
        presets()

    return

def start_screen():
    cls()
    header()

    sel = input("""  
                         Select an Option to begin:

1. Choose a preset query string.
2. Use a custom preset query string.

99. exit

>>> """)

    if sel == "1":
        presets()
    elif sel == "2":
        custom = input("""
Enter custom query string, or 99 to go back.

>>> """)
        if custom == "99":
            start_screen()
        else:
            run_query(str(custom))
    elif sel == "99":
        os._exit(0)

    return

try:
    start_screen()
except KeyboardInterrupt:
    cls()
    os._exit(0)