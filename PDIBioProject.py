''' Module to integrate functions of this tool into Pentaho Data Integration'''
#!/usr/bin/python
import sys
import getopt
import requests
import json
import xml.etree.ElementTree as ET
import urllib
import pandas as pd

# Retrieve the attributes of the samples for a specified BioProject and summarize
# the values of those attributes across the project.
# The intent is to provide a report which will help a user
# 1. Identify the data model of the study
# 2. Identify if the project uses a template similar to other studies

 
def getSampleAttributes(attDetails, url,rows_list):
#	print (urllib.urlopen(url).read())
 	tree = ET.parse(urllib.urlopen(url))
 	root = tree.getroot()
 	for samp in root:
# 		print ("sample:" + str(samp.get('id')))
 		newRow = {}
 		atts = samp.find('Attributes')	
 		for att in atts:
 			aname = str(att.get('harmonized_name'))
 			if aname == 'None':
 				aname = str(att.get('attribute_name'))
 			newRow[aname]=att.text


 		rows_list.append(newRow)		

	
def bioprojectAttributes(bioprojectID,apikey,rows_list):
	eutils = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
	elink = eutils + 'elink.fcgi?dbfrom=bioproject&db=biosample&retmode=json&linkname=bioproject_biosample&api_key='+apikey
	pfetch = eutils + 'efetch.fcgi?db=bioproject&api_key='+ apikey+'&id='
	sfetch = eutils + 'efetch.fcgi?db=biosample&api_key='+ apikey
	
	# get linked samples
	url = elink + '&id=' + bioprojectID 
	attDetails = {}

	# first we do the query and get a list of ids so we know how many hits we get
	r = requests.get(url)
	b = r.json()
	d = b['linksets'][0]['linksetdbs'][0]['links']
	sCount = len(d)
	# now do the same query to set up the list in the history server
	# there may be a way of getting the list size from this second query -
	# but I haven't found how	
	url += '&cmd=neighbor_history'
	r = requests.get(url)
	b = r.json()
	d = b['linksets'][0]
	webenv = d['webenv']
	querykey = d['linksetdbhistories'][0]['querykey']
	# set up query for sample details to use list of ids from the previous query
	url = sfetch + '&query_key='+querykey+'&WebEnv='+webenv
	rows_list.append({'json':b})
	getSampleAttributes(attDetails, url,rows_list)

	


# Initialisation for debugging
#data = [{'bioprojectid': '338795', 'filename': 'a.txt', 'bpid':'421626'}] 
data = [{'bioprojectid': '421626', 'filename': 'a.txt', 'bpid':'421626'}] 
#data = [{'bioprojectid': '279695', 'filename': 'a.txt', 'bpid':'421626'}] 
bplist = pd.DataFrame(data) 

# bplist is the data frame passed in from Pentaho
bplist.bioprojectid = bplist.bioprojectid.astype(str)

apikey = 'ea801de3bee6b4f2186e609a23108ccec508'
maxsamples = 5000

rows_list = []
for index, row in bplist.iterrows():
	#rows_list.append({'akey':index,'avalue':row['bioprojectid']})
	bioprojectAttributes(row['bioprojectid'],apikey,rows_list)


df= pd.DataFrame(rows_list)
#print df



	