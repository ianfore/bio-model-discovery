#!/usr/bin/python
import sys
import getopt
import pandas as pd

# Retrieve the attributes of the samples for a specified BioProject and summarize
# the values of those attributes across the project.
# The intent is to provide a report which will help a user
# 1. Identify the data model of the study
# 2. Identify if the project uses a template similar to other studies

 
def DataFrameAttributes(path):


	print ('____________________________________')
	
	print ('Attribute details for file: ' + path)
	
	df = pd.read_csv(path)
	columns = list(df)
		
	# Summarize the attributes for this bioproject
	uniques = []	
	almostUniques = []	
	constants = []	
	singleValue = []	
	
	rowCount = df.shape[0]
	
	print ('No of rows:' + str(rowCount))
	print('____________________________________')
	print(	'The following attributes vary across row.')
	print (	'Some may indicate the dataset design/model.')
	print (	'Some may be sample/subject observations/measurements/data elements.')
	print ()
# 	for aname, att in attDetails.items():
	for c in columns:
		#print('processing:{}'.format(c))
		
		uniqueValueCount = df[c].nunique()
		if uniqueValueCount == rowCount:
			uniques.append(c)
			#att['variability'] = 'u'
		elif 100.0*uniqueValueCount/rowCount > 80.0:
			almostUniques.append(c)
			#att['variability'] = 'au'
		elif uniqueValueCount == 1:
			if df[c].count == rowCount:
				constants.append(c)
				#att['variability'] = 'c'
			else:
				singleValue.append(c)
				#att['variability'] = 's'
		else:
			#att['variability'] = 'v'
			print ('Column:' + c )
			print (df[c].value_counts())
			print ('____________________________________')
		
	if len(uniques):
		print (	'The following attributes have a unique value for each row. ')
		print (	'They are therefore likely to some kind of identifier.')
		for a in uniques:
			print (a)
		print ('____________________________________')
	if len(almostUniques):
		print (	'The following attributes have a unique value for more than 80% of rows.')
		print (	'They are often a subject identifier.')
		for a in almostUniques:
			print (a)
		print ('____________________________________')
	if len(constants):
		print (	'The following have the same value for all samples.')
		print (	'They are likely to be an attribute of the dataset rather than the row')
		for a in constants :
			print (a)
		print ('____________________________________')
	if len(singleValue):
		print (	'The following have only one value in the dataset')
		print (	'but the attribute is not present for all rows')
		for a in singleValue:
			print (a)
		print ('____________________________________')


def usage():
	print (sys.argv[0] +' -f csvfilepath')
	
def main(argv):

	try:
		opts, args = getopt.getopt(argv, "hf:", ["help", "file="])
	except getopt.GetoptError:
		usage()
		sys.exit(2)
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage()
			sys.exit()
		elif opt in ("-f", "--file"):
			filepath = arg

	DataFrameAttributes(filepath)

if __name__ == "__main__":
	main(sys.argv[1:])


	