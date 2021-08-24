import gzip,time,traceback,requests,os

with open('all_path.txt') as f:
	urls = f.read().split('\n')

for index,url in enumerate(urls):
	if index <= 65:
		continue
	t0 = time.time()
	t1 = t0
	file_name = url.split('/')[-1]
	print("Downloading",file_name)
	r = requests.get('https://s3.amazonaws.com//commoncrawl/' + url, stream = True,timeout=240)
	while True:
		print("Downloading...")
		try:
			data = r.iter_content(chunk_size = 500000)
			with open("file1", "wb") as f:
				for iterate_download,chunk in enumerate(data):
					if t1-t0 > 220:
						raise ValueError
					if chunk:
						f.write(chunk)
					t1 = time.time()
			break
		except (ValueError,requests.Timeout) as e:
			print(e)
			traceback.print_exc()
			t0 = time.time()
			r = requests.get('https://s3.amazonaws.com//commoncrawl/' + url, stream = True,timeout=240)
	with open('texrex.ini',encoding='utf-8') as f:
		job = f.read()
		job = job.replace('namafile',"file1")
		job = job.replace('indexpath',str(index))
		with open('job.ini','w+',encoding='utf-8') as g:
			g.write(job)
	os.system('texrex -j job.ini')
	