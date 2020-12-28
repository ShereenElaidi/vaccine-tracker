from flask import Flask, render_template, request, jsonify
from random import choice
import requests 
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import numpy as np
import unidecode
import matplotlib.pyplot as plt
import math 

# get ready for some PRETTY code
def convert_date(date):
	date = date.lower()
	# split the string
	new_date=""
	month=""
	date_1 = date.split(",")[0]
	date_2 = date_1.split(" ")[1]
	months=["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
	for i, x in zip(range(0, 12), months):
		if x in date:
			month = str(i+1); 
			new_date=date_2+"/"+str(i+1)
			if "ana" in date:
				print(month)
				x = date.split(" ")
				x = month+"/"+x[1]+" & "+month+"/"+x[3]
				x = x.replace(",", "")
				print(x)
				return x
			return new_date 		
	# check of ana is in the string thx quebec government December 24 aNA 25, 2020



# path to chromedriver: 
option = webdriver.ChromeOptions()
option.add_argument(" -- incognito")
option.add_argument('--headless')
browser = webdriver.Chrome(executable_path='/Users/shereenelaidi/Desktop/webdev/vaccine-tracker/VaccineTrackerBackend/chromedriver', options=option)
browser.get("https://www.quebec.ca/en/health/health-issues/a-z/2019-coronavirus/situation-coronavirus-in-quebec/")
requestthing = browser.page_source #obtain the HTML source code
  # print out the HTML source code
  # browser.quit()
	# # return render_template('index.html') # return this html file
 #  requestthing = requests.get("https://www.quebec.ca/en/health/health-issues/a-z/2019-coronavirus/situation-coronavirus-in-quebec/")

soup = BeautifulSoup(requestthing, "html.parser") 
div = soup.find(id="csv-display-synthese-evolution-donnees-en")
div2 = div.find("table")
entry1 = div2.find("tbody")
entry2 = entry1.findAll("tr")
vaccine_totals = np.array([0])
vaccine_dates = ["December 19, 2020"]
# now iterate through all of the elements of entry2 and save them into a list
for day in entry2:
	# extract the row for the current day
	day_data = day.findAll("td")
	# extract the last column of the day which has the vaccine data
	today_vax = day_data[-1]
	today_date = day_data[0]
	# extract the text from the HTML element
	total = today_vax.text
	day = today_date.text
	# checking if \xa0 is in the string 
	total = unidecode.unidecode(total)
	total = total.replace(" ", "")

	int_total = int(total)
	day = str(day)

	# add this to the running total of vaccine counts
	vaccine_totals = np.append(vaccine_totals, int_total)
	vaccine_dates.append(day)

print(vaccine_totals)
vaccine_totals = vaccine_totals.astype(int)
print(vaccine_totals)

# convert_date("December 24 aNA 25, 2020")


new_dates = list(map(convert_date, vaccine_dates))
print(new_dates)
# ax = fig.add_axes([0,0,1,1])
n = vaccine_totals.max() # biggest size of the chart 
yticks = np.arange(0, n, 500)
total = vaccine_totals
plt.bar(new_dates, total)
plt.ylim = n
plt.yscale = "linear"
plt.title("COVID-19 Vaccination Data in Quebec")
plt.ylabel("Doses administered")
plt.xlabel("Dates")
plt.show()
# show the plot






