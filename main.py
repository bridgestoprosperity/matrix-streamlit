# Making a streamlit app
import numpy as np
import streamlit as st
import pandas as pd
import os
import sys
from PIL import Image
from Utils.utils import *

class dashboard:
    def __init__(self):
        self.df = pd.read_excel('Excel Transcription of Data Analysis.xlsx', header=0, index_col=0, sheet_name='Data')
        self.df_bridges_only = self.df.copy().drop(['Feasibility criteria?', 'Numeric?', 'For comparison?'], axis=1)
        self.numeric_dict = {}     # Dictionary that will store numeric sidebar outputs
        self.non_numeric_dict = {}     # Dictionary that will store non-numeric sidebar outputs

    def sidebar(self):
        ########################
        ### Sidebar contents ###
        ########################
        # st.sidebar.subheader('Feasibility Criteria')

        # List of feasibility criteria
        feasibility_criteria = self.df.loc[self.df['Feasibility criteria?'] == 'Yes'].index.to_list()
        # Multiselect for the feasibility criteria selected
        feasibility_criteria_selected = st.sidebar.multiselect('Feasibility Criteria', options=feasibility_criteria)

        #####################################
        ### Numeric feasibility criteria ###
        #####################################
        # Dictionary to store numeric sidebar outputs

        # List of numeric feasibility criteria
        numeric_criteria = list(self.df.loc[(self.df['Numeric?'] == 'Yes') &
                                            (self.df.index.isin(feasibility_criteria_selected))].index)
        st.sidebar.subheader('Numeric Criteria')
        # Slider for numeric feasibility criteria
        for key, item in enumerate(numeric_criteria):
            self.numeric_dict[item] = st.sidebar.slider(item, min_value=0, max_value=self.df_bridges_only.loc[item].max(), value=0)

        #####################################
        ### Non-numeric feasibility criteria ###
        #####################################
        st.sidebar.subheader('Non-Numeric Criteria')
        # List of non-numeric feasibility criteria
        non_numeric_criteria = list(self.df.loc[(self.df['Numeric?'] == 'No')
                                                & (self.df.index.isin(feasibility_criteria_selected))].index)


        # Dictionary to store non-numeric sidebar outputs
        # Multi-select for non-numeric feasibility criteria
        for key, item in enumerate(non_numeric_criteria):
            tmp = self.df_bridges_only.loc[non_numeric_criteria[key]].apply(break_at_semicolon).to_list()
            unique_values = list(set([item for sublist in tmp for item in sublist]))
            self.non_numeric_dict[item] = st.sidebar.multiselect(item, options=unique_values)

        # #################################
        # ### Choice of evaluation mode ###
        # #################################
        # st.sidebar.subheader('Evaluation Mode')
        # evaluation_mode = st.sidebar.radio('Evaluation Mode', ['Flowchart', 'Matrix Format'])



    def main_page(self):
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

        ################
        #### Graphs ####
        ################
        st.subheader('Numeric characteristics of selected bridges')
        numeric_data_display = self.df_bridges_only.copy().loc[self.df['Numeric?'] == 'Yes', :]
        numeric_data_display = check_numeric_criteria(self.numeric_dict, numeric_data_display)
        # numeric_data_display = wrap_dataframe_column_names(numeric_data_display)    # Add newlines to column names to
        # make them fit in the graph
        for indx in numeric_data_display.index:
            st.bar_chart(numeric_data_display.loc[indx, :])

        #############
        ### Tables ###
        #############
        st.subheader('Non-numeric characteristics of selected bridges')

        # filter_dict = self.non_numeric_dict.copy()   # we copy the dictionary to apply make_regex on it
        # for key, item in filter_dict.items():
        #     filter_dict[key] = make_regex(item)

        # We will filter the dataframe to only show the bridges with the selected non-numeric characteristics
        non_numeric_data = self.df_bridges_only.copy()
        non_numeric_data = non_numeric_data.loc[(self.df['Numeric?'] == 'No')&(self.df['For comparison?'] == 'Yes')]

        # Filter the dataframe to only show the bridges with the selected non-numeric characteristics
        non_numeric_data_display = check_strings_in_df(self.non_numeric_dict, non_numeric_data)
        st.table(replace_semicolon_with_newline(non_numeric_data_display))

        ########################
        ### Additional info ####
        ########################
        st.subheader('Additional information')
        additional_info = self.df_bridges_only.copy().loc[self.df['For comparison?'] == 'No', :].to_dict()
        for bridge_type, info in additional_info.items():
            with st.expander(bridge_type):
                for criterion, value in info.items():
                    if criterion == 'Image':
                        image_use = Image.open(value)
                        st.image(image_use, use_column_width=True)
                    if isinstance(value, str) and (criterion != 'Image'):
                        st.markdown(f'**{criterion}**')
                        st.markdown(break_make_list(value))

                    if isinstance(value, float):
                        if not np.isnan(value):
                            st.markdown(f'**{criterion}**')
                            st.markdown(value)

    def dashboard_streamlit(self):
        # self.df = self.df.T
        SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
        sys.path.append(os.path.dirname(SCRIPT_DIR))

        apptitle = 'Dashboard V1'
        st.set_page_config(page_title=apptitle, page_icon=":eyeglasses:")
        st.title('Rural Infrastructure Matrix')

        # Convert columns with 'Numeric?' = 'Yes' to numeric
        for indx in self.df.loc[self.df['Numeric?'] == 'Yes'].index:
            self.df_bridges_only.loc[indx, :] = self.df_bridges_only.loc[indx, :].astype(int)

        tab1, tab2 = st.tabs(['Options', 'Evaluation'])
        # Run sidebar
        with tab1:
            self.sidebar()
            self.main_page()



if __name__ == '__main__':
    dashboard = dashboard()
    dashboard.dashboard_streamlit()