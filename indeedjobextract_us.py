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
python indeedjobextract.py

To run with debugging print lines:
python indeedjobextract.py --verbose
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
cntry = 'US'
upsql = "No"
title = ''
date_posted = ''
location = ''
desc = ''

#Number of jobs to extract change this to get more jobs
num_jobs = 100
job_counter = 0

#Define the csv file name
FileName = time.strftime("%Y%m%d") + ' job_results_indeed.csv'

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

#loop over i amount of pages change this to go through more indeed pages
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
	#change this link if you want a different indeed page
	#quote_page = str(sys.argv)
	quote_page = 'https://www.indeed.com/jobs?q=security+analyst&l=Brisbane%2C+CA&start={}'.format(i)
	
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
	name_box = soup.find('h2')
	
	print('h2')
	
	#loop over the articles in the page
	for article in soup.find_all('h2'):
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
		debug_print(individual_page[0])
		debug_print('end')
		
		debug_print('https://www.indeed.com/{}'.format(individual_page[0]))
		individual_page_url = ('https://www.indeed.com/{}'.format(individual_page[0]))
		
		#Ensure the page will not return a 404 or 410 error
		request = requests.get(individual_page_url)
		if request.status_code == 200:
			pass
		else:
			continue
		
		new_individual_page = urllib.request.urlopen(individual_page_url)
		new_soup = BeautifulSoup(new_individual_page, 'html.parser')
		new_name_box = soup.find('article')
		
		#Get the job title
		template_title = new_soup.find('h3')
		if template_title:
			item_title = template_title.text
			title = item_title.split('- ')
			debug_print('Getting title: \n')
			debug_print(title[0])	
			debug_print()
			
		
		#Get the job location
		template_title = new_soup.find('title')
		if template_title:
			beforesplit_location = template_title.text
			location = beforesplit_location.split('- ')
			debug_print('Getting location: \n')
			debug_print(location[1])	
			debug_print()		
					
					
		#Get the job description		
		template_descriptions = new_soup.find_all('div', class_='jobsearch-JobComponent-description icl-u-xs-mt--md')
		if template_descriptions:
			desc = template_descriptions[0].getText(separator=" ")		
			debug_print()
			debug_print('Getting Description: \n')
			debug_print(desc)
			debug_print()
		
		
		#NOTE: Doesnt show exact date. Goes up to 30 days then just says 30+ days ago.
		#Get the date posted
		template_date = new_soup.find(class_='jobsearch-JobMetadataFooter')
		if template_date:
		
			#Get how old the article is in days
			#Split off the unwanted text and characters
			days_ago_array = template_date.text.split('- ')
			
			days_ago = days_ago_array[1]
			debug_print('printing days ago')
			debug_print(days_ago)
			
			days_ago = days_ago.split()
			
			if days_ago[1] == 'months':
				days_ago[0] = '30'
			
			if days_ago[1] == 'hours':
				days_ago[0] = '0'
			
			if days_ago[0] == 'save':
				days_ago[0] = '0'
			
			days_ago = days_ago[0].split('+')
			
			debug_print('printing days ago')
			debug_print(days_ago[0])
			

			#Convert days_ago to an actual date			
			date_posted = date_downloaded - datetime.timedelta(days=int(days_ago[0]))
			debug_print('printing date posted')
			debug_print(date_posted)
			debug_print()
							
		with open(FileName, 'a+', newline='', encoding='utf-8') as f:
			writer = csv.writer(f)
			writer.writerow([upsql, cntry, title, date_downloaded, date_posted, location, desc])
		
		job_counter += 1
		jobs.append(Job(upsql, cntry, title[0], date_downloaded, date_posted, location[1], desc))

'''
	file = open('filename.csv', 'a')
	file.write('{}, {}, {}, {}, {}\n'.format(title,date_downloaded,date_posted,location,desc))
'''		
	#sleep to look less like a bot
	#time.sleep(3)
		
'''
FileName = time.strftime("%Y%m%d") + ' job_results_indeed.csv'
#FileName = 'job_results_indeed_au.csv'
#FileName = 'job_results_indeed.csv'
		
#Write the job class to csv
with open(FileName, 'a+', newline='', encoding='utf-8') as f:

	writer = csv.writer(f)
	writer.writerow(['UpdSQL', 'Cntry', 'Title', 'Date Downloaded', 'Date Posted', 'Location', 'Description'])
		
	for job in jobs:

		writer.writerow([job.upsql, job.cntry, job.title, job.date_downloaded, job.date_posted, job.location, job.desc])

'''