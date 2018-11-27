"""
This file contains the Logging class which loads all given config information for InputFixer
"""

class Logger:

    def __init__(self, inFix_config):
        print(inFix_config)

    def zip_raw_results(self):
        """
        This function zips up all the raw results and saves them in the file specified by config
        """
        pass

    def finalize_logs(self):
        """
        This function should always be the last call to a logger object
        It closes any open log_files associated with the instance
        """
        pass
