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

To run in command prompt enter:
python seekjobextract.py

To run with debugging print lines:
python seekjobextract.py --verbose
'''


#Create a job class for holding the job information
class Job:
	def __init__(self, updsql, cntry, title, date_downloaded, date_posted, location, desc):
		self.updsql = updsql
		self.cntry = cntry
		self.title = title
		self.date_downloaded = date_downloaded
		self.date_posted = date_posted
		self.location = location
		self.desc = desc
		
jobs = []

#globals
date_downloaded = datetime.date.today()
cntry = 'NZ'
updsql = 'No'
title = ''
date_posted = ''
location = ''
desc = ''

#Number of jobs to extract change this to get more jobs
num_jobs = 100
job_counter = 0

#Define the csv file name
FileName = time.strftime("%Y%m%d") + ' job_results_seek.csv'

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
for i in range(1, 10):
	if job_counter >= num_jobs:
		print('num_jobs limit reached, ending script')
		print('Page: {}'.format(i))
		break
		
	#print some new lines and the current page to separate from previous
	debug_print()
	debug_print('page {}'.format(i))
	debug_print()
	
	#quote_page = str(sys.argv) - Pass parametrs
	
	#loop over the pages to be scraped
	#change this link if you want a different seek page
	quote_page = 'https://www.seek.com.au/jobs-in-information-communication-technology/in-All-New-Zealand-NZ?daterange=999&keywords=%22Security%22%20or%20%22Forensic%22%20or%20%22cyber%22%20or%20%22Analyst%22&page={}'.format(i)	
		
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
	for article in soup.find_all('article'):
		#exit after x successes
		#if len(jobs) >= num_jobs:
		if job_counter >= num_jobs:
			break
		#name = article.text.strip() # strip() is used to remove starting and trailing
				
		debug_print('date downloaded: \n')
		debug_print(date_downloaded)
		debug_print()
		
		individual_page = []

		for url in article.find_all('a'):

			individual_page.append(url.get('href'))
		#debug_print(individual_page[0])
		#debug_print('end')
		
		#debug_print('https://www.seek.com.au{}'.format(individual_page[0]))
		individual_page_url = 'https://www.seek.com.au/{}'.format(individual_page[0])
		
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
		template_descriptions = new_soup.find_all('div', class_='templatetext')
		if template_descriptions:
			desc = template_descriptions[0].getText(separator=" ")
			debug_print()
			debug_print('Getting Description: \n')
			debug_print(desc)
			debug_print()

	
		#Get the job title
		template_title = new_soup.find('h1', class_='jobtitle')
		if template_title:
			temp_title = template_title.text
			title = temp_title.split(' Job')
			title = title[0].split("'")
			title = title[0]
			debug_print('Getting title: \n')
			debug_print(title)
			debug_print()
			
			
		#Get the date posted and Location
		template_date_location = new_soup.find_all('dd')
		if template_date_location:
			date_posted = template_date_location[0].text
				
			#Convert date posted to datetime and then back to usable string
			date_posted = time.strptime(date_posted, "%d %b %Y")
			date_posted = time.strftime('%Y-%m-%dT%H:%M:%SZ', date_posted)
			debug_print(date_posted)

			#split off unwanted time data
			date_posted = date_posted.split('T')	
			date_posted = date_posted[0].split('-')
			
			#Find the day, month and year
			day = date_posted[2]
			month = date_posted[1]
			year = date_posted[0]

			date_posted = day+'/'+month+'/'+year
			debug_print(date_posted)
			
			location = template_date_location[1].text
			
			debug_print('Getting date posted: \n')
			debug_print(date_posted)
			debug_print()
		
			debug_print('Getting location: \n')
			debug_print(location)
			debug_print()
			
		with open(FileName, 'a+', newline='', encoding='utf-8') as f:
			writer = csv.writer(f)
			writer.writerow([updsql, cntry, title, date_downloaded, date_posted, location, desc])
		
		job_counter += 1
		#jobs.append(Job(updsql, cntry, title, date_downloaded, date_posted, location, desc))
			

'''
	file = open('filename.csv', 'a')
	file.write('{}, {}, {}, {}, {}\n'.format(title,date_downloaded,date_posted,location,desc))
'''		
	#sleep to look less like a bot
	#time.sleep(3)

'''	
FileName = time.strftime("%Y%m%d") + ' job_results_seek.csv'
#FileName = 'job_results_seek_nz.csv'
#FileName = 'job_results_seek.csv'

#Write the job class to csv
with open(FileName, 'a+', newline='', encoding='utf-8') as f:

	writer = csv.writer(f)
	writer.writerow(['UpdSQL', 'Cntry', 'Title', 'Date Downloaded', 'Date Posted', 'Location', 'Description'])
		
	for job in jobs:
	
		writer.writerow([job.updsql, job.cntry, job.title, job.date_downloaded, job.date_posted, job.location, job.desc])
'''
