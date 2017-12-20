import re
import requests
from urllib import request
resp = requests.get(url='http://mp.weixin.qq.com/s/Z6OeRHUfiUyKIV-KG7Eb8w')
regx = "https://mmbiz.qpic.cn/mmbiz_jpg/.*?wx_fmt=jpeg"
pic = re.findall(regx,resp.text)
storePATH  = "/Users/fangdongliang/Desktop/pic/"
count = 0
for item in pic:
	count += 1
	filename = storePATH+str(count)+".jpeg" 
	with request.urlopen(item) as stream:
		pic_stream = stream.read()
	with open(filename,"wb") as outfile:
		outfile.write(pic_stream)
		