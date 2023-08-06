import pandas as pd
from dotmap import DotMap

class defaultCosts:
    # A class to store the default costs from the excel sheet of data
    def __init__(self, path):
        self.linear_m_costs = pd.read_excel(path, sheet_name='Per linear m costs', header=0, index_col=0)
        self.lump_sum_costs = pd.read_excel(path, sheet_name='Lumpsum costs', header=0, index_col=0)
        self.unit_costs = pd.read_excel(path, sheet_name='Default Unit Costs', header=0, index_col=0)

        # Store the specific linear m costs as attributes of the class
        self.steel_decking = self.linear_m_costs.loc['Steel Decking', 'Per linear m cost (USD)']
        self.crossbeams_bolts = self.linear_m_costs.loc['Crossbeams + Bolts', 'Per linear m cost (USD)']
        self.fencing = self.linear_m_costs.loc['Fencing System', 'Per linear m cost (USD)']
        # self.ramp_post = self.linear_m_costs.loc['Ramp Post System', 'Per linear m cost (USD)']
        self.restraint_handrail = self.linear_m_costs.loc['Restraint and Handrail Wires', 'Per linear m cost (USD)']
        self.cables_clips = self.linear_m_costs.loc['Cables and Clips', 'Per linear m cost (USD)']

        # Store the specific lump sum costs as attributes of the class
        self.concrete_works_suspended_bridge = self.lump_sum_costs.loc['Concrete Works', 'Lumpsum cost (USD)']
        self.steel_reinf_suspended_bridge = self.lump_sum_costs.loc['Steel Reinforcement', 'Lumpsum cost (USD)']

        # Store the specific unit costs as attributes of the class
        self.cement_cost = self.unit_costs.loc['Cement Cost/50kg bag (USD)', 'Unit cost']
        self.steel_cost = self.unit_costs.loc['Steel Cost/kg (USD)', 'Unit cost']
        self.skilled_labor_cost = self.unit_costs.loc['Skilled Labor Cost/man-day (USD)', 'Unit cost']
        self.masonry_cost = self.unit_costs.loc['Masonry Cost/m3 (USD)', 'Unit cost']
        self.sand_cost = self.unit_costs.loc['Sand Cost/m3 (USD)', 'Unit cost']
        self.aggt_cost = self.unit_costs.loc['Aggregate (20mm) Cost/m3 (USD)', 'Unit cost']
        self.unskilled_labor_cost = self.unit_costs.loc['Unskilled Labor Cost/man-day (USD)', 'Unit cost']
