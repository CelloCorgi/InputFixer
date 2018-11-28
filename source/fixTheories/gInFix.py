"""
This file contains the GInFix class which uses a genprog like / fuzzing approach to fixing the errors
"""

import multiprocess

class GInFix:

    def fix(self, global_config, session_config, log):
        """
        This is the only method that should be called from outside this file
        It runs the overall fixer
        """
        # Convert the bad input into its modifiable datastructure form -> a list of lists
        self.original_bad_input = 

        # Initialize the cache with the original bad, so we don't try the same result twice
        self.cache = {session_config["BadInput"]}

    def generate_new_guess(self):
        pass

    def test_guess(self):
        pass
