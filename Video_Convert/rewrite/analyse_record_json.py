import json

with open('record.json') as fp:
    dic = json.load(fp)

r1 = dic['r1']
r2 = dic['r2']

print(len(r1))
print(len(r2))

for frame_num in range(len(r1)):
	if str(frame_num) in r2:
		time = float(r2[str(frame_num)])
		print(frame_num, time-(frame_num-1)/30)
	else:
		print(frame_num, 'break')
