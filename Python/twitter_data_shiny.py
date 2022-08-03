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

app_ui = ui.page_fluid(
    ui.panel_title("@jumping_uk Twitter Data"),
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_select(id = "x",
                            label = "Variable",
                            choices = {'year': 'Year',
                                       'day': 'Day',
                                       'hour_posted': 'Hour',
                                       'media_type': 'Media'},
                            selected = 'year'),
            ui.input_slider(id = "num",
                             label = "How many tweets would you like to view?", 
                             value = 0,
                             min = 0,
                             max = 881)
            ),
        ui.panel_main(
            ui.output_plot("bar"),
            ui.output_text("text"),
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
    @render.text
    def text():
        if input.num() == 0:
            return "Displaying no @jumping_uk tweets:"
        elif input.num() == 1:
            return "Displaying the most recent @jumping_uk tweet:"
        else:
            return f"Displaying the {input.num()} most recent @jumping_uk tweets:"
    @output
    @render.table
    def table():
        cols = jr.filter(['created_at', 'text', 'favorite_count', 'retweet_count'])
        cols.rename(columns = {'created_at': 'Date', 'text': 'Text', 
                               'favorite_count': 'Likes', 'retweet_count': 'Retweets'},
                    inplace = True)
        pd.set_option('colheader_justify', 'left')
        first_n = cols.head(input.num())
        return first_n
    return server
    
app = App(app_ui, server, debug = True)

