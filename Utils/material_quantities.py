import pandas as pd
from collections import namedtuple
from dotmap import DotMap
from Utils.utils import *


class materialQuantities:
    """This class contains methods for calculating the quantities of materials required for the construction of a bridge
    of a given span."""
    def __init__(self, span_input):
        self.span = span_input
        # self.masonry_bridge_quantities = namedtuple('masonryBridgeQuantities', ['stone_vol', 'cement_mass', 'skilled_labour_man_days',
        #                                                                         'unskilled_labour_man_days'])
        # self.box_culvert_quantities = namedtuple('boxCulvertQuantities', ['steel_mass', 'cement_mass', 'sand_vol', 'aggregate_vol',
        #                                                                     'skilled_labour_man_days', 'unskilled_labour_man_days'])
        # self.unvented_ford_quantities = namedtuple('unventedFordQuantities', ['steel_mass', 'cement_mass', 'sand_vol', 'aggregate_vol',
        #                                                                         'skilled_labour_man_days', 'unskilled_labour_man_days'])
        # self.suspended_bridge_quantities = namedtuple('suspendedBridgeQuantities', ['skilled_labour', 'unskilled_labour'])
        self.masonry_bridge_quantities = DotMap()
        self.box_culvert_quantities = DotMap()
        self.unvented_ford_quantities = DotMap()
        self.suspended_bridge_quantities = DotMap()
        self.suspension_bridge_quantities = DotMap()
        self.all_quantities = DotMap()

    def masonry_bridge(self):
        # The maximum bridge span for a masonry bridge is 20m. If the span is greater than 20m, return a tuple of zeros
        if self.span > 20:
            self.masonry_bridge_quantities.stone_vol = 1E9
            self.masonry_bridge_quantities.cement_mass = 1E9
            self.masonry_bridge_quantities.skilled_labour = 1E9
            self.masonry_bridge_quantities.unskilled_labour = 1E9

            # Store in all
            self.all_quantities.masonry_bridge = self.masonry_bridge_quantities
        else:
            # The formula for the concrete quantities was obtained from the work by Paul Dequeker, Architect. It was reprinted
            # in the BTC Uganda stone masonry bridge manual.
            if self.span <= 15:
                self.masonry_bridge_quantities.stone_vol = 0.0746 * self.span ** 2 + 1.2381 * self.span + 1.0126
            elif self.span <= 20:
                self.masonry_bridge_quantities.stone_vol = 0.0691 * self.span ** 2 + 1.4238 * self.span + 1.4175


            # The following volumes are derived straight from the BTC Uganda Manual
            self.masonry_bridge_quantities.cement_mass = 1.65 * 50 * self.masonry_bridge_quantities.stone_vol
            self.masonry_bridge_quantities.skilled_labour = self.masonry_bridge_quantities.stone_vol/1.45
            self.masonry_bridge_quantities.unskilled_labour = self.masonry_bridge_quantities.stone_vol/1.45 * 2

            # Store in all_quantities
            self.all_quantities.masonry_bridge = self.masonry_bridge_quantities

    def box_culvert(self):
        # The maximum bridge span for a box culvert is 15m. If the span is greater than 15m, return a tuple of zeros
        if self.span > 15:
            self.box_culvert_quantities.steel_mass = 1E9
            self.box_culvert_quantities.cement_mass = 1E9
            self.box_culvert_quantities.sand_vol = 1E9
            self.box_culvert_quantities.aggregate_vol = 1E9
            self.box_culvert_quantities.skilled_labour = 1E9
            self.box_culvert_quantities.unskilled_labour = 1E9
            # Store in all_quantities
            self.all_quantities.box_culvert = self.box_culvert_quantities
        else:
            # The equations for box culvert volumes are taken from Fragkakis et al. (2015). Some assumptions have been
            # made for the net height of overburden (h_over), the net height of the box culvert (h_net), and the thickness
            # of the box culvert walls (which is used to compute b_net).
            h_over = 3       # Reasonable assumption
            h_net = 3        # Approximate average of h_net terms in Fragkakis et al. (2015)
            b_net = self.span - 1  # Based on assuming that the thickness of walls is 500mm, which is reasonable since
            # the minimum thickness of walls in the Wisconsin DOT standard is 250mm for a 10ft high box culvert

            # The following equations are taken from Fragkakis et al. (2015)
            concrete_vol = -4.083 + 2.459 * b_net + 0.673 * h_net + 0.216 * h_over
            self.box_culvert_quantities.steel_mass = -562.023 + 284.674 * b_net + 98.080 * h_net + 20.913 * h_over

            # # Minimum is 0 for both steel and concrete
            # if self.box_culvert_quantities.steel_mass < 0:
            #     self.box_culvert_quantities.steel_mass = 0
            # if concrete_vol < 0:
            #     concrete_vol = 0

            # The conversions from concrete volumes to quantities of cement, sand, and aggregate are taken from the
            # unit labour cost derivation obtained from interviews (assumed concrete class = C30).
            self.box_culvert_quantities.cement_mass = concrete_vol * 9.4 * 50
            self.box_culvert_quantities.sand_vol = concrete_vol * 0.28
            self.box_culvert_quantities.aggregate_vol = concrete_vol * 0.58
            self.box_culvert_quantities.skilled_labour = concrete_vol * 5/8    # assume 5man-hours to produce 1m3 of concrete and an 8 hour work day
            self.box_culvert_quantities.unskilled_labour = concrete_vol * 15/8  # assume 15man-hours to produce 1m3 of concrete and an 8 hour work
            # day
            # Store in all_quantities
            self.all_quantities.box_culvert = self.box_culvert_quantities

    def unvented_ford(self):
        # Quantities based on a standard unvented ford design proviced in the Iowa LWSC manual.
        # Thickness = 8 inches (200mm)
        # Reinforcement = #5 bars (16mm dia) at 12 inches (300mm) on center = 5.2kg/m length
        # Assume Concrete class = C25
        concrete_vol = self.span * 1.2 * 0.25     # Factor of 1.2 to deal with the fact that the length along the
        # streambed is greater than the span of the bridge
        self.unvented_ford_quantities.cement_mass = concrete_vol * 7.3 * 50
        self.unvented_ford_quantities.sand_vol = concrete_vol * 0.32
        self.unvented_ford_quantities.aggregate_vol = concrete_vol * 0.66
        self.unvented_ford_quantities.steel_mass = self.span * 5.2 * 1.2
        self.unvented_ford_quantities.skilled_labour = concrete_vol * 5 / 8    # assume 5man-hours to produce 1m3 of concrete and an 8 hour work day
        self.unvented_ford_quantities.unskilled_labour = concrete_vol * 15 / 8  # assume 15man-hours to produce 1m3 of concrete and an 8 hour work day

        # Store in all_quantities
        self.all_quantities.unvented_ford = self.unvented_ford_quantities

    def suspended_bridge(self):
        # The quantities for skilled and unskilled man-days are taken from the Helvetas manual for the construction of
        # suspended bridges.
        self.suspended_bridge_quantities.skilled_labour = self.span * 1.3 + 400
        self.suspended_bridge_quantities.unskilled_labour = self.span * 1.3 + 1300

        # Store in all_quantities
        self.all_quantities.suspended_bridge = self.suspended_bridge_quantities
    
    def suspension_bridge(self):
        # The quantities for skilled and unskilled man-days are taken from the Helvetas manual for the construction of
        # suspension bridges.
        self.suspension_bridge_quantities.skilled_labour = self.span * 1.3 + 400
        self.suspension_bridge_quantities.unskilled_labour = self.span * 1.3 + 1300

        # Store in all_quantities
        self.all_quantities.suspension_bridge = self.suspension_bridge_quantities


    def calculate_quantities(self):
        self.masonry_bridge()
        self.box_culvert()
        self.unvented_ford()
        self.suspended_bridge()
        self.suspension_bridge()

        # Format all quantities
        # Make dataframe
        self.all_quantities = (
            pd.DataFrame.from_dict(self.all_quantities, orient='columns')
                               .rename(index={'cement_mass': 'Cement (kg)', 'sand_vol': 'Sand (m3)', 'aggregate_vol': 'Aggregate (m3)',
                                'steel_mass': 'Steel (kg)', 'stone_vol': 'Masonry Stone (m3)',
                                'skilled_labour': 'Skilled Labour (man-days)', 'unskilled_labour': 'Unskilled Labour (man-days)'
                                              })
                               )

        # Drop the _typ row
        self.all_quantities.drop(['_typ'], inplace=True)

        # Round off to 1 decimal place
        self.all_quantities = self.all_quantities.reset_index().applymap(round_non_nan, decimals=1)

        # Rename columns
        self.all_quantities = (
            self.all_quantities
                .rename(columns={'masonry_bridge': 'Masonry Stone Arch Bridge',
                                'suspended_bridge': 'Suspended Cable Bridge', 'unvented_ford':
                                'Reinforced Concrete Unvented Ford', 'box_culvert': 'Box Culvert',
                                 'suspension_bridge': 'Suspension Bridge',
                                 'index': 'Material',
                                 })
            )





    def to_dict(self):
        # Return dictionary of all parameter values
        return self.__dict__

    def __repr__(self):
        # Return dictionary of all parameter values
        return repr(self.__dict__)





if __name__ == '__main__':
    test = materialQuantities(4)
    test.masonry_bridge()
    test.box_culvert()
    test.unvented_ford()
    test.suspended_bridge()
    print(test.masonry_bridge_quantities)
    print(test.box_culvert_quantities)
    print(test.unvented_ford_quantities)
    print(test.suspended_bridge_quantities)
