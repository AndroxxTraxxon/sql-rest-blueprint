from . import BlueprintHelper

helper = BlueprintHelper()
helper.parseArgs()
helper.findSource()
helper.getDBModel()
print(helper.db)
helper.updateConfigFromDatabase()
helper.buildFileStructure() 