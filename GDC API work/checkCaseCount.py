import requests
import json

file_endpt = 'https://api.gdc.cancer.gov/files/'
headers = {'Content-Type': 'application/json'}
chunkSize = 1000
fromBase = 0
pagesRetrieved = 0
totalPages = 4
multiCount = 0
filetypes = {}
datatypes = {}

print ("file type\tfile name\tfile id\tcases")

while pagesRetrieved < totalPages:

# data_categorys
# Transcriptome Profiling
# Clinical
# Biospecimen
# Raw Sequencing Data
# Simple Nucleotide Variation
# Copy Number Variation
# DNA Methylation

	body = {
		"filters":{
					"op":"=",
					"content":{
						"field":"data_category",
						"value":"Biospecimen"
					}
			
		},
		"fields":"cases.case_id,file_name,data_format,data_type",
		"format":"json",
		"sort":"file_name",
		"from":fromBase,
		"size":chunkSize
	}

	#print ("retrieving from %d" % fromBase)
	r = requests.post(file_endpt, data=json.dumps(body), headers=headers)
	# print (json.dumps(r.json(), indent=2))
	b = r.json()
	d = b['data']
	p = d['pagination']
	#print (p)
	totalPages = p['pages']
	h = d['hits']

	for i in h :
		if i['data_format'] in filetypes:
			filetypes[i['data_format']] += 1
		else:
			filetypes[i['data_format']] = 1
			
		if i['data_type'] in datatypes:
			datatypes[i['data_type']] += 1
		else:
			datatypes[i['data_type']] = 1
			
		cl = i['cases']
		if len(cl) > 1:
			print (i['data_format'] + "\t" + i['file_name']+"\t"+ i['id'] + "\t" + str(len(cl)))
			multiCount += 1
			
	pagesRetrieved += 1
	fromBase += chunkSize
	print("retrieved %d of %d pages\n" % (pagesRetrieved,totalPages))	

print (str(multiCount) + " files apply to more than one case")
print ("Total hits: " + str(p['total']))

print ("\nFile types")
for type, count in filetypes.items():
    print('{} {}'.format(type, count))

print ("\nData types")	
for type, count in datatypes.items():
    print('{} {}'.format(type, count))
	



