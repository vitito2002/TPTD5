# Python program to read
# json file

import json
f = open('data.json')
data = json.load(f)
for i in data['emp_details']:
	print(i)

f.close()

