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
from Utils.Material_quantities import materialQuantities
from Utils.Default_costs import defaultCosts

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

        #####################################
        ### Numeric feasibility criteria ###
        #####################################
        # Dictionary to store numeric sidebar outputs

        # List of numeric feasibility criteria
        # numeric_criteria = list(self.df.loc[(self.df['Numeric?'] == 'Yes') &
        #                                     (self.df.index.isin(feasibility_criteria_selected))].index)
        st.sidebar.subheader('Bridge span (m) for cost calculation')

        # Slider for span
        self.span_slider = st.sidebar.slider('Span (m)', min_value=0, max_value=int(self.df_bridges_only.loc['Span (m)'].max())
                                             , value=10)

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

    def material_quantities_costs(self):
        ####################################
        ### Table of material quantities ###
        ####################################
        st.subheader('Material quantities of selected bridges')

        # Explanation of the table in an expander
        with st.expander('Explanation'):
            st.write('''The table below shows the material quantities of the selected bridges. Values are calculated
            per meter width of bridge deck. The quantities obtained do not include the substructure and earthworks. The
            quantities are calculated using formula obtained from the literature. \nThe masonry arch bridge stone 
            quantities are obtained from the formula by Paul Dequeker as given below:''')
            st.latex(r'''Masonry\_stone = 0.075span^2 + 1.24span + 1.01''')
            st.write('''for a Roman arch bridge, while the formula for a segmental arch bridge the formula is:''')
            st.latex(r'''Masonry\_stone = 0.069span^2 + 1.42span + 1.42''')
            st.write('''The quantities for skilled and unskilled labour are obtained from the following rules of thumb:''')
            # Bulleted list of rules of thumb
            st.write('''- Cement requirement: 1.5 - 1.8 bags per cubic meter of stone masonry for a 1:3 mix''')
            st.write('''- Labour: 1 mason with 2 casual labourers construct 1.3 - 1.6 cubic meters of stone masonry per 
            day''')



        # Creating a material_quantities object with the span value
        material_quantities = materialQuantities(self.span_slider)
        material_quantities.calculate_quantities()

        # Make first column bold
        all_material_quantities = make_first_column_bold(material_quantities.all_quantities).fillna('')

        # Replacing zeros with 'Max span exceeded' - has to be done as the last thing, otherwise some previous
        # formatting won't work
        all_material_quantities_display = all_material_quantities.replace(0, 'Max span exceeded')



        # Write the contents as a plotly table
        fig = go.Figure(data=[go.Table(
            header=dict(values=list(all_material_quantities_display.columns),
                        fill_color='#9cd1b4',
                        align='left'),
            cells=dict(values=[all_material_quantities_display[col] for col in all_material_quantities_display.columns],
                       fill_color='#ecf7f1',
                       align='left', height=25))
        ])

        # Update figure to make it wider, increase font size, increase the height of the rows and wrap text
        fig.update_layout(width=1200, height=500, font_size=15, margin=dict(l=0, r=0, b=0, t=0))

        st.write(fig)

        #################################
        ######### Costs ##################
        #################################
        st.header('Cost Calculation')
        st.subheader('Items with per linear meter cost (Suspended Cable Bridge)')

        # Getting the per linear meter cost of the items
        default_costs = defaultCosts(self.path)
        col1a, col2a = st.columns(2)
        with col1a:
            steel_decking_cost = st.number_input('Steel Decking Cost (USD)', min_value=0.0,
                                                 max_value=default_costs.steel_decking*2,
                                                 value=default_costs.steel_decking, step=0.1)
            crossbeams_bolts = st.number_input('Crossbeams + Bolts Cost (USD)', min_value=0.0,
                                                max_value=default_costs.crossbeams_bolts*2,
                                                value=default_costs.crossbeams_bolts, step=0.1)
            fencing = st.number_input('Fencing System (USD)', min_value=0.0, max_value=default_costs.fencing*2,
                                        value=default_costs.fencing, step=0.1)
        with col2a:
            restraint_handrail = st.number_input('Restraint and Handrail Wires (USD)', min_value=0.0,
                                                    max_value=default_costs.restraint_handrail*2,
                                                    value=default_costs.restraint_handrail, step=0.1)
            cables_clips = st.number_input('Cables and Clips Cost (USD)', min_value=0.0,
                                                max_value=default_costs.cables_clips*2,
                                                value=default_costs.cables_clips, step=0.1)

        st.subheader('Lumpsum costs (Suspended Cable Bridge)')

        # Getting the lumpsum costs
        col1b, col2b = st.columns(2)
        with col1b:
            concrete_works_suspended_bridge = st.number_input('Concrete Works (USD)', min_value=0.0,
                                                               max_value=default_costs.concrete_works_suspended_bridge * 2,
                                                               value=default_costs.concrete_works_suspended_bridge, step=0.1)
            steel_reinf_suspended_bridge = st.number_input('Steel Works (USD)', min_value=0.0,
                                max_value=default_costs.steel_reinf_suspended_bridge*2,
                                value=default_costs.steel_reinf_suspended_bridge, step=0.1)

        # List of unit costs
        # Numeric entry in two columns
        st.subheader('Unit Costs for Other Items')
        col1c, col2c = st.columns(2)
        with col1c:
            cement_cost = st.number_input('Cement Cost/50kg bag (USD)', min_value=0.0, max_value=default_costs.cement_cost*2,
                                            value=default_costs.cement_cost, step=0.1)
            steel_cost = st.number_input('Steel Cost/kg (USD)', min_value=0.0, max_value=default_costs.steel_cost*2,
                                            value=default_costs.steel_cost, step=0.1)
            skilled_labor_cost = st.number_input('Skilled Labor Cost/man-day (USD)', min_value=0.0, max_value=default_costs.skilled_labor_cost*2,
                                                    value=default_costs.skilled_labor_cost, step=0.1)
            masonry_cost = st.number_input('Masonry Cost/m3 (USD)', min_value=0.0, max_value=default_costs.masonry_cost*2,
                                            value=default_costs.masonry_cost, step=0.1)

        with col2c:
            sand_cost = st.number_input('Sand Cost/m3 (USD)', min_value=0.0, max_value=default_costs.sand_cost*2,
                                            value=default_costs.sand_cost, step=0.1)
            aggt_cost = st.number_input('Aggregate (20mm) Cost/m3 (USD)', min_value=0.0, max_value=default_costs.aggt_cost*2,
                                            value=default_costs.aggt_cost, step=0.1)
            unskilled_labor_cost = st.number_input('Unskilled Labor Cost/man-day (USD)', min_value=0.0,
                                                   max_value=default_costs.unskilled_labor_cost*2,
                                                    value=default_costs.unskilled_labor_cost, step=0.1)

        #### Unit costs (continued) ####
        # Convert to pandas series, with same row names as all_quantities from the main_page
        unit_costs = pd.Series([masonry_cost, cement_cost, skilled_labor_cost, unskilled_labor_cost,
                                steel_cost, sand_cost, aggt_cost], index=all_material_quantities.iloc[:, 0])
        # costs = unit_costs * all_material_quantities.iloc[:, 1:].replace('', 0.0).astype(float)
        # Multiply each column by the unit cost
        costs = all_material_quantities.set_index('Material').replace('', 0.0).astype(float).multiply(unit_costs,
                                                                                                 axis=0)
        st.subheader('Total Costs for Bridge Superstructures')
        # Create a table of total costs and plot as a plotly table
        total_costs = costs.sum(axis=0).to_frame(name='Total Cost (USD)')

        # Add the per linear meter costs multiplied by the span and the lumpsum costs
        total_costs.loc['Suspended Cable Bridge'] += (
                (steel_decking_cost + crossbeams_bolts + fencing
                 + restraint_handrail + cables_clips) * self.span_slider
                + concrete_works_suspended_bridge + steel_reinf_suspended_bridge)

        # Formatting
        total_costs = total_costs.reset_index().rename({'index': 'Bridge Type'}, axis=1)
        total_costs = make_first_column_bold(total_costs).applymap(round_non_nan).fillna('')

        # Replacing zeros with 'Max span exceeded' - has to be done as the last thing, otherwise some previous
        # formatting won't work
        total_costs = total_costs.replace(0, 'Max span exceeded')
        fig = go.Figure(data=[go.Table(
            header=dict(values=list(total_costs.columns),
                        fill_color='#9cd1b4',
                        align='left'),
            cells=dict(values=[total_costs[col] for col in total_costs.columns],
                       fill_color='#ecf7f1',
                       align='left', height=25))
        ])

        # Update figure to make it wider, increase font size, increase the height of the rows and wrap text
        fig.update_layout(width=1200, height=200, font_size=15, margin=dict(l=0, r=0, b=0, t=0))

        st.write(fig)


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
        self.material_quantities_costs()
        self.additional_info()
        self.resources()



if __name__ == '__main__':
    dashboard = dashboard()
    dashboard.dashboard_streamlit()