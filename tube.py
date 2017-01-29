"""Tube.py : This program analyses a number of entries to the London's tube stations 
             chosen by user. It then creates a bar plot and pie charts comparing the 
             entries to our stations on a weekday, Saturday and Sunday.
             The data is from London Datastore and it contains information from 2014"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def main():
    print('This program is based on data from 2014 collected from London Datastore.'\
          'You can choose a number of stations to see and compare how many entries'\
          'to the stations have been on a weekday, Saturday and Sunday.')
    #import the excel file with our data as pandas dataframe and read first sheet
    xls_file = pd.read_excel('tube02.xls',sheetname = '2014 Entry & Exit')
    #get the first column as a list we can loop through  
    station_list = xls_file.iloc[:,0]   
    stations = choose_stations(station_list)
    weekday, saturday, sunday = extract_data(stations, xls_file) 
    make_bar_plot(stations, xls_file, weekday, saturday, sunday)
    make_pie_chart(stations, xls_file, weekday, 'Weekday')
    make_pie_chart(stations, xls_file, saturday, 'Saturday')
    make_pie_chart(stations, xls_file, sunday, 'Sunday')

def make_pie_chart(stations, data, what_day, title):
    """make a pie chart with our stations and corresponding data"""
    fig = plt.figure(figsize=[10,10])
    ax = fig.add_subplot(111)
    what_day = sorted(what_day)            #sort what_day
    cmap = plt.cm.prism                    #choose a colourmap for our pie chart   
    colors = cmap(np.linspace(0., 1., len(what_day)))  #attach colours to what_day
    pie_chart = ax.pie(what_day, labels=stations, shadow=True, colors=colors,
                       startangle=160, labeldistance=1.05, autopct='%1.1f%%')
    for pie_wedge in pie_chart[0]:         #set the edges of each pie slice to white
        pie_wedge.set_edgecolor('white')       
    ax.set_title(title, fontsize = 20, bbox={'facecolor':'0.9'})
    ax.axis('equal')                       #view the plot drop above
    plt.show()
       
def make_bar_plot(stations, data, weekday, saturday, sunday):
    """make a bar plot with our stations and corresponding data"""
    N = len(stations)                 #check how many stations the user chose
    fig = plt.figure(figsize=[N,10])  #adjust the width of the plot to it
    ax = fig.add_subplot(111) 
    ind = np.arange(N)                #the x locations for the stations
    width = 0.25                      # the width of the bars
    #create and label bars
    rects1 = ax.bar(ind, weekday, width, color='red', label = 'Weekday')
    rects2 = ax.bar(ind+width, saturday, width, color='blue', label = 'Saturday')
    rects3 = ax.bar(ind+width+width, sunday, width, color='green', label = 'Sunday')
    #set names of the labels and a title
    ax.set_xlim(-width,len(ind))
    ax.set_ylim(bottom = 0)
    ax.set_ylabel('Entries to the stations')
    ax.set_xticks(ind+width+(width/2))
    xtick_names = ax.set_xticklabels(stations)
    plt.setp(xtick_names, rotation=90, fontsize=10)
    #put a legend on top
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15),
          ncol=3, fancybox=True, shadow=True)
    plt.show()        
 
def extract_data (stations, data):
    """get data from out dataframe regarding entries on particur day of the week"""
    weekday = []
    saturday = []
    sunday = []
    for station in stations:
        station = station.strip()
        station_list = data.iloc[:,0]                #first column of our file
        #get indexes in the file where the chosen stations are
        ind = data[station_list.str.contains("^{}$".format(station))].index.get_values()
        weekday.append(data.ix[ind,2].get_values())  #get data from the third column
        saturday.append(data.ix[ind,3].get_values()) #get data from the fourth column
        sunday.append(data.ix[ind,4].get_values())   #get data from the fifth column
    return weekday, saturday, sunday
    
def choose_stations(station_list):
    """Read names of the stations entered by the user and check if they exist"""
    source = input('Enter the list of stations you would like to compare,'\
                   'seperated by comma:\n')
    stations = source.split(",")
    data = []
    for station in stations:
        station = station.strip()
        #tell user to enter the station again if it is not in our dataframe
        while not station_list.str.contains("^{}$".format(station)).any():
            print("Station {} doesn't exist.".format(station))
            station = input("Enter it again: ")
        data.append(station)        
    return data

main()