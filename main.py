#!/usr/bin/python
#
# Copyright 2012 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# https://developers.google.com/api-client-library/python/start/get_started

import json
import httplib2
import sys

from apiclient.discovery import build
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import OAuth2WebServerFlow

# For this example, the client id and client secret are command-line arguments.
client_id = '984906845754-sjigo0sol9um69meshbsq3djeqp9at8s.apps.googleusercontent.com'
client_secret = 'uZHfhF1kXZWgLsUMdYA_XPY6'

# The scope URL for read/write access to a user's photos
scope = 'https://www.googleapis.com/auth/photoslibrary'

# Create a flow object. This object holds the client_id, client_secret, and
# scope. It assists with OAuth 2.0 steps to get user authorization and
# credentials.
flow = OAuth2WebServerFlow(client_id, client_secret, scope)

# Create a Storage object. This object holds the credentials that your
# application needs to authorize access to the user's data. The name of the
# credentials file is provided. If the file does not exist, it is
# created. This object can only hold credentials for a single user, so
# as-written, this script can only handle a single user.
storage = Storage('credentials.dat')

# The get() function returns the credentials for the Storage object. If no
# credentials were found, None is returned.
credentials = storage.get()

  # If no credentials are found or the credentials are invalid due to
  # expiration, new credentials need to be obtained from the authorization
  # server. The oauth2client.tools.run_flow() function attempts to open an
  # authorization server page in your default web browser. The server
  # asks the user to grant your application access to the user's data.
  # If the user grants access, the run_flow() function returns new credentials.
  # The new credentials are also stored in the supplied Storage object,
  # which updates the credentials.dat file.
if credentials is None or credentials.invalid:
  credentials = tools.run_flow(flow, storage, tools.argparser.parse_args())

  # Create an httplib2.Http object to handle our HTTP requests, and authorize it
  # using the credentials.authorize() function.
http = httplib2.Http()
http = credentials.authorize(http)

  # The apiclient.discovery.build() function returns an instance of an API service
  # object can be used to make API calls. The object is constructed with
  # methods specific to the photos API. The arguments provided are:
  #   name of the API ('photos')
  #   version of the API you are using ('v1')
  #   authorized httplib2.Http() object that can be used for API calls
service = build('photoslibrary', 'v1', http=http)

all_ids = set()
all_albums = set()
ids_from_albums = set()
no_album = set()


def main():
  try:
    
    print (get_all_items(100))
    print(get_album_ids(25))
    print(find_them(ids_from_albums, all_ids))

    i=1
    for x in no_album:

        print (str(i) + ') ' + get_details(x))
        i = i + 1
     
  except AccessTokenRefreshError:
    # The AccessTokenRefreshError exception is raised if the credentials
    # have been revoked by the user or they have expired.
    print ('The credentials have been revoked or expired, please re-run the application to re-authorize')


def get_all_items(ps):
#Gets a list of all mediaItem IDs
    nextpageToken = None
    i=0
    request = service.mediaItems().list(pageSize=ps, pageToken=nextpageToken)

    while request != None:
      response = request.execute()
      nextpageToken = response.get('nextPageToken')
      all_mediaitems = response.get('mediaItems', [])

      for item in all_mediaitems:
        all_ids.add(item['id'])
        
      request = service.mediaItems().list_next(request, response)
      i = i + ps
      print (str(i) + ' processed so far...')
      #if i > 500:
      # break
      
    id_count = len(all_ids)
    return ('All mediaItem IDs (' + str(id_count) + ') collected!')
    

def get_album_ids(ps):
    #Gets a list of all album IDs
    i=0
    total_ids_in_albums = 0
    nextpageToken = None
    request = service.albums().list(pageSize=ps, pageToken=nextpageToken)

    while request != None:
      response = request.execute()
      nextpageToken = response.get('nextPageToken')
      all_albums_res = response.get('albums', [])

      for item in all_albums_res:
        
        all_albums.add(item['id'])
        id_count = get_items_in_album(item['id'])
        total_ids_in_albums =  total_ids_in_albums + id_count
                
      request = service.mediaItems().list_next(request, response)
      i = i + ps
      print (str(i) + ' albums processed so far...')
      #if i > 10:
      #  break

    album_count = len(all_albums)
    
    return (str(total_ids_in_albums) + ' total mediaItems from ' + str(album_count) + ' albums')


def get_items_in_album(albumId):
    #Gets a list of mediaItem IDs for a specified Album ID
    nextpageToken = None

    body = {
    "albumId": albumId,
    "pageSize": 50, #max=100
    "pageToken": nextpageToken
    }

    request = service.mediaItems().search(body=body)

    while request != None:
      response = request.execute()
      nextpageToken = response.get('nextPageToken')
      mediaitems = response.get('mediaItems', [])

      for item in mediaitems:
        ids_from_albums.add(item['id'])

      request = service.mediaItems().list_next(request, response)

    id_count = len(ids_from_albums)
    return id_count
            

def get_details(mediaitem):
  #Gets the details of a single mediaItem
  request = service.mediaItems().get(mediaItemId=mediaitem)
  response = request.execute()
  URL = response.get('productUrl', [])
  FileName = response.get('filename', [])
  return (FileName + ' | ' + URL + '\n')


def find_them(list_a, list_b):
  i=0
  x=0
  for num in list_b:
    if num not in list_a:
      no_album.add(num)
      x = x + 1
    i = i + 1
  return (str(i) + ' total items checked, & ' + str(x) + ' mediaItems found without an album:')

if __name__ == '__main__':
  main()
