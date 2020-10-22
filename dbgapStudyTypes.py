#!/usr/bin/python
import sys
import getopt
import requests
import json
import xml.etree.ElementTree as ET
import urllib

# Retrieve the attributes of the samples for a specified BioProject and summarize
# the values of those attributes across the project.
# The intent is to provide a report which will help a user
# 1. Identify the data model of the study
# 2. Identify if the project uses a template similar to other studies


	
def bioprojectAttributes(apikey):
	eutils = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
	esearch = eutils + 'esearch.fcgi?db=gap&retmode=json&api_key='+apikey
#	pfetch = eutils + 'efetch.fcgi?db=bioproject&api_key='+ apikey+'&id='
#	sfetch = eutils + 'efetch.fcgi?db=biosample&api_key='+ apikey
	
	# get linked samples
	url = esearch + '&id=phs000001' #+ bioprojectID 
	print url
#	attDetails = {}

	# first we do the query and get a list of ids so we know how many hits we get
	r = requests.get(url)
	b = r.json()
	print(b)
#	d = b['linksets'][0]['linksetdbs'][0]['links']
#	sCount = len(d)
	

def usage():
	print sys.argv[0] +' -k apikey '
	
def main(argv):
    bioprojectid = ''
    apikey = ''
    maxsamples = 5000
    try:
        opts, args = getopt.getopt(argv, "k:", ["help",  "apikey="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-k", "--apikey"):
            apikey = arg

    bioprojectAttributes(apikey)
    
if __name__ == "__main__":
    main(sys.argv[1:])


	