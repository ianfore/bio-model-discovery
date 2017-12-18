import json


importers = {'El Salvador' : 1234,
             'Nicaragua' : 152,
             'Spain' : 252
            }

exporters = {'Spain' : 252,
             'Germany' : 251,
             'Italy' : 1563
             }

#print importers.keys() & exporters.keys()
print "Intersects:", filter(importers.has_key, exporters.keys())

# with open('templates.json') as json_file:  
#     data = json.load(json_file)
# 
#     t1 = data['template1']
#     t2 = data['template2']
#     print t1 & t2
