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

 
def getSampleAttributes(sampleID, attList, attDetails, url):
#	print (urllib.urlopen(url+str(sampleID)).read())
 	tree = ET.parse(urllib.urlopen(url+str(sampleID)))
 	root = tree.getroot()
 	for samp in root:
 		print ("sample:" + str(samp.get('id')))
 		atts = samp.find('Attributes')	
 		for att in atts:
 			aname = str(att.get('harmonized_name'))
			if aname == 'None':
				aname = str(att.get('attribute_name'))
 			if aname in attList:
 				attList[aname] += 1
 				if att.text in attDetails[aname]:
 					attDetails[aname][att.text] += 1
 				else:
 					attDetails[aname][att.text] = 1
 			else:
 				attList[aname] = 1
 				attDetails[aname] = {att.text : 1}

	
def bioprojectAttributes(bioprojectID,apikey):
	eutils = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
	elink = eutils + 'elink.fcgi?dbfrom=bioproject&db=biosample&retmode=json&linkname=bioproject_biosample&api_key='+apikey
	pfetch = eutils + 'efetch.fcgi?db=bioproject&api_key='+ apikey+'&id='
	sfetch = eutils + 'efetch.fcgi?db=biosample&api_key='+ apikey+'&id='
	
	# get linked samples
	# the behavior of elink is such that the call to it will only retrieve 500 samples
	# for now that is a good enough way to stop the program consuming resources
	url = elink + '&id=' + bioprojectID 
	attList = {}
	attDetails = {}

#	print url
	r = requests.get(url)
	b = r.json()
	d = b['linksets'][0]
	p = d['linksetdbs'][0]
	h = p['links']
	
	# call efetch for a chunk of sample ids in one go
	# so far calling for 25 ids at once seems to be a good compromise between the number
	# of calls that must be made and requesting too many ids which makes any call too slow
	idchunk = 25
 	for i in xrange(0,len(h),idchunk):
 		# create a slice of ids and turn it into a comma delimited string w no spaces
 		# the ids are numbers - so they must also be converted to strings
		sl = ','.join(map(str, h[i:i+idchunk])) 
 		getSampleAttributes(sl, attList, attDetails, sfetch)
 		print '____________________________________'
 	
 	# Get some details of the bioproject
 	tree = ET.parse(urllib.urlopen(pfetch+bioprojectID))
 	root = tree.getroot()
 	project = root[0][0]
 	archiveId = project[0][0]
 	desc = project.find('ProjectDescr')
	print 'Attribute details for BioProject ID: ' + bioprojectID
 	print 'Accession:'+archiveId.get('accession')
 	print 'Title:'+desc.find('Title').text
 	
	# Summarize the attributes for this bioproject
	uniques = {}	
	almostUniques = {}	
	constants = {}	
	print 'No of samples:' + str(len(h))
 	print '____________________________________'
 	print 	'The following attributes vary across samples.'
 	print 	'Some may indicate the project design/model.'
 	print 	'Some may be sample/subject observations/measurements/data elements.'
 	print
 	for a, vList in attDetails.items():
 		if len(vList) == attList[a]:
 			uniques[a] = vList
 		elif 100.0*len(vList)/attList[a] > 80.0:
 			almostUniques[a] = vList
 		elif len(vList) == 1 and vList.values()[0] == len(h):
 			constants[a] = vList
 		else:
 			print 'Attribute:' + a + ' total:' + str(attList[a])
 			for v in vList:
 				print v, vList[v]
 			print '____________________________________'
 		
 	if len(uniques):
		print 	'The following attributes have a unique value for each sample. '
		print 	'They are therefore likely to some kind of identifier.'
		for a in uniques:
			print a, attList[a]
		print '____________________________________'
 	if len(almostUniques):
		print 	'The following attributes have a unique value for more than 80% of samples.'
		print 	'They are often a subject identifier.'
		for a in almostUniques:
			print a, attList[a]
		print '____________________________________'
 	if len(constants):
		print 	'The following have the same value for all samples.'
		print 	'They are likely to be an attribute of the study rather than the sample'
		for a, vList in constants.items() :
			print a+':'+vList.keys()[0] 
		print '____________________________________'
#	work in progress - do a json dump of the attribute details	
# 	print json.dumps(attDetails, sort_keys=True, indent=4, separators=(',', ': '))
	

def usage():
	print sys.argv[0] +' -k apikey -b bioprojectid'
	
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


	