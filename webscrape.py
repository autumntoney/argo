# -*- coding: utf-8 -*-
#importing packages needed for the following script
import cookiejar
import http.cookiejar as cookielib
import cgi
import requests
import sys
import urllib3 
import mechanize
from time import sleep
import os
from io import BytesIO
import pandas as pd



#importing the csv file from the site that will give the object_ids
#This will require the appropriate path to run correctly. I uploaded the csv in my jupyter notebook home or else
#the input would look like "C:/user/autumn/documents/Elevation Certificates - All.csv"

elevation_certs = pd.read_csv("Elevation Certificates - All.csv")

# A routine to download a file from a link, by simulating a click on it
#this is the function that we use to locate all pdfs and save them to our machine
def downloadlink(linkUrl, referer):
    r = br.click_link(linkUrl)
    r.add_header("Referer", referer) # add a referer header, just in case
    response = br.open(r)
    

    #get filename from the response headers if possible
    cdheader = response.info().get('Content-Disposition')
    if cdheader:
        value, params = cgi.parse_header(cdheader)
        filename  = params["filename"]
    else:
        # if not use the link's basename
        filename = os.path.basename(linkUrl.url)
    
    
    f = open(i + "_"+ filename + ".pdf", "wb") #TODO: perhaps ensure that file doesn't already exist?
    f.write(response.read()) # write the response content to disk
    print(filename," has been downloaded")
    br.back()

# Make a Browser (think of this as chrome or firefox etc)
br = mechanize.Browser()

# Enable cookie support for urllib2 
cookiejar = cookielib.LWPCookieJar() 
br.set_cookiejar( cookiejar ) 

# Broser options 
br.set_handle_equiv( True ) 
br.set_handle_gzip( True ) 
br.set_handle_redirect( True ) 
br.set_handle_referer( True ) 
br.set_handle_robots( False ) 
br.set_handle_refresh( mechanize._http.HTTPRefreshProcessor(), max_time = 1 ) 
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')] # masquerade as a real browser. this is not nice to do though.

#   Open your site--we have to iterate through all object ID's:
#   this was a little example I used to make sure that the code ran smoothly we will be using the entire object_id column
#   ob_id = elevation_certs['OBJECTID']

object_id = ["10802", "10803", "10804"]


for i in object_id:
    #select the webpage (this is the part that is iterated through to grab every data entry)
    mypageUrl = "https://maps.floridadisaster.org/gis/rest/services/Feature/Elevation_Certificates/MapServer/0/" + i + "/attachments/"
    br.open(mypageUrl)

    print("Get all PDF links\n")
    filetypes=["pdf", "PDF"] # pattern matching for links, can add more kinds here
    myfiles=[]
    for l in br.links():
    #check if this link has the file extension or text we want
        myfiles.extend([l for t in filetypes if t in l.url or t in l.text])

    for l in myfiles:
# for index, l in zip(range(100), myfiles): # <--- uncomment this line (and coment the one above) to download 100 links.
    #sleep(1) # uncomment to throttle downloads, so you dont hammer the site
        downloadlink(l, mypageUrl)