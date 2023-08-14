import pandas as pd
import streamlit as st
import os
import graphviz
from Utils.utils import *
from Utils.material_quantities import materialQuantities
from Utils.default_costs import defaultCostsSuspendedBridge, defaultCostsSuspensionBridge, defaultUnitCosts
from Utils.graph_generation import graph_generation
from Utils.downloadable_report import report_builder
import plotly.graph_objects as go

os.environ["PATH"] += os.pathsep + r'C:\Program Files\Graphviz\bin'   #TODO: Comment this out before push

class material_quantities_costs:
    def __init__(self):
        # #For running on my local machine
        # self.path = r'C:\Users\mwendwa.kiko\Documents\Personal_Kiko\E4C_Internship\Other_Docs\Dashboard_test\Excel Transcription of Data Analysis.xlsx'
        # #For running on the server
        self.path = r'Excel Transcription of Data Analysis.xlsx'
        # For debugger mode
        self.df = pd.read_excel(self.path, header=0, index_col=0, sheet_name='Data')  # For running the dashboard
        self.df_bridges_only = self.df.copy().drop(['Feasibility criteria?', 'Numeric?', 'For comparison?'], axis=1)
        self.span_slider = 0
        self.total_costs = pd.DataFrame()

    def sidebar(self):
        ########################
        ### Sidebar contents ###
        ########################

        st.sidebar.subheader('Bridge span (m) for cost calculation')

        # Slider for span
        self.span_slider = st.sidebar.slider('Span (m)', min_value=0, max_value=int(self.df_bridges_only.loc['Span (m)'].max())
                                             , value=10)

    def material_quantities_costs(self):


        ####################################
        ### Table of material quantities ###
        ####################################
        st.subheader('Material quantities of selected bridges')

        # Explanation of the table in an expander
        with st.expander('Explanation of the material quantities and cost calculations'):
            # Masonry bridge quantities
            st.write('''The table below shows the material quantities of the selected bridges. Values are calculated
            per meter width of bridge deck. The quantities obtained do not include the substructure and earthworks. The
            quantities are calculated using formula obtained from the literature.\n\n **Masonry Bridge Quantities**
            \nThe masonry arch bridge stone quantities are obtained from the formula by Paul Dequeker as given below:''')
            st.latex(r'''Masonry\_stone = 0.075span^2 + 1.24span + 1.01''')
            st.write('''for a Roman arch bridge, while the formula for a segmental arch bridge the formula is:''')
            st.latex(r'''Masonry\_stone = 0.069span^2 + 1.42span + 1.42''')
            st.write('''The quantities for skilled and unskilled labour are obtained from the following rules of thumb:''')
            # Bulleted list of rules of thumb
            st.write('''- Cement requirement: 1.5 - 1.8 bags per cubic meter of stone masonry for a 1:3 mix''')
            st.write('''- Labour: 1 mason with 2 casual labourers construct 1.3 - 1.6 cubic meters of stone masonry per 
            day''')

            # Suspended bridge quantities
            st.write('''\n\n**Suspended Bridge Quantities**\n\nThe costs for the suspended bridge are obtained
            from the cost estimation spreadsheet developed by the Edward Gould CEng MICE of the B2P team for internal use
            The full spreadsheet can be obtained from B2P upon request. \n\n Most of these item costs are given per meter
            length of bridge, unlike for the other bridge types, where the quantities are derived from first principles, 
            and the total cost is based on the unit cost of the materials themselves, such as steel and concrete. 
            Furthermore, some of the works, notably the abutments, are given as a lump sum, rather than as a cost per
            item. \n\nFor this reason, unlike for the other bridge types, the material quantities for the suspended bridge
            are not given in the table below. Instead, the total cost of the bridge is given, based on the cost per
            item.''')

            # Box culvert quantities
            st.write('''\n\n**Box Culvert Quantities**\n\nThe quantities for the box culvert are obtained from the work 
            of Fragkakis et al. (2015). Their study was based on the construction quantities for 104 recently completed 
            (at the time of the study) box culverts in Greece. Through this, they estimated the quantities of materials
            required for construction, according to the formulae given below:''')
            st.latex(r'''Volume_{concrete} = -4.08 + 2.46b_{net} + 0.67h_{net} + 0.22h_{over}''')
            st.latex(r'''Weight_{reinforcement} = -562 + 285b_{net} + 98h_{net} + 21h_{over}''')
            st.write('''where *b<sub>net</sub>* is the net width of the box culvert, *h<sub>net</sub>* is the 
            net height of the box culvert, and *h<sub>over</sub>* is the height of the overburden above the box culvert.'''
            , unsafe_allow_html=True)

            # Reinforced concrete unvented ford quantities
            st.write('''\n\n**Reinforced Concrete Unvented Ford Quantities**\n\nThe quantities for the reinforced
            concrete unvented ford are based on an standard design recommended in the 
            [Iowa DOT Guide](https://iowadot.gov/research/reports/Year/2003andolder/fullreports/tr453.pdf), page 18. 
            Furthermore, the quantities are mutliplied by 1.2 to account for the length along the streambed being
            longer than the straight line distance from bank to bank.'''
            , unsafe_allow_html=True)

        with st.expander('Material Quantities and Cost Calculations'):
            st.write('''The material quantities given below can be adjusted by changing the span value in the sidebar.
            ''')
            # Creating a material_quantities object with the span value
            material_quantities = materialQuantities(self.span_slider)
            material_quantities.calculate_quantities()

            # Make first column bold
            all_material_quantities = make_first_column_bold(material_quantities.all_quantities).fillna('')

            # Replacing zeros with 'Max span exceeded' - has to be done as the last thing, otherwise some previous
            # formatting won't work
            all_material_quantities_display = all_material_quantities.replace(1E9, 'Max span exceeded')



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
            st.write('''These are material quantities for the suspended cable bridge. Their default values are
            taken from B2P's internal work, as previously explained. They can however be adjusted by the user.''')

            # Getting the per linear meter cost of the items
            default_costs_suspended = defaultCostsSuspendedBridge(self.path)
            col1a, col2a = st.columns(2)
            with col1a:
                steel_decking_cost_suspended = st.number_input('Steel Decking Cost (USD)', min_value=0.0,
                                                     max_value=default_costs_suspended.steel_decking*2,
                                                     value=default_costs_suspended.steel_decking, step=0.1)
                crossbeams_bolts_suspended = st.number_input('Crossbeams + Bolts Cost (USD)', min_value=0.0,
                                                    max_value=default_costs_suspended.crossbeams_bolts*2,
                                                    value=default_costs_suspended.crossbeams_bolts, step=0.1)
                fencing_suspended = st.number_input('Fencing System (USD)', min_value=0.0, max_value=default_costs_suspended.fencing*2,
                                            value=default_costs_suspended.fencing, step=0.1)
            with col2a:
                restraint_handrail_suspended = st.number_input('Restraint and Handrail Wires (USD)', min_value=0.0,
                                                        max_value=default_costs_suspended.restraint_handrail*2,
                                                        value=default_costs_suspended.restraint_handrail, step=0.1)
                cables_clips_suspended = st.number_input('Cables and Clips Cost (USD)', min_value=0.0,
                                                    max_value=default_costs_suspended.cables_clips*2,
                                                    value=default_costs_suspended.cables_clips, step=0.1)

            st.subheader('Lumpsum costs (Suspended Cable Bridge)')

            # Getting the lumpsum costs
            col1b, col2b = st.columns(2)
            with col1b:
                concrete_works_suspended_bridge = st.number_input('Concrete Works (USD)', min_value=0.0,
                                                                   max_value=default_costs_suspended.concrete_works_suspended_bridge * 2,
                                                                   value=default_costs_suspended.concrete_works_suspended_bridge, step=0.1)
            with col2b:
                steel_reinf_suspended_bridge = st.number_input('Steel Works (USD)', min_value=0.0,
                                    max_value=default_costs_suspended.steel_reinf_suspended_bridge*2,
                                    value=default_costs_suspended.steel_reinf_suspended_bridge, step=0.1)

            # Exactly the same code for the suspended cable bridge, but for the suspension bridge
            st.subheader('Items with per linear meter cost (Suspension Bridge)')
            st.write('''These are material quantities for the suspension bridge. Their default values are
            taken from B2P's internal work, as previously explained. They can however be adjusted by the user.''')

            # Getting the per linear meter cost of the items
            default_costs_suspension = defaultCostsSuspensionBridge(self.path)

            col1c, col2c = st.columns(2)

            with col1c:
                steel_decking_cost_suspension = st.number_input('Suspension Bridge Steel Decking Cost (USD)', min_value=0.0,
                                                     max_value=default_costs_suspension.steel_decking*2,
                                                     value=default_costs_suspension.steel_decking, step=0.1)
                crossbeams_bolts_suspension = st.number_input('Suspension Bridge Crossbeams + Bolts Cost (USD)', min_value=0.0,
                                                    max_value=default_costs_suspension.crossbeams_bolts*2,
                                                    value=default_costs_suspension.crossbeams_bolts, step=0.1)
                fencing_suspension = st.number_input('Suspension Bridge Fencing System (USD)', min_value=0.0, max_value=default_costs_suspension.fencing*2,
                                            value=default_costs_suspension.fencing, step=0.1)
            with col2c:
                restraint_handrail_suspension = st.number_input('Suspension Bridge Restraint and Handrail Wires (USD)', min_value=0.0,
                                                        max_value=default_costs_suspension.restraint_handrail*2,
                                                        value=default_costs_suspension.restraint_handrail, step=0.1)
                cables_clips_suspension = st.number_input('Suspension Bridge Cables and Clips Cost (USD)', min_value=0.0,
                                                    max_value=default_costs_suspension.cables_clips*2,
                                                    value=default_costs_suspension.cables_clips, step=0.1)

            st.subheader('Lumpsum costs (Suspension Bridge)')

            # Getting the lumpsum costs
            col1d, col2d = st.columns(2)
            with col1d:
                concrete_works_suspension_bridge = st.number_input('Suspension Bridge Concrete Works (USD)', min_value=0.0,
                                                                   max_value=default_costs_suspension.concrete_works_suspension_bridge * 2,
                                                                   value=default_costs_suspension.concrete_works_suspension_bridge, step=0.1)
                tower_system_suspension_bridge = st.number_input('Suspension Bridge Tower System (USD)', min_value=0.0,
                                                                    max_value=default_costs_suspension.tower_system * 2,
                                                                    value=default_costs_suspension.tower_system, step=0.1)
            with col2d:
                steel_reinf_suspension_bridge = st.number_input('Suspension Bridge Steel Works (USD)', min_value=0.0,
                                    max_value=default_costs_suspension.steel_reinf_suspension_bridge*2,
                                    value=default_costs_suspension.steel_reinf_suspension_bridge, step=0.1)



            # List of unit costs
            # Numeric entry in two columns
            default_unit_costs = defaultUnitCosts(self.path)
            
            st.subheader('Unit Costs for Other Items')
            st.write('''These are unit costs for other items. Their default values are taken from market research, but
            can be adjusted by the user.''')
            col1e, col2e = st.columns(2)
            with col1e:
                cement_cost = st.number_input('Cement Cost/50kg bag (USD)', min_value=0.0, max_value=default_unit_costs.cement_cost*2,
                                                value=default_unit_costs.cement_cost, step=0.1)
                steel_cost = st.number_input('Steel Cost/kg (USD)', min_value=0.0, max_value=default_unit_costs.steel_cost*2,
                                                value=default_unit_costs.steel_cost, step=0.1)
                skilled_labor_cost = st.number_input('Skilled Labor Cost/man-day (USD)', min_value=0.0, max_value=default_unit_costs.skilled_labor_cost*2,
                                                        value=default_unit_costs.skilled_labor_cost, step=0.1)
                masonry_cost = st.number_input('Masonry Cost/m3 (USD)', min_value=0.0, max_value=default_unit_costs.masonry_cost*2,
                                                value=default_unit_costs.masonry_cost, step=0.1)

            with col2e:
                sand_cost = st.number_input('Sand Cost/m3 (USD)', min_value=0.0, max_value=default_unit_costs.sand_cost*2,
                                                value=default_unit_costs.sand_cost, step=0.1)
                aggt_cost = st.number_input('Aggregate (20mm) Cost/m3 (USD)', min_value=0.0, max_value=default_unit_costs.aggt_cost*2,
                                                value=default_unit_costs.aggt_cost, step=0.1)
                unskilled_labor_cost = st.number_input('Unskilled Labor Cost/man-day (USD)', min_value=0.0,
                                                       max_value=default_unit_costs.unskilled_labor_cost*2,
                                                        value=default_unit_costs.unskilled_labor_cost, step=0.1)

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
        self.total_costs = costs.sum(axis=0).to_frame(name='Total Cost (USD)')

        # Add the per linear meter costs multiplied by the span and the lumpsum costs for the suspension bridge and the
        # suspended cable bridge
        self.total_costs.loc['Suspended Cable Bridge'] += (
                (steel_decking_cost_suspended + crossbeams_bolts_suspended + fencing_suspended
                 + restraint_handrail_suspended + cables_clips_suspended) * self.span_slider
                + concrete_works_suspended_bridge + steel_reinf_suspended_bridge)

        self.total_costs.loc['Suspension Bridge'] += (
                (steel_decking_cost_suspension + crossbeams_bolts_suspension + fencing_suspension
                    + restraint_handrail_suspension + cables_clips_suspension) * self.span_slider
                + concrete_works_suspension_bridge + steel_reinf_suspension_bridge + tower_system_suspension_bridge)


        # Formatting
        self.total_costs = self.total_costs.reset_index().rename({'index': 'Bridge Type'}, axis=1)
        # self.total_costs = make_first_column_bold(self.total_costs).applymap(round_non_nan).fillna('')

        # Formatting
        total_costs_rendered = self.total_costs.copy().applymap(round_non_nan)
        total_costs_rendered = make_first_column_bold(total_costs_rendered)
        total_costs_rendered = render_df_formatting(total_costs_rendered)

        # # Replacing zeros with 'Max span exceeded' - has to be done as the last thing, otherwise some previous
        # # formatting won't work
        # self.total_costs = self.total_costs.replace(0, 'Max span exceeded')
        fig = go.Figure(data=[go.Table(
            header=dict(values=list(total_costs_rendered.columns),
                        fill_color='#9cd1b4',
                        align='left'),
            cells=dict(values=[total_costs_rendered[col] for col in total_costs_rendered],
                       fill_color='#ecf7f1',
                       align='left', height=25))
        ])

        # Update figure to make it wider, increase font size, increase the height of the rows and wrap text
        fig.update_layout(width=1200, height=225, font_size=15, margin=dict(l=0, r=0, b=0, t=0))

        st.write(fig)


class dashboard_evaluation:
    def __init__(self):
        # Config app
        apptitle = 'Evaluation Page'
        st.set_page_config(page_title=apptitle, page_icon=":eyeglasses:", layout='wide')
        st.title('Bridge Site Evaluation')

        # Load data
        # self.bridges_evaluation = pd.read_excel(r'C:\Users\mwendwa.kiko\Documents\Personal_Kiko\E4C_Internship\Other_Docs'
        #                                         r'\Dashboard_test\Excel Transcription of Data Analysis.xlsx', header=0,
        #                                         index_col=0, sheet_name='Decision Points')
        # That's for debugging, the one for display is below
        self.bridges_evaluation = pd.read_excel('Excel Transcription of Data Analysis.xlsx', header=0, index_col=0,
                                                sheet_name='Decision Points')
        self.bridge_itself_selection_dict = {}  # Stores the 'bridge itself' selection
        self.bridge_site_selection_dict = {}  # Stores the 'bridge site' selection
        self.wider_context_selection_dict = {}  # Stores the 'wider context' selection
        self.decision_points_selection_dict = {}  # Stores the output of all the decision points selected
        self.all_bridges = ['Suspended Cable Bridge', 'Suspension Bridge', 'Masonry Stone Arch Bridge', 'Timber Log Footbridge',
                            'Box Culvert', 'Unvented Ford/Drift']

        # Material quantities
        self.material_quantities_costs = material_quantities_costs()
        self.material_quantities_costs.sidebar()
        self.material_quantities_costs.material_quantities_costs()
        self.total_costs = self.material_quantities_costs.total_costs.set_index('Bridge Type')

        # Getting rid of the formatting tags in the index of total_costs
        self.total_costs.index = [x.replace('<b>', '').replace('</b>', '') for x in self.total_costs.index]

        # The bridge data used for the information synthesis tab
        self.bridge_data = self.material_quantities_costs.df_bridges_only
        self.principal_materials = self.bridge_data.loc['Principle structural material', :]
        self.vehicle_types_loading = self.bridge_data.loc['Allowable Traffic', :]


    def filter_on_cost(self, cost_input):
        # Bridges that are too expensive
        abandoned_on_cost = (self.total_costs[self.total_costs['Total Cost (USD)'] == 'Max span exceeded'].index.tolist()
                             + self.total_costs[self.total_costs['Total Cost (USD)'] > cost_input].index.tolist())

        # Bridges that are not too expensive
        remaining_on_cost = [bridge for bridge in self.all_bridges if bridge not in abandoned_on_cost]

        # Rename the 'Reinforced concrete unvented ford' to 'Unvented Ford/Drift' to match the other decision points
        remaining_on_cost = [x.replace('Reinforced Concrete Unvented Ford', 'Unvented Ford/Drift') for x in remaining_on_cost]
        abandoned_on_cost = [x.replace('Reinforced Concrete Unvented Ford', 'Unvented Ford/Drift') for x in abandoned_on_cost]

        # Turn remaining_on_cost and abandoned_on_cost into strings with semi-colon separators to match formatting elsewhere
        remaining_on_cost = '; '.join(remaining_on_cost)
        abandoned_on_cost = '; '.join(abandoned_on_cost)

        # Update the dataframe by appending a new row
        self.bridges_evaluation = pd.concat([self.bridges_evaluation,
                                             pd.DataFrame({'Options Remaining': [remaining_on_cost],
                                            'Options Abandoned': [abandoned_on_cost],
                                            'Meaning': """Available budget for construction of the bridge superstructure.
                                            The construction costs against which this will be compared are as calculated
                                            using the methods shown in the sections above. \n\nNote that for the Unvented
                                            Ford/Drift, the construction cost estimates given here are those for the 
                                            reinforced concrete unvented ford, assuming the design from the section 
                                            above. \n\nAlso note that the costs are per m width of bridge.""",},
                                            index=[f'Budget for Bridge Superstructure'])])

    def filter_on_bridge_data_row(self, input_list: list, input_row: pd.Series, index_name: str):
        # List of columns that contain the selected structural materials
        remaining_on_structural_material = (input_row[input_row.str.contains
                                                    ('|'.join(input_list), regex=True)].index.tolist())
        # Bridges that are made of the selected structural materials
        abandoned_on_structural_material = [bridge for bridge in self.all_bridges if bridge not in remaining_on_structural_material]

        # Turn remaining_on_structural_material and abandoned_on_structural_material into strings with semi-colon separators to match formatting elsewhere
        remaining_on_structural_material = '; '.join(remaining_on_structural_material)
        abandoned_on_structural_material = '; '.join(abandoned_on_structural_material)

        # Update the dataframe by appending a new row
        self.bridges_evaluation = pd.concat([self.bridges_evaluation,
                                             pd.DataFrame({'Options Remaining': [remaining_on_structural_material],
                                                            'Options Abandoned': [abandoned_on_structural_material],
                                                           'Meaning': """The structural material of the bridge superstructure.
                                                           The options remaining are those that contain at least one of the
                                                           structural materials selected."""
                                                           },
                                                            index=[index_name])])

    def filter_on_height_difference_abutments(self, height_difference_abutments_input):
        # The limit for the height difference between the abutments is 1/50 of the span for a suspension bridge
        if (self.material_quantities_costs.span_slider/50 < height_difference_abutments_input
                < self.material_quantities_costs.span_slider/25):
            abandoned_on_height_difference_abutments = ['Suspension Bridge']
        # The limit for the height difference between the abutments is 1/25 of the span for a suspended cable bridge
        elif height_difference_abutments_input > self.material_quantities_costs.span_slider/25:
            abandoned_on_height_difference_abutments = ['Suspended Cable Bridge', 'Suspension Bridge']
        else:
            abandoned_on_height_difference_abutments = []

        # Bridges that are not too high
        remaining_on_height_difference_abutments = [bridge for bridge in self.all_bridges if bridge not in abandoned_on_height_difference_abutments]

        # Turn remaining_on_height_difference_abutments and abandoned_on_height_difference_abutments into strings with semi-colon separators to match formatting elsewhere
        remaining_on_height_difference_abutments = '; '.join(remaining_on_height_difference_abutments)
        abandoned_on_height_difference_abutments = '; '.join(abandoned_on_height_difference_abutments)

        # Update the dataframe by appending a new row
        self.bridges_evaluation = pd.concat([self.bridges_evaluation,
                                             pd.DataFrame({'Options Remaining': [remaining_on_height_difference_abutments],
                                                            'Options Abandoned': [abandoned_on_height_difference_abutments],
                                                           'Meaning': """The recommended limits for the height difference
                                                           between abutments are: \n\n Suspension Bridge: span/50 
                                                           \n\nSuspended Cable Bridge: span/25."""
                                                           },
                                                            index=[f'Height difference between abutments (m)'])])


    def main_page(self):
        st.header('Dynamic Design Flowchart for Bridge Evaluation')
        with st.expander('Explanation of the flowchart'):
            st.write("""The dynamic flowchart below enables evaluation of the possible bridge options for a particular 
            site. The evaluation can be made across three dimensions: \n- The characteristics of the bridge itself: these
            include the allowable loading, structural material and cost 
            \n- The characteristics of the bridge site: these include the river flow volumes and the riverbed material
            \n- The wider transport network. \nFor each of these options it is possible to define attributes of the bridge/
            bridge site, and based on these filter out the options that do not meet the selected criteria, leaving only those 
            that do. \n One caveat here: an option may be filtered out multiple times at different decision nodes.""")
        # Create a container with 4 columns
        col1, col2, col3 = st.columns(3)

        # Column 1
        with col1:
            st.subheader('Bridge Itself')
            # st.expander('Explanation will go here', expanded=False)
            bridge_itself_options = self.bridges_evaluation.loc[self.bridges_evaluation['Type of variable'] == 'Bridge Itself']\
                .index.tolist() + ['Budget for Bridge Superstructure', 'Principal Structural Material',
                                   'Vehicle types/Allowable loading']  # Budget for Bridge Superstructure is not in the
            # excel file, so it's added here, same for Principal Structural Material

            # Create a multiselect for the bridge itself options
            bridge_itself_selection = st.multiselect('Select the bridge itself options', options=bridge_itself_options)

            # # Create a selectbox for the each selected option in the multiselect and store the results in a single dictionary
            #
            # for option in bridge_itself_selection:
            #     self.bridge_itself_selection_dict[option] = st.selectbox(option, options=['Yes', 'No'])

            # For the time being just create a dictionary with all the options set to 'Yes'
            for option in bridge_itself_selection:
                self.bridge_site_selection_dict[option] = 'Yes'

                # Create a numeric input for the cost of the bridge superstructure
                if option == 'Budget for Bridge Superstructure':
                    superstructure_cost = st.number_input('Budget for Bridge Superstructure (USD)', min_value=0.0,
                                                              max_value=self.total_costs.max().max(),
                                                          value=0.0, step=0.1)
                    self.filter_on_cost(superstructure_cost)
                elif option == 'Principal Structural Material':
                    self.materials_selected = st.multiselect('Principal Structural Material',
                                                             options=unique_row_values(self.principal_materials))
                    self.filter_on_bridge_data_row(self.materials_selected, self.principal_materials,
                                                   'Principal Structural Material')
                elif option == 'Vehicle types/Allowable loading':
                    self.vehicle_types_selected = st.multiselect('Vehicle types/Allowable loading',
                                                                 options=unique_row_values(self.vehicle_types_loading))
                    self.filter_on_bridge_data_row(self.vehicle_types_selected, self.vehicle_types_loading,
                                                   'Vehicle types/Allowable loading')
                st.markdown(f"**{option}**: {self.bridges_evaluation.loc[option, 'Meaning']}\n")  # Display the *
                # explanation of the options selected

        with col2:
            st.subheader('Bridge Site')
            # st.expander('Explanation will go here', expanded=False)
            bridge_site_options = self.bridges_evaluation.loc[self.bridges_evaluation['Type of variable'] == 'Bridge Site']\
                .index.tolist() + ['Height difference between abutments (m)']

            # Create a multiselect for the bridge site options
            bridge_site_selection = st.multiselect('Select the bridge site options', options=bridge_site_options)

            # Create a selectbox for the each selected option in the multiselect and store the results in a single dictionary
            # for option in bridge_site_selection:
            #     self.bridge_site_selection_dict[option] = st.selectbox(option, options=['Yes', 'No'])
            for option in bridge_site_selection:
                self.bridge_site_selection_dict[option] = 'Yes'    # For now we just set all the options to 'Yes'

                # Create a numeric input for the height difference between the abutments
                if option == 'Height difference between abutments (m)':
                    height_difference_abutments = st.number_input('Height difference between abutments (m)',
                                                                  min_value=0.0, max_value=100.0, value=0.0, step=0.1)
                    self.filter_on_height_difference_abutments(height_difference_abutments)

                st.markdown(f"**{option}**: {self.bridges_evaluation.loc[option, 'Meaning']}\n")  # Display the *

        with col3:
            st.subheader('Wider Transport Network')
            # st.expander('Explanation will go here', expanded=False)
            wider_context_options = (self.bridges_evaluation.loc[
                                         self.bridges_evaluation['Type of variable'] == 'Wider Transport Network']
                                            .index.tolist())

            # Create a multiselect for the wider context options
            wider_context_selection = st.multiselect('Select the wider context options', options=wider_context_options)

            # Create a selectbox for the each selected option in the multiselect and store the results in a single dictionary
            # for option in wider_context_selection:
            #     self.wider_context_selection_dict[option] = st.selectbox(option, options=['Yes', 'No'])
            for option in wider_context_selection:
                self.wider_context_selection_dict[option] = 'Yes'    # For now we just set all the options to 'Yes'
                st.markdown(f"**{option}**: {self.bridges_evaluation.loc[option, 'Meaning']}\n")  # Display the
                # explanation of the options selected


        # # Make the graph
        graphGeneration = graph_generation(self.bridge_itself_selection_dict, self.bridge_site_selection_dict,
                                           self.wider_context_selection_dict, self.decision_points_selection_dict,
                                           self.bridges_evaluation)
        graphGeneration.make_graph()

        # # Download Button
        # st.button('Download Report', on_click=self.download_report())

    def download_report(self):
        # Create a button, which when clicked will send the span and the total costs to report_builder
        report_builder(self.material_quantities_costs.span_slider, self.total_costs)


    def evaluation_page_rendering(self):
        # Render the main page
        self.main_page()



if __name__ == '__main__':
    dashboard = dashboard_evaluation()
    dashboard.evaluation_page_rendering()
