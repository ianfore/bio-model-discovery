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

 
def getSampleAttributes(attDetails, url):
#	print (urllib.urlopen(url).read())
 	tree = ET.parse(urllib.urlopen(url))
 	root = tree.getroot()
 	for samp in root:
 		print ("sample:" + str(samp.get('id')))
 		atts = samp.find('Attributes')	
 		for att in atts:
 			aname = str(att.get('harmonized_name'))
 			if aname == 'None':
 				aname = str(att.get('attribute_name'))
 			if aname in attDetails:
 				attDetails[aname]['sampleCount'] += 1
 				if att.text in attDetails[aname]['values']:
 					attDetails[aname]['values'][att.text] += 1
 				else:
 					attDetails[aname]['values'][att.text] = 1
 			else:
 				attDetails[aname] = {'sampleCount' : 1, 'values' : {att.text : 1}}

	
def bioprojectAttributes(bioprojectID,apikey):
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

	getSampleAttributes(attDetails, url)
	print ('____________________________________')
	
	# Get some details of the bioproject
 	tree = ET.parse(urllib.urlopen(pfetch+bioprojectID))
 	root = tree.getroot()
 	project = root[0][0]
 	accession = project[0][0].get('accession')
 	title = project.find('ProjectDescr').find('Title').text
	print ('Attribute details for BioProject ID: ' + bioprojectID)
 	print ('Accession:'+accession)
 	print ('Title:'+title)
 	
	# Summarize the attributes for this bioproject
	uniques = {}	
	almostUniques = {}	
	constants = {}	
	singleValue = {}	
	print ('No of samples:' + str(sCount))
 	print ('____________________________________')
 	print (	'The following attributes vary across samples.')
 	print (	'Some may indicate the project design/model.')
 	print (	'Some may be sample/subject observations/measurements/data elements.')
 	print
 	for aname, att in attDetails.items():
 		vList = att['values']
 		if len(vList) == att['sampleCount']:
 			uniques[aname] = att
 			att['variability'] = 'u'
 		elif 100.0*len(vList)/att['sampleCount'] > 80.0:
 			almostUniques[aname] = att
 			att['variability'] = 'au'
 		elif len(vList) == 1:
 			if vList.values()[0] == sCount:
 				constants[aname] = att
 				att['variability'] = 'c'
 			else:
 				singleValue[aname] = att
 				att['variability'] = 's'
 		else:
 			att['variability'] = 'v'
 			print ('Attribute:' + aname + ' total:' + str(att['sampleCount']))
 			for v, vCount in att['values'].items():
 				print (v, vCount)
 			print ('____________________________________')
 		
 	if len(uniques):
		print (	'The following attributes have a unique value for each sample. ')
		print (	'They are therefore likely to some kind of identifier.')
		for a, att in uniques.items():
			print (a, att['sampleCount'])
		print ('____________________________________')
 	if len(almostUniques):
		print (	'The following attributes have a unique value for more than 80% of samples.')
		print (	'They are often a subject identifier.')
		for a, att in almostUniques.items():
			print (a, att['sampleCount'])
		print ('____________________________________')
 	if len(constants):
		print (	'The following have the same value for all samples.')
		print (	'They are likely to be an attribute of the study rather than the sample')
		for a, att in constants.items() :
			print (a+':'+att['values'].keys()[0] )
		print ('____________________________________')
 	if len(singleValue):
		print (	'The following have only one value in the bioproject')
		print (	'but the attribute is not present for all samples')
		for a, att in singleValue.items() :
			print (a+':'+att['values'].keys()[0] + ' ' + str(att['values'].values()[0]))
		print ('____________________________________')
#	work in progress - do a json dump of the attribute details
#	projDict = {"accession":accession, "title":title, "attributes" : attDetails}	
#	print (json.dumps(projDict, indent=4, separators=(',', ': ')))
#	print (json.dumps(attDetails.keys(), indent=4, separators=(',', ': ')))
#	print (type(attDetails.keys()))
#	export for analysis
#  	f = open('data/attributes.txt', 'a')
#  	for attKey, att in attDetails.items():
#  		f.write( str(bioprojectID)+'\t'+attKey+'\t'+str(att['sampleCount'])+'\t'+att['variability']+'\n')
#  	f.close

def usage():
	print (sys.argv[0] +' -k apikey -b bioprojectid')
	
def main(argv):
    bioprojectid = ''
    apikey = ''
    maxsamples = 5000
    try:
        opts, args = getopt.getopt(argv, "hb:k:", ["help", "bioprojectid=", "apikey="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-b", "--bioprojectid"):
            bioprojectid = arg
        elif opt in ("-k", "--apikey"):
            apikey = arg

    bioprojectAttributes(bioprojectid,apikey)
    
if __name__ == "__main__":
    main(sys.argv[1:])


	