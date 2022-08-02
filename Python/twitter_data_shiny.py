# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 11:55:28 2022

@author: dfs20
"""

from shiny import App, ui, render
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotnine as gg

jr = pd.read_csv('Data/jr_shiny.csv')
jr = jr.astype(object)

#rstats = pd.read_csv('rstats_hashtag.csv')
#rstats = rstats.filter(['screen_name', 'created_at', 'text', 'favorite_count',
#                        'retweet_count'])

choices = ({'year': 'Year',
           'day': 'Day',
           'hour_posted': 'Hour',
           'media_type': 'Media'})

app_ui = ui.page_flui(
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_select(id = "x",
                            label = "Variable",
                            choices = {'year': 'Year',
                                       'day': 'Day',
                                       'hour_posted': 'Hour',
                                       'media_type': 'Media'},
                            selected = 'year'),
            ui.input_numeric(id = "num",
                             label = "Display @jumping_uk tweets", 
                             value = 0,
                             min = 0,
                             max = 881)
            ),
        ui.panel_main(
            ui.output_plot("bar"),
            ui.output_table("table")
            )
        )
    )

def server(input, output, session):
    @output
    @render.plot
    def bar():
        avg_int = jr.groupby(input.x(), as_index = False).agg({'retweet_count':'mean',
                                                               'favorite_count':'mean'})
        avg_int = pd.melt(avg_int, id_vars = input.x())
        plot = (gg.ggplot(avg_int, gg.aes(input.x(), 'value', fill = 'variable')) +
                    gg.geom_col(position = 'dodge') +
                    gg.xlab(str.title(choices[input.x()])) +
                    gg.ylab("Average Interactions") +
                    gg.scale_fill_brewer(type = "qual", palette = "Dark2",
                                         name = "Interaction",
                                         labels = (["Favourite Count", "Retweet Count"])) +
                    gg.theme_classic())
        return plot
    @output
    @render.table
    def table():
        cols = jr.filter(['created_at', 'text', 'favorite_count', 'retweet_count'])
        first_n = cols.head(input.num())
        return first_n
    return server
    
app = App(app_ui, server, debug = True)

