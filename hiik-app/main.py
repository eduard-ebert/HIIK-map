# Heidelberg Institute of International Conflict Research
# Bergheim Street 58
# 69115 Heidelberg
# Germany
# Developer: Eduard Ebert
# Contact: ebert@hiik.de

###                ###
### Import section ###
###                ###

import json
import bokeh.settings
import pandas as pd
import geopandas as gpd
import numpy as np

from bokeh.io import show
from bokeh.io.doc import curdoc
from bokeh.models import (Tabs, Panel, Slider, CDSView, ColorBar, ColumnDataSource, CustomJS, CustomJSFilter, GeoJSONDataSource, HoverTool, LinearColorMapper, Slider, Legend, LegendItem)
from bokeh.layouts import column, row, widgetbox
from bokeh.palettes import brewer
from bokeh.plotting import output_file, show, figure
from bokeh.embed import file_html, components
from bokeh.resources import CDN

###                ###
###   Global map   ###
###                ###

# Define paths to data and maps as variables
shp_global = "http://raw.githubusercontent.com/eduard-ebert/HIIK-map/master/hiik-app/maps/global.json"
data_global = "http://raw.githubusercontent.com/eduard-ebert/HIIK-map/master/hiik-app/data/global.xlsx"

# Read shapefile
shp_gdf_global = gpd.read_file(shp_global)[["NAME_0", "GID_0", "HASC_0", "geometry"]]

# Filter data for missing values
shp_gdf_global = shp_gdf_global[~shp_gdf_global["geometry"].isnull()]

# Read spreadsheet
df_global = pd.read_excel(data_global,
                          names = ["GID_0", "Country_0", "TIME_0", "TIME_STRING", "HASC_0", "INTENSITY_0"],
                          skiprows = 1)

# Filter data for year 2019
df_2019_global = df_global[df_global["TIME_0"] == 0]

# Merge dataframes for the year 2019
merged_global = shp_gdf_global.merge(df_2019_global, left_on = "HASC_0",
                                     right_on = "HASC_0", how = "left")

merged_global_json = json.loads(merged_global.to_json())

json_data_global = json.dumps(merged_global_json)

# Define function json_data
def json_data_global(selectedYear_global):
    yr_global = selectedYear_global
    df_yr_global = df_global[df_global["TIME_0"] == yr_global]
    merged_global = shp_gdf_global.merge(df_yr_global, left_on = "HASC_0", right_on = "HASC_0", how = "left")
    merged_global_json = json.loads(merged_global.to_json())
    json_data_global = json.dumps(merged_global_json)
    return json_data_global

# Input GeoJSON source that contains features for plotting
geosource_global = GeoJSONDataSource(geojson = json_data_global(0))

# Define color palettes with HIIK colors and instantiate color mappers
hiik_colors = ["#f6f6f6", "#badaef", "#67bff1",
               "#2099d0","#006aa8", "#000116"]

color_mapper = LinearColorMapper(palette = hiik_colors, low = 0, high = 5, nan_color = "#d9d9d9")

def make_plot_global():
    # Create the global map
    p_global = figure(title = "Conflicts on a national level in 2019",
                    plot_height = 450, plot_width = 713,
                    toolbar_location = "below",
                    tools = "pan, wheel_zoom, box_zoom, reset")

    p_global.xgrid.grid_line_color = None
    p_global.ygrid.grid_line_color = None
    p_global.axis.visible = False

    # Legend
    x = 1
    y = 1
    p_global.square(x, y, legend_label = "No Dispute", fill_color = "#f6f6f6", line_color = None)
    p_global.square(x, y, legend_label = "Dispute", fill_color = "#badaef", line_color = None)
    p_global.square(x, y, legend_label = "Non-violent crisis", fill_color = "#67bff1", line_color = None)
    p_global.square(x, y, legend_label = "Violent crisis", fill_color = "#2099d0", line_color = None)
    p_global.square(x, y, legend_label = "Limited war", fill_color = "#006aa8", line_color = None)
    p_global.square(x, y, legend_label = "War", fill_color = "#000116", line_color = None)
    p_global.legend.location = "bottom_left"

    # Add patch renderer to figure.
    states = p_global.patches("xs", "ys", source = geosource_global,
                    fill_color = {"field" : "INTENSITY_0",
                                    "transform" : color_mapper},
                    line_color = "gray", line_width = 0.25, fill_alpha = 1)

    # Create hover tool
    p_global.add_tools(HoverTool(renderers = [states], tooltips = [("Country", "@NAME_0"),
                                                                ("Intensity", "@INTENSITY_0"),
                                                                ("Time", "@TIME_STRING")]))
    return p_global

# Define the callback function: update_plot
def update_plot_global(attr, old, new):
    yr_global = slider_global.value
    new_data_global = json_data_global(yr_global)       
    geosource_global.geojson = new_data_global 
    curdoc().clear()
    curdoc().add_root(layout)

# Define the slider object
slider_global = Slider(title = "Time", start = 0,
                       end = 12, step = 1, value = 0)

slider_global.on_change("value", update_plot_global)

###                ###
###  Regional map  ###
###                ###

# Define paths to data and maps as variables
shp_subnational = "http://raw.githubusercontent.com/eduard-ebert/HIIK-map/master/hiik-app/maps/subnational.json"
data_subnational = "http://raw.githubusercontent.com/eduard-ebert/HIIK-map/master/hiik-app/data/subnational.xlsx"

# Read shapefile
shp_gdf_subnational = gpd.read_file(shp_subnational)[["GID_0", "NAME_0", "GID_1", "NAME_1", "NL_NAME_1", "VARNAME_1", "TYPE_1", "ENGTYPE_1", "CC_1", "HASC_1", "geometry"]]
shp_gdf_subnational = shp_gdf_subnational[~shp_gdf_subnational["geometry"].isnull()]
shp_gdf_subnational = shp_gdf_subnational[~shp_gdf_subnational["HASC_1"].isnull()]

# Read spreadsheet
df_subnational = pd.read_excel(data_subnational, names = ["GID_1", "Country_1",
                                                          "Region", "HASC_1",
                                                          "TIME_1", "TIME_STRING",
                                                          "INTENSITY_1"], skiprows = 1)

df_subnational = df_subnational[~df_subnational["HASC_1"].isnull()]

# Filter data for year 2019
df_subnational_2019 = df_subnational[df_subnational["TIME_1"] == 0]

# Merge dataframes world_map and df for the year 2018
merged_subnational = shp_gdf_subnational.merge(df_subnational_2019, left_on = "HASC_1",
                                               right_on = "HASC_1", how = "inner")

# Input GeoJSON source that contains features for plotting
merged_json_subnational = json.loads(merged_subnational.to_json())

json_data_subnational = json.dumps(merged_json_subnational)

# Define function json_data
def json_data_subnational(selectedYear_subnational):
    yr_subnational = selectedYear_subnational
    df_yr_subnational = df_subnational[df_subnational["TIME_1"] == yr_subnational]
    merged_subnational = shp_gdf_subnational.merge(df_yr_subnational, left_on = "HASC_1", right_on = "HASC_1", how = "inner")
    merged_json_subnational = json.loads(merged_subnational.to_json())
    json_data_subnational = json.dumps(merged_json_subnational)
    return json_data_subnational

# Input GeoJSON source that contains features for plotting
geosource_subnational = GeoJSONDataSource(geojson = json_data_subnational(0))

# Define color palettes with HIIK colors and instantiate color mappers
hiik_colors = ["#f6f6f6", "#badaef", "#67bff1",
               "#2099d0","#006aa8", "#000116"]

color_mapper = LinearColorMapper(palette = hiik_colors, low = 0, high = 5, nan_color = "#d9d9d9")

def make_plot_subnational():
    # Create subnational map
    p_subnational = figure(title = "Conflicts on a subnational level in 2019",
                        plot_height = 450, plot_width = 713,
                        toolbar_location = "below",
                        tools = "pan, wheel_zoom, box_zoom, reset")

    p_subnational.xgrid.grid_line_color = None
    p_subnational.ygrid.grid_line_color = None
    p_subnational.axis.visible = False

    # Legend
    x = 1
    y = 1

    p_subnational.square(x, y, legend_label = "No Dispute", fill_color = "#f6f6f6", line_color = None)
    p_subnational.square(x, y, legend_label = "Dispute", fill_color = "#badaef", line_color = None)
    p_subnational.square(x, y, legend_label = "Non-violent crisis", fill_color = "#67bff1", line_color = None)
    p_subnational.square(x, y, legend_label = "Violent crisis", fill_color = "#2099d0", line_color = None)
    p_subnational.square(x, y, legend_label = "Limited war", fill_color = "#006aa8", line_color = None)
    p_subnational.square(x, y, legend_label = "War", fill_color = "#000116", line_color = None)
    p_subnational.legend.location = "bottom_left"

    # Add patch renderer to figure.
    regions = p_subnational.patches("xs","ys", source = geosource_subnational,
                                    fill_color = {"field": "INTENSITY_1",
                                                "transform": color_mapper},
                                    line_color = "gray", line_width = 0.25, fill_alpha = 1)

    # Create hover tool
    p_subnational.add_tools(HoverTool(renderers = [regions], tooltips = [("Country", "@Country_1"),
                                                                        ("Region", "@Region"),
                                                                        ("Intensity", "@INTENSITY_1"),
                                                                        ("Time", "@TIME_STRING")]))
    return p_subnational

# Define the callback function: update_plot
def update_plot_subnational(attr, old, new):
    yr_subnational = slider_subnational.value
    new_data_subnational = json_data_subnational(yr_subnational)       
    geosource_subnational.geojson = new_data_subnational
    curdoc().clear()
    curdoc().add_root(layout)

# Define the slider object
slider_subnational = Slider(title = "Time", start = 0,
                            end = 12, step = 1, value = 0)

slider_subnational.on_change("value", update_plot_subnational)

###                ###
### Make the plots ###
###                ###

# Call the plotting functions
plot_global = make_plot_global()
plot_subnational = make_plot_subnational()

# Make a colum layout and plot (global)
layout_global = column(plot_global, widgetbox(slider_global))

# First tab
tab_global = Panel(child=layout_global, title = "National and international level")

# Make a colum layout and plot (subnational)
layout_subnational = column(plot_subnational, widgetbox(slider_subnational))

# Second tab
tab_subnational = Panel(child=layout_subnational, title = "Subnational level")

# Tab switch
tabs = Tabs(tabs=[tab_global, tab_subnational])

layout = tabs

# Show plot
curdoc().add_root(layout)

#show(tabs)
