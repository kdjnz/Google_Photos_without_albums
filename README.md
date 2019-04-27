Currently (April 2019) there's no function in Google Photos to view files that don't belong to a folder.
This script simply provides a list of files that do not belong in a folder.

This script finds all file IDs (photos and videos) and stores in list 1.
Then it finds all album IDs, then all file IDs that belong to each album ID to store in list 2.
Then we check to see if each of the file IDs in list 1 is also in list 2, if not, it's returned in the final output in the form of the file name and URL.
This gives a list to then manually access each file and assign a folder as required.

Unfortunately at the time of writing, there's no API method to modify the album details of a file, so it just relies on manually updating each file.

Please note, this is my very first working Python script. I'm not a developer, and I took it on as an opportunity to learn about Python using easily accessible Google APIs, with the aim to solve a real world problem.

I'm sure there are better ways to achieve what I have created, and I hope to improve as I continue learning about this language.
Constructive feedback is welcome, criticism isn't.

Thanks.

How to use:

If you need to set up your environment, follow the guide here:
https://developers.google.com/api-client-library/python/start/get_started

Once set up, within the directory of the main.py file, at the Python command line type:
$ main.py [client_id] [client_secret]

Tip: Use a Google Photo instance with a few files to test it first. Currently I have 10,000+ files and I have get back a (correct) list of 5,000 items without folders...So it takes some time to work through these and create the output list.
