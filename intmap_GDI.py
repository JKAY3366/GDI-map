#!/usr/bin/env python
# coding: utf-8

# In[2]:


import json
import bokeh

import geopandas as gpd
import pandas as pd

from bokeh.io import output_notebook, show, output_file, curdoc
from bokeh.plotting import figure
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar, Slider, HoverTool
from bokeh.palettes import brewer
from bokeh.layouts import widgetbox, row, column


# In[3]:


import requests
import io
    
# Downloading the csv file from your GitHub account

url2 = "https://raw.githubusercontent.com/JKAY3366/TrialMap/main/modified-GDI.csv" # Make sure the url is the raw version of the file on GitHub
downloads = requests.get(url2).content

# Reading the downloaded content and turning it into a pandas dataframe

new_file2 = pd.read_csv(io.StringIO(downloads.decode('utf-8')))
new_file2.head


# In[5]:


states = gpd.read_file("india.geojson")
states


# In[11]:


#Define function that returns json_data for year selected by user.
    
def json_dat(selectedYear):
    year = selectedYear
    df_year = new_file2[new_file2['Year'] == year]
    mergedd = states.merge(df_year, on='NAME_1')
    mergedd_json = json.loads(mergedd.to_json())
    json_dat = json.dumps(mergedd_json)
    return json_dat
#Input GeoJSON source that contains features for plotting.
geosource = GeoJSONDataSource(geojson = json_dat(2018))
#Define a sequential multi-hue color palette.
palet = brewer['RdPu'][8]
#Reverse color order so that dark blue is highest obesity.
palet = palet[::-1]
#Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors.
color_map = LinearColorMapper(palette = palet, low = 0.5, high = 1)
#Define custom tick labels for color bar.
tick_labels = {'0': '0', '0.4': '0.4', '0.5':'0.5', '0.6':'0.6', '0.7':'0.7', '0.8':'0.8', '0.9':'0.9','1':'1'}
#Add hover tool
hover = HoverTool(tooltips = [ ('State','@NAME_1'),('GDI', '@GDI')])
#Create color bar. 
color_bar = ColorBar(color_mapper=color_map, label_standoff=8,width = 500, height = 20,
                     border_line_color=None,location = (0,0), orientation = 'horizontal', major_label_overrides = tick_labels)
#Create figure object.
q = figure(title = 'GDI of Indian States, 2018', plot_height = 600 , plot_width = 600, toolbar_location = None, tools = [hover])
q.xgrid.grid_line_color = None
q.ygrid.grid_line_color = None
#Add patch renderer to figure. 
q.patches('xs','ys', source = geosource,fill_color = {'field' :'GDI', 'transform' : color_map},
          line_color = 'black', line_width = 0.25, fill_alpha = 1)
#Specify layout
q.add_layout(color_bar, 'below')
# Define the callback function: update_plot
def update_plo(attr, old, new):
    year = slider.value
    new_data2 = json_dat(year)
    geosource.geojson = new_data2
    q.title.text = 'GDI of Indian States, %d' %year
    
# Make a slider object: slider 
slider = Slider(title = 'Year',start = 2000, end = 2018, step = 1, value = 2018)
slider.on_change('value', update_plo)
# Make a column layout of widgetbox(slider) and plot, and add it to the current document
layout = column(q,bokeh.models.Column(slider))
curdoc().add_root(layout)
#Display plot inline in Jupyter notebook
output_notebook()
#Display plot
show(layout)


# Note that the slider in the jupyter output will not work. We need to create a local server to view the interactive map.
# To create a local server and view the interactive map:<br>
# Open Anaconca Prompt.<br>
# Change the working directory to current working directory.<br>
# Type the following command:<br> 
# `bokeh serve --show intmap-GDI.ipynb`
