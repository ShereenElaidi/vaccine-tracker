from flask import Flask, render_template, request, jsonify
from random import choice
import requests 
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

web_site = Flask(__name__) # server object



@web_site.route('/') # when i get a request
def index():
	# return render_template('index.html') # return this html file
  requestthing = requests.get("https://www.quebec.ca/en/health/health-issues/a-z/2019-coronavirus/situation-coronavirus-in-quebec/")
  htmltext = requestthing.text
  soup = BeautifulSoup(htmltext, "html.parser") 
  div = soup.find(id="csv-display-synthese-evolution-donnees-en")
  print(div.prettify())
  div2 = div.find("table")
  print(div2.prettify())
  entry = div.find("table").find("tbody").find("tr").find_all("th")[-1]
  response = jsonify() # converts hello world into a json 
  response.headers.add("Access-Control-Allow-Origin", "*")# has data and headers, one of the header is which type of IPs can request this resource. 
  return response 

@web_site.route('/user/', defaults={'username': None})
@web_site.route('/user/<username>')
def generate_user(username):
	if not username:
		username = request.args.get('username')

	if not username:
		return 'Sorry error something, malformed request.'

	return render_template('personal_user.html', user=username)

@web_site.route('/page')
def random_page():
  return render_template('page.html', code=choice(number_list))

web_site.run(host='0.0.0.0', port=8080)



