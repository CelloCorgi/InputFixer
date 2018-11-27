"""
This file contains the Logging class which loads all given config information for InputFixer
"""

class Logger:

    def __init__(self, inFix_config):
        """
        This function initilizes the log by setting up a folder named by the current time in the
        specified log folder
        """
        self.log_folder = inFix_config.get_log_folder_path()
        self.session = inFix_config.get_session_path()
        self.config_info = inFix_config

        # Now make a log file folder in the specified location

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
