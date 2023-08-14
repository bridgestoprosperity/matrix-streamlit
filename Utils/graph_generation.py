import pandas as pd
import streamlit as st
import os
import sys
import graphviz

# Add the file path to the sys.path list
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from Utils.utils import *

class graph_generation:
    def __init__(self, bridge_itself_selection_dict, bridge_site_selection_dict, wider_context_selection_dict,  decision_points_selection_dict,
                 bridges_evaluation):
        self.bridges_evaluation = bridges_evaluation  # The dataframe containing the evaluation info of all the bridges
        self.bridge_itself_selection_dict = bridge_itself_selection_dict  # Stores the 'bridge itself' selection
        self.bridge_site_selection_dict = bridge_site_selection_dict  # Stores the 'bridge site' selection
        self.wider_context_selection_dict = wider_context_selection_dict  # Stores the 'wider context' selection
        self.decision_points_selection_dict = decision_points_selection_dict  # Stores the output of all the decision points selected

        # The graph object
        self.graph = graphviz.Digraph('G', filename='decision_tree.gv', engine='dot', format='png')

        # Counters
        self.can_do_counter = 0  # Counter for the number of 'can do' nodes
        self.cannot_do_counter = 0  # Counter for the number of 'cannot do' nodes
        self.decision_counter = 0  # Counter for the number of decision nodes
        self.options_remaining_counter = 0  # Counter for the number of options remaining
        self.options_abandoned_counter = 0  # Counter for the number of options abandoned

        # Options remaining and abandoned

        self.options_remaining = break_and_get_unique(
            self.bridges_evaluation[['Options Remaining', 'Options Abandoned']])
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
                     in self.decision_points_selection_dict.keys()] +
                    [key for key in self.wider_context_selection_dict.keys() if key not
                        in self.decision_points_selection_dict.keys()])

        for key in new_keys:
            self.modify_options(key)
            self.decision_points_selection_dict[key] = {'Remaining': self.modify_options(key)[0],
                                                        'Abandoned': self.modify_options(key)[1]
                                                        }

    def can_be_node(self):
        # Make a diamond shaped graphviz node with 'Can be' inside
        self.can_do_counter += 1
        return self.graph.node(f'Can_{self.can_do_counter}', 'Recommended ', shape='diamond')

    def cannot_be_node(self):
        # Make a diamond shaped graphviz node with 'Cannot be' inside
        self.cannot_do_counter += 1
        return self.graph.node(f'Cant_{self.cannot_do_counter}', 'Not Recommended ', shape='diamond')

    def decision_node(self, decision_point):
        # Make a rectangular shaped graphviz node with the decision point inside
        self.decision_counter += 1
        return self.graph.node(f'Decision_{self.decision_counter}', decision_point, shape='rect')

    def options_remaining_node(self, options_remaining):
        # Make a rectangular shaped graphviz node with rounded corners and options_remaining inside
        self.options_remaining_counter += 1
        return self.graph.node(f'Remain_{self.options_remaining_counter}', options_remaining, shape='rect',
                               style='rounded')

    def options_abandoned_node(self, options_abandoned):
        # Make a rectangular shaped graphviz node with rounded corners and options_abandoned inside
        self.options_abandoned_counter += 1
        return self.graph.node(f'Abandon_{self.options_abandoned_counter}', options_abandoned, shape='rect',
                               style='rounded')

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
        # # # Saves the graph when running on local machine
        # self.graph.render(directory=os.getcwd()).replace('\\', '/')
        # st.image('decision_tree.gv.png')
        # # Display graph when running on streamlit cloud
        st.graphviz_chart(self.graph)
        # self.graph.render()    # Todo: In the final report, note that a workaround needs to be found to bundle
        # the dot command line tool with the app on GitHub.

    def make_graph(self):
        # Makes the graph
        self.update_keys_values()
        self.make_nodes()
        self.make_edges()
        self.save_display_graph()
