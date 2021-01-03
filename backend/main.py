from flask import Flask, render_template, request, jsonify, send_file 
import requests 
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
import numpy as np
import matplotlib.pyplot as plt
import math 
import io
import time
import re
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
import os 

PORT = os.environ["PORT"]

# fix for my computer :(, since the background wasn't working locally for me

plt.rcParams.update({
    "figure.facecolor":  (0.0, 0.0, 0.0, 0.0),  
    "axes.facecolor":    (0.0, 0.0, 0.0, 0.0),  
    "savefig.facecolor": (0.0, 0.0, 0.0, 0.0),  
})



DATA_URL = 'https://cdn-contenu.quebec.ca/cdn-contenu/sante/documents/Problemes_de_sante/covid-19/csv/synthese-7jours-en.csv'

# plt.ioff() #IMPORTANT DO NOT REMOVE
# Reads from api and outputs result
def get_new_data(address):
  r = requests.get(address, allow_redirects=True)
  f = io.TextIOWrapper(io.BytesIO(r.content), encoding='utf8').read()
  data = [[line.split(';')[0],line.split(';')[-1]] for line in f.split("\n")][1:-1]
  return data

# print(get_new_data(DATA_URL))

web_site = Flask(__name__) # server object


@web_site.route('/data.png') # route to the picture that we are sending
def file():
  return send_file('data.png')

@web_site.route('/') # when i get a request
def index():
  fobj = open('vaccine_data.txt', 'r', encoding = 'utf-8')

  dates = []
  totals = []
  for line in fobj:
    split_line_list = line.split('&')
    date_var = split_line_list[0].strip()
    dose_var = int(split_line_list[1].strip())
    dates.append(date_var)
    totals.append(dose_var)
  
  cumulative_doses = 0
  for number in totals:
    cumulative_doses += number
  # data that we want to relay back to the front-end
  data = list()
  data.append(str(cumulative_doses))
  # add the most recent entry 
  data.append(str(totals[-1]))
  # add the date corresponding to the most recent entry 
  data.append(str(dates[-1]))

  to_print = "Cumulative vaccine doses administered: "+data[0]+" doses. Latest dose administered ("+data[2]+"): "+data[1]+" doses."

  # return the cumulative vaccine doses administered to the front-end
  response = jsonify(to_print)
  response.headers.add("Access-Control-Allow-Origin", "*")# has data and headers, one of the header is which type of IPs can request this resource. 
  return response 

def scheduled_update():
  print("scheduled process running")
  # a function to convert the date from MONTH DAY, YEAR to DD/MM
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
        if "and" in date:
          x = date.split(" ")
          x = x[1]+"/"+month+" and "+x[3]+"/"+month
          x = x.replace(",", "")
          return x
        return new_date 

  # since the quebec government only displays data for the 7 most recent
  # days, we need to save them into an external text file. 
  # open the vaccine_data.txt file 
  database = open('vaccine_data.txt', "r+")
  database_read = database.readlines()
  database.close()

  # making the arrays to store the vaccine data
  vaccine_totals = np.array(list()) # this is creating a new empty array (to store the vaccine counts)
  vaccine_dates = list() # this is creating a new list to keep track of the dates 

  # this is the database
  for day in database_read:
    curr_date = day.split("&")[0]
    curr_date = curr_date.strip()
    curr_count = day.split("&")[1]
    # append the current date and count to the existing arrays and lists
    vaccine_totals = np.append(vaccine_totals, int(curr_count))
    vaccine_dates.append(curr_date)


  def process_date(unprocessed_dates):
    processed_dates = list()
    for date in unprocessed_dates:
      new_date = convert_date(date)
      processed_dates.append(new_date)
    return processed_dates

  # this function returns the last index of the database array where the new data is the same
  def last_similar(database_date, new_dates):
    for i, date in reversed(list(enumerate(new_dates))):
      if date != database_date[-1]:
        continue
      else:
        return i
    return 'no similar index'

  # returns list error if no similar index, otherwise concatenates list
  def append_last_similar_dates(database, new, index):
    if index == 'no similar index':
      return 'list error'
    extra = new[index + 1:]
    for item in extra:
      database.append(item)
    return database

  # returns list error if no similar index, otherwise concatenates array
  def append_last_similar_values(array, newlist, index):
    if index == 'no similar index':
      return 'list error'
    extra = newlist[index + 1:]
    for number in extra:
      array = np.append(array, number)
    return array

  # Get the data from the quebec government's web_site
  data = get_new_data(DATA_URL)
  dates = list() 
  doses = np.array(list())

  # populate the dates list
  for entry in data:
    dates.append(entry[0])
    # remove the space between the numbers 
    curr_dose = entry[1]
    curr_dose = re.sub('\s+', '', curr_dose)
    
    doses = np.append(doses, curr_dose)

  # append the new list to the existing data  
  # convert the new dates to the proper format
  new_dates = list(map(convert_date, dates))
  # merge the last_similar doses and dates 
  merged_dates = append_last_similar_dates(vaccine_dates, new_dates, last_similar(vaccine_dates, new_dates))
  # convert the vaccine doses to integers
  vaccine_totals = vaccine_totals.astype(int)
  doses = doses.astype(int)
  merged_totals = append_last_similar_values(vaccine_totals, doses, last_similar(vaccine_totals, doses))


  def write_file(date_bank, value_bank, newfile_name):
    output_fobj = open(newfile_name, 'w', encoding = 'utf-8')
    
    lines_list = list()
    for i in range(len(date_bank)):
      newline = str(date_bank[i]) + ' & ' + str(value_bank[i]) + '\n'
      lines_list.append(newline)
    
    for line in lines_list:
      output_fobj.write(line)
    output_fobj.close()
  
  write_file(merged_dates, merged_totals, 'vaccine_data.txt')



  # a function to plot the data. Takes as input the vaccine dose count, the 
  # dates, and a boolean whether we want to display the plot, and download the plot
  def plot_vaccine(vaccine_totals, dates, download_plot):
    # to get the upper limit of the plot 
    WHITE = '#FFFFFF'
    plt.rc('font', family='sans-serif')
    fig, ax = plt.subplots()
    n = vaccine_totals.max()
    # yticks = np.arange(0, n, 500)
    fig.set_size_inches(6, 3)
    # ax.bar(dates, vaccine_totals, color = '#39ff14')
    ax.bar(dates, vaccine_totals, color = '#39ff14')
    # ax.set_ylim(n) 
    # fig.patch.set_facecolor('#222222')
    ax.tick_params(color='white', labelcolor='white')
    for spine in ax.spines.values():
      spine.set_edgecolor(WHITE)
    ax.xaxis.label.set_color(WHITE)
    ax.yaxis.label.set_color(WHITE)
    ax.set_yscale("linear")
    # ax.set_title("COVID-19 Vaccination Data in Québec", color = WHITE)
    ax.set_xticks(list(map(lambda x : dates[x], range(0,len(dates),5))))
    ax.set_ylabel("Doses administered")
    ax.set_xlabel("Dates")
    # fig.set_facecolor('#222222')
    # ax.set_facecolor('#222222')
    if (download_plot == True):
      plt.savefig("data.png", bbox_inches = 'tight', pad_inches = 0.05, dpi=150)
    plt.close('all')
    return 
    # close the plot
    
  plot_vaccine(merged_totals, merged_dates, True)
  

scheduler = BackgroundScheduler()
scheduler.add_job(scheduled_update,'interval',seconds=30)
scheduler.start()
atexit.register(lambda: scheduler.shutdown(wait=False))



def hello():
  return jsonify("hello").headers.add("Access-Control-Allow-Origin", "*")

# Shut down the scheduler when exiting the app


web_site.run(host='0.0.0.0', port=PORT)

