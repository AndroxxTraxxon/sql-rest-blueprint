import sys
import os
from db.mysql import MySQLParser

import pprint
import shutil
import re
import glob


def generalUsage():
    print("Here's some useful usage docs!")


def usage(cmd:str = None):
    if cmd is None:
        generalUsage()
    elif cmd == 'source':
        print("Here's some useful usage docs for `source`")
    elif cmd == 'dest':
        print("Here's some useful usage docs for `dest`")
    elif cmd == 'apiName':
        print("Here's some useful usage docs for `name`")
    elif cmd == 'lang':
        print("Here's some useful usage docs for `name`")
    else:
        generalUsage()
    exit()

def configDefaults():
    config = dict()
    config['cwd'] = os.getcwd()
    config['verbose'] = False
    config['srcType'] = 'file'
    config['dbType'] = 'mysql'
    config['srcRelPath'] = 'init.sql'
    config['destRelPath'] = 'api_name'
    config['apiName'] = 'api_name'
    config['fileExtensions'] = dict()
    config['fileExtensions']['php'] = 'php'
    config['fileExtensions']['python'] = 'py'
    config['fileExtensions']['java'] = 'java'
    return config

def parseArgs():
    _ , *args = sys.argv
    config = configDefaults()
    if len(args) == 0:
        print("No arguments found. Continuing with defaults...")
        return config
    if args[0] == 'help':
        usage()
    """ Parse all the args from the cli"""
    while len(args) > 0:
        currentArg, *args = args
        if(currentArg == '-s' or currentArg == '--source'):
            if len(args) > 0:
                config['srcRelPath'], *args = args
            else:
                usage('source')
        elif(currentArg == '-d' or currentArg == '--dest'):
            if len(args) > 0:
                arg, *args = args
                config['destRelPath'] = arg
                if config['apiName'] == configDefaults()['apiName']:
                    config['apiName'] = str(arg).split('/')[-1]
            else:
                usage('dest')
        elif(currentArg == '-v' or currentArg == '--verbose'):
            config['verbose'] = True
        elif(currentArg == '-n' or currentArg == '--name'):
            if len(args) > 0:
                config['apiName'], *args = args
            else:
                usage('name')
        elif(
            currentArg == '-l' or 
            currentArg == '--lang' or 
            currentArg == '--language'):
            if len(args) > 0:
                config['lang'], *args = args
            else:
                usage('lang')
        else:
            usage()
    
    validateConfig(config)

    return config

def validateConfig(config):
    """ Verify that the configs are enough to generate a file. """
    # language
    if config['lang'] not in config['fileExtensions'].keys():
        print("Appropriate language not specified.")
        exit()

def findSourcefile(config):
    print(config['cwd'], config['srcRelPath'])
    fileCandidate = os.path.join(config['cwd'], config['srcRelPath'])
    if os.path.exists(fileCandidate):
        config['srcAbsPath'] = fileCandidate
    else:
        print("Could not find file `{0}`. \nLooking for another possibility...".format(fileCandidate))
        """ Go looking for a .sql file, only in the cwd """
        fileSearchPath = os.path.join(config['cwd'], '*.sql')
        print("Searching {0} for files...".format(fileSearchPath))
        potentialFiles = glob.glob(fileSearchPath)
        if len(potentialFiles) > 0:
            fileCandidate = potentialFiles[0]
            print("Using `{0}` as db structure source.".format(fileCandidate))
            config['srcAbsPath'] = fileCandidate
        else:
            print("Could not find any sql file in `{0}`".format(config['cwd']))
            exit()

def updateConfigFromDatabase(config, dbModel):
    """ Check if it's default. If it is, override with parsed values from db. """
    if config['apiName'] == 'api_name':
        config['apiName'] = dbModel.name
    """ Check if it's default. If it is, override with parsed values from db. """
    if config['destRelPath'] == 'api_name': 
        config['destRelPath'] = dbModel.name
    config['libroot'] = os.path.dirname(os.path.realpath(__file__))
    config['destAbsPath'] = os.path.join(config['cwd'],config['destRelPath'])
    config['templateRoot'] = os.path.join(config['libroot'],'builder',config['lang'],'src')

def buildFolderStructure(config, dbModel):
    tableNameVarPattern = re.compile('\\{\\{\\$([a-z\\_]+)\\}\\}')

    """ create a directory at the destination """
    if not os.path.isdir(config['destAbsPath']):
        os.mkdir(config['destAbsPath'])


    var_pattern = re.compile(r"\{\{\$([a-zA-Z\_]+)\}\}")
    for root, dirs, files in os.walk(config['templateRoot']):
        
        """
        Make all of the directories in the template source.
        """
        for name in dirs:
            
            relpath = os.path.relpath(os.path.join(root, name), config['templateRoot']).split(os.path.sep)
            for i in range(len(relpath)):
                if var_pattern.match(relpath[i]) is not None:
                    relpath[i] = getTableFileBuilder(config['lang']).processReplacement(config, dbModel, relpath[i])
            relpath = os.path.join(*relpath)
            if not os.path.isdir(os.path.join(config['destAbsPath'],relpath)):
                os.mkdir(os.path.join(config['destAbsPath'],relpath))
        """
        Copy all of the generic supporting files from the template.
        """
        for name in files:
            """ If the path has variables, then pre-process the variable names. """
            relpath = os.path.relpath(os.path.join(root, name), config['templateRoot']).split(os.path.sep)
            for i in range(len(relpath)-1): # -1 so that the file name is not included. this will be processed later.
                if var_pattern.match(relpath[i]) is not None:
                    relpath[i] = getTableFileBuilder(
                        config['lang']
                    ).processReplacement(
                        config, dbModel, relpath[i])
            relpath = os.path.join(*relpath)
            if os.path.exists(os.path.join(config['destAbsPath'],relpath)):
                print(
                    "Overwriting file `{0}`".format(
                        os.path.join(
                            config['destAbsPath'],
                            relpath)))
            
            """ Figure out what kind of file this is. """
            fileEnding = config['fileExtensions'][config['lang']]
            templateFileEnding = '.template.'+config['fileExtensions'][config['lang']]
            if not (name.find(templateFileEnding) == len(name) - len(templateFileEnding)):
                """ 
                Completely generic files. Not templated, with static names.

                Not templated at all. 
                Just need to be copied (not ending in `.template.*`)
                """
                shutil.copy(os.path.join(root, name), config['destAbsPath']+'/'+relpath)
            elif tableNameVarPattern.match(name) is None :
                """ 
                API-specific files, not specifically named after API, 
                but needed in to support the package

                Ending in `.template.*, but only one instance of these. 
                Does not have a generated variable name in it.
                """
                newFileName = name[0:len(name) - len(templateFileEnding) + 1] + fileEnding
                oldFilePath = os.path.join(root, name)
                newFilePath = os.path.join(config['destAbsPath'], relpath[0:-len(name)])
                print(
                    "Make General File ::", 
                    name, 
                    '\n             --->', 
                    os.path.join(newFilePath, newFileName)
                )
                processGenericFile(
                    oldFilePath,
                    newFilePath,
                    config,
                    dbModel
                )
            else:
                """
                Table-specific files.
                This file type is designated by containing one of the {{$*}} variable tags, 
                as well as the `.template.*` ending. One will be made for each table in the db.
                """
                newFileName = name[0:len(name) - len(templateFileEnding) + 1] + fileEnding
                newFileNameStar = tableNameVarPattern.sub(r'*', newFileName)
                oldFilePath = os.path.join(root, name)
                newFolderPath = os.path.join(config['destAbsPath'], relpath[0:-(len(name)+1)])
                print(
                    "Make Table Files  ::",
                    name, 
                    '\n             --->', 
                    os.path.join(newFolderPath, newFileNameStar)
                )
                processTableFile(
                    oldFilePath,
                    newFolderPath,
                    config,
                    dbModel
                )

def processGenericFile(src, destFolder, config, dbModel):
    fileBuilder = getTableFileBuilder(config['lang'])
    if fileBuilder is not None:
        fileBuilder.buildAPIFile(src, destFolder, config, dbModel)
    else:
        raise NotImplementedError("Internal Error: API File builder for `{0}` not found.".format(config['lang']))

def getTableFileBuilder(language):
    if language == 'php':
        import builder.php
        return builder.php.PHPTableFileBuilder
    return None
    

def processTableFile(src, destFolder, config, dbModel):
    fileBuilder = getTableFileBuilder(config['lang'])
    if fileBuilder is not None:
        fileBuilder.buildTableFile(src, destFolder, config, dbModel)
    else:
        raise NotImplementedError("Internal Error: Table file builder for `{0}` not found.".format(config['lang']))


if __name__ == "__main__":
    config = parseArgs()
    findSourcefile(config)
    dbModel = MySQLParser.buildFromFile(config['srcAbsPath'])
    updateConfigFromDatabase(config, dbModel)
    buildFolderStructure(config, dbModel)



