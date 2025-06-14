#!/usr/bin/env python
# coding: utf-8

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the dataset
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Automobile Sales Statistics Dashboard"

# App layout
app.layout = html.Div([
    html.H1("Automobile Sales Statistics Dashboard", style={'textAlign': 'center', 'marginBottom': '30px'}),
    
    dcc.Dropdown(
        id='dropdown-statistics',
        options=[
            {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
            {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
        ],
        value='Yearly Statistics',
        clearable=False,
        style={'width': '300px', 'marginBottom': '20px'}
    ),
    
    dcc.Dropdown(
        id='select-year',
        options=[{'label': str(y), 'value': y} for y in sorted(data['Year'].unique())],
        value=2022,
        clearable=False,
        style={'width': '150px', 'marginBottom': '40px'}
    ),
    
    html.Div(id='output-container')
])

# Toggle year dropdown based on selected statistic type
@app.callback(
    Output('select-year', 'disabled'),
    Input('dropdown-statistics', 'value')
)
def toggle_year_dropdown(selected_stat):
    return selected_stat == 'Recession Period Statistics'

# Update charts based on user input
@app.callback(
    Output('output-container', 'children'),
    [Input('dropdown-statistics', 'value'),
     Input('select-year', 'value')]
)
def update_graphs(selected_stat, selected_year):
    if selected_stat == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]

        # Plot 1
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = html.Div([
            html.H4("Average Automobile Sales Over Recession Years"),
            dcc.Graph(figure=px.line(yearly_rec, x='Year', y='Automobile_Sales',
                                     title="Average Automobile Sales Over Recession Years"))
        ], style={'flex': '1', 'padding': '10px'})

        # Plot 2
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = html.Div([
            html.H4("Average Number of Vehicles Sold by Vehicle Type"),
            dcc.Graph(figure=px.bar(average_sales, x='Vehicle_Type', y='Automobile_Sales',
                                    title="Average Automobile Sales by Vehicle Type"))
        ], style={'flex': '1', 'padding': '10px'})

        # Plot 3
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = html.Div([
            html.H4("Advertising Expenditure Share by Vehicle Type During Recessions"),
            dcc.Graph(figure=px.pie(exp_rec, values='Advertising_Expenditure', names='Vehicle_Type',
                                    title="Total Advertising Expenditure Share by Vehicle Type"))
        ], style={'flex': '1', 'padding': '10px'})

        # Plot 4
        unemp_data = recession_data.groupby(['Unemployment_Rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = html.Div([
            html.H4("Effect of Unemployment Rate on Vehicle Type and Sales"),
            dcc.Graph(figure=px.bar(unemp_data, x='Unemployment_Rate', y='Automobile_Sales',
                                    color='Vehicle_Type',
                                    title="Effect of Unemployment Rate on Vehicle Type and Sales"))
        ], style={'flex': '1', 'padding': '10px'})

        return html.Div([
            html.Div([R_chart1, R_chart2], style={'display': 'flex'}),
            html.Div([R_chart3, R_chart4], style={'display': 'flex'})
        ])

    elif selected_stat == 'Yearly Statistics' and selected_year is not None:
        yearly_data = data[data['Year'] == selected_year]

        # Plot 1: Line chart - Average sales per year
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = html.Div([
            html.H4("Average Automobile Sales Over All Years"),
            dcc.Graph(figure=px.line(yas, x='Year', y='Automobile_Sales',
                                     title="Average Automobile Sales Over Years"))
        ], style={'flex': '1', 'padding': '10px'})

        # Plot 2: Monthly sales for selected year
        mas = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = html.Div([
            html.H4(f"Total Monthly Automobile Sales in {selected_year}"),
            dcc.Graph(figure=px.line(mas, x='Month', y='Automobile_Sales',
                                     title=f"Total Monthly Automobile Sales in {selected_year}"))
        ], style={'flex': '1', 'padding': '10px'})

        # Plot 3: Bar chart - Avg vehicles sold by type in year
        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = html.Div([
            html.H4(f"Average Vehicles Sold by Vehicle Type in {selected_year}"),
            dcc.Graph(figure=px.bar(avr_vdata, x='Vehicle_Type', y='Automobile_Sales',
                                    title=f"Average Automobile Sales by Vehicle Type in {selected_year}"))
        ], style={'flex': '1', 'padding': '10px'})

        # Plot 4: Pie chart - Ad spend by vehicle type in year
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = html.Div([
            html.H4(f"Advertising Expenditure Share by Vehicle Type in {selected_year}"),
            dcc.Graph(figure=px.pie(exp_data, values='Advertising_Expenditure', names='Vehicle_Type',
                                    title=f"Advertising Expenditure Share by Vehicle Type in {selected_year}"))
        ], style={'flex': '1', 'padding': '10px'})

        return html.Div([
            html.Div([Y_chart1, Y_chart2], style={'display': 'flex'}),
            html.Div([Y_chart3, Y_chart4], style={'display': 'flex'})
        ])

    else:
        return html.Div("Please select a valid option.", style={'padding': '20px'})


if __name__ == '__main__':
    app.run(debug=True)
