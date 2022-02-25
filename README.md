# CamView
> A CLI-tool used to stream CCTV online footage based on URL params

<br>

## Get Started
To get started with CamView, simply download the ``camview.py`` file and download the required libs, and then run.
1. ``pip install -r requirements.txt``
2. ``python camview.py``

CamView has some optional flags for different modes. To use as normal, you do not need to include any of these. However, for devices with certain constraints, there is an optional CLI mode where images are converted and then printed to the terminal. To use this feature, type:
``` bash
python camview.py --cli
```

<br>

## Screenshot(s)

![Imgur](https://i.imgur.com/mACCAfU.png)

<br>

## About CamView
CamView works on part magic, part Python, and part Google! It wouldn't be fair for me to take all the credit, when in fact CamView builds on top of each of these tools.

The process CamView uses is detailed a bit more here for those who are interested.
1. First, we take the string (either specified by the user or the selected preset) and use it as a Google query like
``inurl:query``. This is a well-known process for finding things on the internet, and used more widely outside of misconfigured/public webcam discovery to find exploitable servers or logins with default credentials. More on this process (called Google Hacking), can be found [here](https://en.wikipedia.org/wiki/Google_hacking)
2. Next, we take all the google search results, and send them to a verify function, where we request the page and check the response. If the page loads as expected, we send the url on, if not, we don't use that url later.
3. Using the urls we've uncovered, we load each of them and inject a custom JS script into each page. This JS script (since there is no set way to find the stream, as it is an <img> element) will iterate through every image on the site, and then return the one with the largest dimensions. (We go off the assumption that the largest image must be the stream, but ocassionally we are wrong.
4. Once we have this image in our python script, we open a new thread and display the image using the OpenCV tools, either in the default video player, or we convert the frame with climage and print it as is.

<br>

## Licence
```
Copyright 2022 Finn Lancaster

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```
