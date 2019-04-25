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

def main():

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
  ids_in_album = set()
    
  try: 

#Gets a list of all mediaItem IDs
    nextpageToken = None
    i=0    
    request = service.mediaItems().list(pageSize=10, pageToken=nextpageToken)

    while request != None:
      response = request.execute()
      nextpageToken = response.get('nextPageToken')
      all_mediaitems = response.get('mediaItems', [])

      for item in all_mediaitems:
        all_ids.add(item['id'])

      request = service.mediaItems().list_next(request, response)
      i=i+10
      print (i)
      if i>20:
        break

    id_count = len(all_ids)
    print ('All mediaitem IDs (' + str(id_count) + ') collected!')

    
#Gets a list of all album IDs
    nextpageToken = None
    request = service.albums().list(pageSize=25, pageToken=nextpageToken)

    while request != None:
      response = request.execute()
      nextpageToken = response.get('nextPageToken')
      all_albums_res = response.get('albums', [])

      for item in all_albums_res:
        all_albums.add(item['id'])     
                        
      request = service.mediaItems().list_next(request, response)
     
    album_count = len(all_albums)
    print ('All Album IDs ('+ str(album_count) + ') collected!')
    

#Gets a list of mediaItem IDs for a specified Album ID
def items_in_album(albumId)

    #albumId = 'AOeO1cZkS_ibfao2UP31k7vezVZB1gVQUDobJ5mCrjwuv2wnKiNYy9gLjGgdRDParA69N_EV1tK2'
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
        ids_in_album.add(item['id'])
        
      request = service.mediaItems().list_next(request, response)
 
    id_count = len(ids_in_album)
    return print ('All mediaitem IDs (' + str(id_count) + ') in the Album collected!')

      
  except AccessTokenRefreshError:
    # The AccessTokenRefreshError exception is raised if the credentials
    # have been revoked by the user or they have expired.
    print ('The credentials have been revoked or expired, please re-run'
           'the application to re-authorize')

if __name__ == '__main__':
  main()
