# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 11:55:28 2022

@author: dfs20
"""

from shiny import App, ui, render
import pandas as pd
import plotnine as gg

jr = pd.read_csv("jr_shiny.csv")
jr = jr.astype({"year": "object", "day": "object", "hour": "object"})

choices_select = {"year": "Year", "day": "Day", "hour": "Hour", "media_type": "Media"}
choices_check = {
    "created_at": "Date",
    "text": "Text",
    "retweet_count": "Retweets",
    "favorite_count": "Likes",
}

app_ui = ui.page_fluid(
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_select(
                id="x", label="X-axis Variable", choices=choices_select, selected="year"
            ),
            ui.input_numeric(
                id="num",
                label="How many tweets do you want to view?",
                value=0,
                min=0,
                max=50,
            ),
            ui.panel_conditional(
                "input.num > 0 && input.num <= 50",
                ui.input_checkbox_group(
                    id="cols",
                    label="Select which variables you want to view:",
                    choices=choices_check,
                    selected=(["created_at", "text"]),
                ),
            ),
        ),
        ui.panel_main(
            ui.output_plot("plot"), ui.output_text("text"), ui.output_table("table")
        ),
    ),
)


def server(input, output, session):
    @output
    @render.plot
    def plot():
        avg_int = jr.groupby(input.x(), as_index=False).agg(
            {"retweet_count": "mean", "favorite_count": "mean"}
        )
        avg_int = pd.melt(avg_int, id_vars=input.x())
        plot = (
            gg.ggplot(avg_int, gg.aes(input.x(), "value", fill="variable"))
            + gg.geom_col(position="dodge")
            + gg.xlab(str.title(choices_select[input.x()]))
            + gg.ylab("Average Interactions")
            + gg.scale_fill_brewer(
                type="qual",
                palette="Dark2",
                name="Interaction",
                labels=(["Like", "Retweet"]),
            )
            + gg.theme_classic()
        )
        if input.x() == "day":
            return plot + gg.scale_x_discrete(
                labels=(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
            )
        else:
            return plot

    @output
    @render.text
    def text():
        if isinstance(input.num(), int):
            if input.cols() == () or input.num() <= 0 or input.num() > 50:
                return ""
            elif input.num() == 1:
                return "Displaying the most recent @jumping_uk tweet:"
            else:
                return f"Displaying the {input.num()} most recent @jumping_uk tweets:"
        else:
            return None

    @output
    @render.table
    def table():
        cols = jr.filter(input.cols())
        cols.rename(
            columns={
                "created_at": "Date",
                "text": "Text",
                "retweet_count": "Retweets",
                "favorite_count": "Likes",
            },
            inplace=True,
        )
        pd.set_option("colheader_justify", "left")
        first_n = cols.head(input.num())
        if isinstance(input.num(), int):
            if input.num() <= 0 or input.num() > 50:
                return None
            else:
                return first_n
        else:
            return None


app = App(app_ui, server)
