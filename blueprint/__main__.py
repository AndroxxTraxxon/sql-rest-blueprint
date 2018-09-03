from . import BlueprintHelper

helper = BlueprintHelper()
""" Parse the user CLI input """
helper.parseArgs() 
""" Find the source, whether it be a hosted server or a file """
helper.findSource()
""" Acquire db model from source, and build it in memory. """
helper.getDBModel()
""" Override appropriate settings if they were left as defaults."""
helper.updateConfigFromDatabase()
""" Build the file structure from the db model, given the current configuration"""
helper.buildFileStructure()