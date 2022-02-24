# import libraries
import urllib.request
from bs4 import BeautifulSoup
import time
import datetime
import sys
import csv
import requests
import argparse

'''
This program uses the python library BeautifulSoup
To install open command prompt enter: 

pip install beautifulsoup4
pip install lxml
pip install requests

To run in command prompt enter:
python seekjobextract.py

To run with debugging print lines:
python seekjobextract.py --verbose
'''


#Create a job class for holding the job information
class Job:
	def __init__(self, upsql, cntry, title, date_downloaded, date_posted, location, desc):
		self.upsql = upsql
		self.cntry = cntry
		self.title = title
		self.date_downloaded = date_downloaded
		self.date_posted = date_posted
		self.location = location
		self.desc = desc
		
jobs = []

#globals
date_downloaded = datetime.date.today()
cntry = 'UK'
upsql = "No"
title = ''
date_posted = ''
location = ''
desc = ''

#Number of jobs to extract change this to get more jobs
num_jobs = 100
job_counter = 0

#Define the csv file name
FileName = time.strftime("%Y%m%d") + ' job_results_cv-library.csv'

#Debug function for testing
def debug_print(x = ''):
	if args.verbose:
		print(x)

parser = argparse.ArgumentParser(description='Skill scraper')
parser.add_argument('-v', '--verbose', action='store_true')
args = parser.parse_args()	
	
with open(FileName, 'a+', newline='', encoding='utf-8') as f:
	writer = csv.writer(f)
	writer.writerow(['UpdSQL', 'Cntry', 'Title', 'Date Downloaded', 'Date Posted', 'Location', 'Description'])
	
#loop over i amount of pages change this to go through more seek pages
for i in range(1, 20):
	if job_counter >= num_jobs:
		print('num_jobs limit reached, ending script')
		print('Page: {}'.format(i))
		break
		
	#print some new lines and the current page to separate from previous
	debug_print()
	debug_print('page {}'.format(i))
	debug_print()
	
	#loop over the pages to be scraped
	#change this link if you want a different seek page
	
	
	#quote_page = str(sys.argv)
	
	quote_page = 'https://www.cv-library.co.uk/jobs/cyber-security?page={}'.format(i)
	
	#Ensure the page will not return a 404 or 410 error
	request = requests.get(quote_page)
	if request.status_code == 200:
		pass
	else:
		continue
	
	page = urllib.request.urlopen(quote_page)
	#debug_print(page.read())
	#sys.exit(0)


	soup = BeautifulSoup(page, 'html.parser')
	name_box = soup.find('article')
	
	
	#loop over the articles in the page
	for article in soup.find_all('div', class_='jobtitle-divider'):
		#exit after x successes
		#if len(jobs) >= num_jobs:
		if job_counter >= num_jobs:
			break
			
		debug_print('date downloaded: \n')
		debug_print(date_downloaded)
		debug_print()
		
		individual_page = []

		for url in article.find_all('a'):

			individual_page.append(url.get('href'))
		debug_print(individual_page[0])
		
		debug_print('https://www.cv-library.co.uk{}'.format(individual_page[0]))
		individual_page_url = 'https://www.cv-library.co.uk{}'.format(individual_page[0])
		
		#Ensure the page will not return a 404 or 410 error
		request = requests.get(individual_page_url)
		if request.status_code == 200:
			pass
		else:
			continue
		
		new_individual_page = urllib.request.urlopen(individual_page_url)
		new_soup = BeautifulSoup(new_individual_page, 'html.parser')
		new_name_box = soup.find('article')
		
		
		#Get the job description		
		template_descriptions = new_soup.find('div', class_='jd-details jobview-desc')
		if template_descriptions:
			desc = template_descriptions.getText(separator=" ")			
			#Remove the leading whitespace
			desc = desc.lstrip()
			debug_print('Getting Description: \n')
			debug_print(desc)
			debug_print()

		
		#Get the title
		template_title = new_soup.find('div', class_='job-top')
		if template_title:
			title_tag = template_title.find('h1', {'class': 'jobTitle'})
			if title_tag:
				title = title_tag.text
				debug_print('Getting Title: \n')
				debug_print(title)
		
		
		#Get the location
		template_location = new_soup.find('div', class_='job-top')
		if template_title:
			location_tag = template_title.find('div', {"id": "job-location"})
			if location_tag:
				location = location_tag.text
				debug_print('Getting Location: \n')
				debug_print(location)
				
				
		#Get the date posted
		template_date = new_soup.find('div', class_='job-top')
		if template_date:		
			date_tag = template_date.find('div', {"id": "js-posted-details"})
			if date_tag:
				date_posted = date_tag.text
				debug_print(date_posted)
				#Strip unwanted data from text
				date_posted = date_posted.split('(')
				date_posted = date_posted[0].strip()
				date_posted = date_posted.split()
				date_posted = date_posted[0]
				debug_print('printing date_posted')
				debug_print(date_posted)
				debug_print()
	
		with open(FileName, 'a+', newline='', encoding='utf-8') as f:
			writer = csv.writer(f)
			writer.writerow([upsql, cntry, title, date_downloaded, date_posted, location, desc])
		
		job_counter += 1	
		jobs.append(Job(upsql, cntry, title, date_downloaded, date_posted, location, desc))
			

'''
	file = open('filename.csv', 'a')
	file.write('{}, {}, {}, {}, {}\n'.format(title,date_downloaded,date_posted,location,desc))
'''		
	#sleep to look less like a bot
	#time.sleep(3)
		
'''
FileName = time.strftime("%Y%m%d") + ' job_results_cv-library.csv'
#FileName = 'job_results_seek_au.csv'
#FileName = 'job_results_seek.csv'
		
#Write the job class to csv
with open(FileName, 'a+', newline='', encoding='utf-8') as f:

	writer = csv.writer(f)
	writer.writerow(['UpdSQL', 'Cntry', 'Title', 'Date Downloaded', 'Date Posted', 'Location', 'Description'])
		
	for job in jobs:
	
		writer.writerow([job.upsql, job.cntry, job.title, job.date_downloaded, job.date_posted, job.location, job.desc])

'''