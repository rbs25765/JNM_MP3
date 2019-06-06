import requests
from bs4 import BeautifulSoup
import os
import datetime
from clint.textui import progress
import sys


class WebScrapingM:

	def __init__(self):
		self.base_url = 'http://www.srinannagaru.com'
		self.sub_url = 'http://www.srinannagaru.com/snaudios.php'
		self.num = 1

	def url_generator(self):

		resp = requests.get(self.sub_url)
		resp = resp.content
		return resp

	def soup_generator(self):

		soup_url = self.url_generator()
		soup_out = BeautifulSoup(soup_url, 'lxml')
		return soup_out

	def url_extractor(self, year):

		soup = self.soup_generator()
		link_list = [link['href'] for link in soup.find_all('a') if link['href'].endswith('.mp3')]
		year_link_list = [self.base_url + link for link in link_list if str(year) in link]

		return year_link_list

	def file_extract(self, fpath, url_list, no=2):
		final_start_time = datetime.datetime.now()
		for link in url_list:
			if self.num <= no and self.num <= len(url_list):
				start_time = datetime.datetime.now()
				filename = link.split('/')[-1]
				outfile = '{}/{}'.format(fpath,filename)
				if not os.path.exists(outfile):
					print("Downloading {} from {}".format(filename, link))
					r = requests.get(link, stream=True)
					with open(outfile, 'wb') as f:
						total_length = int(r.headers.get('content-length'))
						print("File Size  is {0:.2f} MB".format(total_length/(1024*1024)))
						f.write(next(r.iter_content(chunk_size=1024*1024)))
						for chunk in progress.bar(r.iter_content(chunk_size=1024*1024), expected_size=(total_length/(1024*1024)+1)):
							f.write(chunk)
							f.flush()
					end_time = datetime.datetime.now()
					print("{} Download Completed in {} ".format(filename, (end_time-start_time)))
					self.num += 1
				else:
					# print("{} exists, Hence trying next file".format(filename))
					self.num = 1
			else:
				break
		final_end_time = datetime.datetime.now()
		print("Total no of Files downloaded = {} in {}".format(self.num-1, (final_end_time-final_start_time)))

		return


if __name__ == '__main__':
	wsm = WebScrapingM()
	year = int(input("Enter Year to download: "))
	if not os.path.exists('./Output/'+str(year)):
		os.mkdir('./Output/'+str(year))
	urllist = wsm.url_extractor(year)
	print("Total Number of files in {} are {}".format(year, len(urllist)))
	number_of_files = int(input("Enter Number of files to download: "))
	out_path = '{}/{}'.format('./Output', year)
	wsm.file_extract(out_path, urllist, number_of_files)
	input("press Enter to exit")
	sys.exit()
