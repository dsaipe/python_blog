# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 10:28:55 2022

@author: dfs20
"""

import shiny
from shiny import App, ui, render
import pandas as pd
import plotnine as gg
import nest_asyncio

nest_asyncio.apply()

movies = pd.read_csv('movies.csv')

nrow = len(movies)

app_ui = ui.page_fluid(
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_select("y",
                            "Y-axis",
                            choices = {"imdb_rating": "IMDB Rating", 
                                      "imdb_num_votes": "Number of IMDB Votes", 
                                      "critics_score": "Critics Score", 
                                      "audience_score": "Audience Score", 
                                      "runtime": "Runtime"},
                            selected = "imdb_rating"),
            ui.input_select("x",
                            "X-axis",
                            choices = {"imdb_rating": "IMDB Rating", 
                                      "imdb_num_votes": "Number of IMDB Votes", 
                                      "critics_score": "Critics Score", 
                                      "audience_score": "Audience Score", 
                                      "runtime": "Runtime"},
                            selected = "imdb_num_votes"),
            ui.input_select("z",
                            "Colour",
                            choices = {"title_type": "Type", 
                                      "genre": "Genre",
                                      "mpaa_rating": "MPAA Rating"},
                            selected = "title_type"),
            ui.input_checkbox("show_data",
                              "Show data table",
                              value = False)
            ),
        ui.panel_main(
            ui.output_plot("scatterplot"),
            ui.output_table("moviestable")
            )
        )
    )

def server(input, output, session):
    @output
    @render.plot
    def scatterplot():
        plot = (gg.ggplot(movies, gg.aes(input.x, input.y)) + 
                    gg.geom_point(colour = input.z))
        return plot
    @output
    @render.table
    def moviestable():
        if input.show_data == True:
            return movies
    return server
        
app = App(app_ui, server, debug = True)

shiny.run_app(app)
