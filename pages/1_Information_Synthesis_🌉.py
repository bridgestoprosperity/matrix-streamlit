# Making a streamlit app
import numpy as np
import streamlit as st
import pandas as pd
import os
import sys
import urllib.request
import plotly.graph_objects as go
from dotmap import DotMap
from PIL import Image
from Utils.utils import *
from Utils.material_quantities import materialQuantities
from Utils.default_costs import defaultCostsSuspendedBridge

class dashboard:
    def __init__(self):
        self.path = r'C:\Users\mwendwa.kiko\Documents\Personal_Kiko\E4C_Internship\Other_Docs\Dashboard_test\Excel Transcription of Data Analysis.xlsx'
        # self.path = r'Excel Transcription of Data Analysis.xlsx'
        # For debugger mode
        self.df = pd.read_excel(self.path, header=0, index_col=0, sheet_name='Data')    # For running the dashboard
        self.df_bridges_only = self.df.copy().drop(['Feasibility criteria?', 'Numeric?', 'For comparison?'], axis=1)
        self.numeric_dict = {}     # Dictionary that will store numeric sidebar outputs
        self.non_numeric_dict = {}     # Dictionary that will store non-numeric sidebar outputs
        self.span_slider = 0         # Value returned by span slider

    def sidebar(self):
        ########################
        ### Sidebar contents ###
        ########################
        # st.sidebar.subheader('Feasibility Criteria')

        # #####################################
        # ### Numeric feasibility criteria ###
        # #####################################
        # # Dictionary to store numeric sidebar outputs
        #
        # # List of numeric feasibility criteria
        # # numeric_criteria = list(self.df.loc[(self.df['Numeric?'] == 'Yes') &
        # #                                     (self.df.index.isin(feasibility_criteria_selected))].index)
        # st.sidebar.subheader('Bridge span (m) for cost calculation')
        #
        # # Slider for span
        # self.span_slider = st.sidebar.slider('Span (m)', min_value=0, max_value=int(self.df_bridges_only.loc['Span (m)'].max())
        #                                      , value=10)

        # # Slider for numeric feasibility criteria
        # for key, item in enumerate(numeric_criteria):
        #     self.numeric_dict[item] = st.sidebar.slider(item, min_value=0, max_value=self.df_bridges_only.loc[item].max(), value=0)

        #####################################
        ### Non-numeric feasibility criteria ###
        #####################################
        st.sidebar.subheader('Filtering Criteria for Comparison Table')
        # List of feasibility criteria
        feasibility_criteria = self.df.loc[self.df['Feasibility criteria?'] == 'Yes'].index.to_list()
        # Multiselect for the feasibility criteria selected
        feasibility_criteria_selected = st.sidebar.multiselect('Filter by? ...', options=feasibility_criteria)

        # List of non-numeric feasibility criteria
        non_numeric_criteria = list(self.df.loc[(self.df['Numeric?'] == 'No')
                                                & (self.df.index.isin(feasibility_criteria_selected))].index)


        # Dictionary to store non-numeric sidebar outputs
        # Multi-select for non-numeric feasibility criteria
        for key, item in enumerate(non_numeric_criteria):
            tmp = self.df_bridges_only.loc[non_numeric_criteria[key]].apply(break_at_semicolon).to_list()
            unique_values = list(set([item for sublist in tmp for item in sublist if item != '']))
            self.non_numeric_dict[item] = st.sidebar.multiselect(item, options=unique_values)

        # #################################
        # ### Choice of evaluation mode ###
        # #################################
        # st.sidebar.subheader('Evaluation Mode')
        # evaluation_mode = st.sidebar.radio('Evaluation Mode', ['Flowchart', 'Matrix Format'])




    def comparison_table(self):


        # ################
        # #### Graphs ####
        # ################
        # st.subheader('Numeric characteristics of selected bridges')
        # numeric_data_display = self.df_bridges_only.copy().loc[self.df['Numeric?'] == 'Yes', :]
        # numeric_data_display = check_numeric_criteria(self.numeric_dict, numeric_data_display)
        # # numeric_data_display = wrap_dataframe_column_names(numeric_data_display)    # Add newlines to column names to
        # # make them fit in the graph
        # for indx in numeric_data_display.index:
        #     st.bar_chart(numeric_data_display.loc[indx, :])

        #############
        ### Tables ###
        #############
        st.subheader('Comparison table of selected bridges')

        # filter_dict = self.non_numeric_dict.copy()   # we copy the dictionary to apply make_regex on it
        # for key, item in filter_dict.items():
        #     filter_dict[key] = make_regex(item)

        # We will filter the dataframe to only show the bridges with the selected non-numeric characteristics
        non_numeric_data = self.df_bridges_only.copy()
        non_numeric_data = non_numeric_data.loc[(self.df['Numeric?'] == 'No') & (self.df['For comparison?'] == 'Yes')]

        # Filter the dataframe to only show the bridges with the selected non-numeric characteristics
        non_numeric_data_display = check_strings_in_df(self.non_numeric_dict, non_numeric_data)
        # st.table(replace_semicolon_with_newline(non_numeric_data_display))

        # Write the contents as a plotly table
        non_numeric_data_display.fillna('', inplace=True)    # Replace NaN with empty string to get rid of NA values

        # We wrap the column names to make them fit in the table, but only when the table has lots of columns
        if len(list(non_numeric_data_display.columns)) > 3:
            non_numeric_data_display = wrap_dataframe_column_values(replace_semicolon_with_linebreak(non_numeric_data_display))
        else:
            non_numeric_data_display = replace_semicolon_with_linebreak(non_numeric_data_display)

        # We name the axis and reset the index so that it appears in the table as a column
        non_numeric_data_display.index.name = 'Evaluation criteria'
        non_numeric_data_display.reset_index(inplace=True)

        # Creating a material_quantities object with the span value
        material_quantities = materialQuantities(self.span_slider)
        material_quantities.calculate_quantities()

        # Make first column bold
        non_numeric_data_display = make_first_column_bold(non_numeric_data_display).fillna('')


        # ## Write the contents as a html list
        # # non_numeric_data_display = replace_text_with_bulleted_list(non_numeric_data_display)
        # non_numeric_data_display = convert_dataframe_to_plotly_table(non_numeric_data_display, 'Suspended Cable Bridge')

        # Write the contents as a plotly table
        fig = go.Figure(data=[go.Table(
            header=dict(values=list(non_numeric_data_display.columns),
                        fill_color='#9cd1b4',
                        align='left'),
            cells=dict(values=[non_numeric_data_display[col] for col in non_numeric_data_display.columns],
                       fill_color='#ecf7f1',
                       align='left', height=25))
        ])

        # Update figure to make it wider, increase font size, increase the height of the rows and wrap text
        fig.update_layout(width=1200, height=800, font_size=15, margin=dict(l=0, r=0, b=0, t=0))

        st.write(fig)

        # # Using containers and tables, make a pseudo-list
        # non_numeric_data_display = markdown_list_from_dataframe(non_numeric_data_display)



    def additional_info(self):
        ########################
        ### Additional info ####
        ########################
        st.subheader('Additional information')
        additional_info = self.df_bridges_only.copy().loc[self.df['For comparison?'] == 'No', :].to_dict()
        for bridge_type, info in additional_info.items():
            with st.expander(bridge_type):
                for criterion, value in info.items():
                    # if criterion == 'Image':
                    #     # urllib.request.urlopen(value, f"{bridge_type}.jpg")
                    #     # image_use = Image.open(f'{bridge_type}.jpg')
                    #     image_use = Image.open(value)
                    #     # st.image(image_use, use_column_width=True)
                    if isinstance(value, str) and (criterion != 'Image'):
                        st.markdown(f'**{criterion}**')
                        st.markdown(break_make_list(value))

                    if isinstance(value, float):
                        if not np.isnan(value):
                            st.markdown(f'**{criterion}**')
                            st.markdown(value)

    def resources(self):
        ################
        ### Resources ###
        ################
        st.subheader('List of Resources')
        resources = self.df_bridges_only.loc['Resources', :].to_dict()
        for bridge_type, value in resources.items():
            st.markdown(f'**{bridge_type}**')
            resrce = markdown_string_of_links(value)
            for link in resrce:
                st.markdown(link, unsafe_allow_html=True)

    def dashboard_streamlit(self):
        # self.df = self.df.T
        SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
        sys.path.append(os.path.dirname(SCRIPT_DIR))

        apptitle = 'Dashboard V1'
        st.set_page_config(page_title=apptitle, page_icon="🌉", layout="wide")
        st.title('Rural Infrastructure Matrix')

        # Convert columns with 'Numeric?' = 'Yes' to numeric
        for indx in self.df.loc[self.df['Numeric?'] == 'Yes'].index:
            self.df_bridges_only.loc[indx, :] = self.df_bridges_only.loc[indx, :].astype(float)

        # Display the sidebar and main page
        self.sidebar()
        self.comparison_table()
        # self.material_quantities_costs()
        self.additional_info()
        self.resources()



if __name__ == '__main__':
    dashboard = dashboard()
    dashboard.dashboard_streamlit()