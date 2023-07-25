import pandas as pd
import streamlit as st
import os
import graphviz
from Utils.utils import *

os.environ["PATH"] += os.pathsep + r'C:\Program Files\Graphviz\bin'   #TODO: Comment this out before push

class dashboard_evaluation:
    def __init__(self):
        # Load data
        # self.bridges_evaluation = pd.read_excel(r'C:\Users\mwendwa.kiko\Documents\Personal_Kiko\E4C_Internship\Other_Docs\Dashboard_test\Excel Transcription of Data Analysis.xlsx', header=0, index_col=0, sheet_name='Decision Points')
        # That's for debugging, the one for display is below
        self.bridges_evaluation = pd.read_excel('Excel Transcription of Data Analysis.xlsx', header=0, index_col=0, sheet_name='Decision Points')
        self.bridge_itself_selection_dict = {}   # Stores the 'bridge itself' selection
        self.bridge_site_selection_dict = {}     # Stores the 'bridge site' selection
        self.decision_points_selection_dict = {} # Stores the output of all the decision points selected

        # The graph object
        self.graph = graphviz.Digraph('G', filename='decision_tree.gv', engine='dot', format='png')

        # Counters
        self.can_do_counter = 0     # Counter for the number of 'can do' nodes
        self.cannot_do_counter = 0  # Counter for the number of 'cannot do' nodes
        self.decision_counter = 0   # Counter for the number of decision nodes
        self.options_remaining_counter = 0    # Counter for the number of options remaining
        self.options_abandoned_counter = 0    # Counter for the number of options abandoned

        # Options remaining and abandoned

        self.options_remaining = break_and_get_unique(self.bridges_evaluation[['Options Remaining', 'Options Abandoned']])
        # self.options_remaining = []
        self.options_abandoned = []

    def modify_options(self, decision_pt):
        '''Based on the decision_pt, appends the options abandoned lists and removes them from the options remaining
        '''
        # remaining_here = self.bridges_evaluation.loc[decision_pt, 'Options Remaining'].split('; ')
        abandoned_here = self.bridges_evaluation.loc[decision_pt, 'Options Abandoned'].split('; ')

        # Append to the options abandoned list if not already there
        self.options_abandoned += [option for option in abandoned_here if option not in self.options_abandoned]

        # Remove from the options remaining list if there
        # self.options_remaining = [option for option in self.options_remaining if option not in abandoned_here]
        self.options_remaining = list(set(self.options_remaining) - set(abandoned_here))

        # Return a string of the options remaining and abandoned
        return ', '.join(self.options_remaining), ', '.join(abandoned_here)


    def update_keys_values(self):
        '''Check if there are any keys in the bridge_itself_selection_dict and bridge_site_selection_dict
        that are not in the decision_points_selection_dict'''
        new_keys = ([key for key in self.bridge_itself_selection_dict.keys() if key not
                     in self.decision_points_selection_dict.keys()] +
                    [key for key in self.bridge_site_selection_dict.keys() if key not
                        in self.decision_points_selection_dict.keys()])
        for key in new_keys:
            self.modify_options(key)
            self.decision_points_selection_dict[key] = {'Remaining': self.modify_options(key)[0],
                                                        'Abandoned': self.modify_options(key)[1]
                                                        }
    def can_be_node(self):
        # Make a diamond shaped graphviz node with 'Can be' inside
        self.can_do_counter += 1
        return self.graph.node(f'Can_{self.can_do_counter}', 'Can be ', shape='diamond')

    def cannot_be_node(self):
        # Make a diamond shaped graphviz node with 'Cannot be' inside
        self.cannot_do_counter += 1
        return self.graph.node(f'Cant_{self.cannot_do_counter}', 'Cannot be ', shape='diamond')

    def decision_node(self, decision_point):
        # Make a rectangular shaped graphviz node with the decision point inside
        self.decision_counter += 1
        return self.graph.node(f'Decision_{self.decision_counter}', decision_point, shape='rect')

    def options_remaining_node(self, options_remaining):
        # Make a rectangular shaped graphviz node with rounded corners and options_remaining inside
        self.options_remaining_counter += 1
        return self.graph.node(f'Remain_{self.options_remaining_counter}', options_remaining, shape='rect', style='rounded')

    def options_abandoned_node(self, options_abandoned):
        # Make a rectangular shaped graphviz node with rounded corners and options_abandoned inside
        self.options_abandoned_counter += 1
        return self.graph.node(f'Abandon_{self.options_abandoned_counter}', options_abandoned, shape='rect', style='rounded')

    def make_nodes(self):
        # Makes the nodes using the above functions and the data in the decision_points_selection_dict
        for key, value in self.decision_points_selection_dict.items():
            self.decision_node(key)
            self.cannot_be_node()
            self.can_be_node()
            self.options_remaining_node(value['Remaining'])
            self.options_abandoned_node(value['Abandoned'])

    def single_subgraph(self, counter_value):
        '''Creates a subgraph for the ith decision point'''
        self.graph.edge(f'Decision_{counter_value}', f'Can_{counter_value}')
        self.graph.edge(f'Decision_{counter_value}', f'Cant_{counter_value}')
        self.graph.edge(f'Can_{counter_value}', f'Remain_{counter_value}')
        self.graph.edge(f'Cant_{counter_value}', f'Abandon_{counter_value}')

    def make_edges(self):
        # Makes the edges between the nodes
        for counter_value in range(1, self.decision_counter + 1):
            if counter_value != 1:
                self.graph.edge(f'Remain_{counter_value - 1}', f'Decision_{counter_value}')
            if counter_value == 1:
                self.graph.edge('Start', f'Decision_{counter_value}')
            self.single_subgraph(counter_value)


    def save_display_graph(self):
        # # Saves the graph when running on local machine
        # self.graph.render(directory=os.getcwd()).replace('\\', '/')
        # st.image('decision_tree.gv.png')
        # Display graph when running on streamlit cloud
        st.graphviz_chart(self.graph)

    def main_page(self):
        # Create a container with 4 columns
        col1, col2, col3, col4 = st.columns(4)

        # Column 1
        with col1:
            st.subheader('Bridge Itself')
            st.expander('Explanation will go here', expanded=False)
            bridge_itself_options = self.bridges_evaluation.loc[self.bridges_evaluation['Type of variable'] == 'Bridge Itself']\
                .index.tolist()

            # Create a multiselect for the bridge itself options
            bridge_itself_selection = st.multiselect('Select the bridge itself options', options=bridge_itself_options)

            # Create a selectbox for the each selected option in the multiselect and store the results in a single dictionary

            for option in bridge_itself_selection:
                self.bridge_itself_selection_dict[option] = st.selectbox(option, options=['Yes', 'No'])

        with col2:
            st.subheader('Bridge Site')
            st.expander('Explanation will go here', expanded=False)
            bridge_site_options = self.bridges_evaluation.loc[self.bridges_evaluation['Type of variable'] == 'Bridge Site']\
                .index.tolist()

            # Create a multiselect for the bridge site options
            bridge_site_selection = st.multiselect('Select the bridge site options', options=bridge_site_options)

            # Create a selectbox for the each selected option in the multiselect and store the results in a single dictionary
            for option in bridge_site_selection:
                self.bridge_site_selection_dict[option] = st.selectbox(option, options=['Yes', 'No'])

        with col3:
            st.subheader('Wider Transport Network')
            st.expander('Explanation will go here', expanded=False)

        with col4:
            st.subheader('Stream Flow')
            st.expander('Explanation will go here', expanded=False)

        # Make the graph
        self.update_keys_values()
        self.make_nodes()
        self.make_edges()
        self.save_display_graph()




    def evaluation_page_rendering(self):
        # Config app
        apptitle = 'Evaluation Page'
        st.set_page_config(page_title=apptitle, page_icon=":eyeglasses:", layout='wide')
        st.title('Bridge Site Evaluation')

        self.main_page()

if __name__ == '__main__':
    dashboard = dashboard_evaluation()
    dashboard.evaluation_page_rendering()
