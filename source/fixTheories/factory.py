"""
This file generates an object of the appropriate theory.

IT MUST BE MODIFIED FOR ANY ADDED THEORY
ANY ADDED THEORY MUST IMPLEMENT THE .fix method
"""

import fixTheories.gInFix as gInFix

def get_theory_solver(theory_name):
    """
    This is the factory function - ya, I know this is hacky, but....
    """

    if theory_name == "gInFix": 
        return gInFix.GInFix()
    
    # TODO: Add custom theories here
    
    return None


