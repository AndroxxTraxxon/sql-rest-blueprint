import sys
import os
from db.mysql import MySQLParser
import pprint
import shutil
import re


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
    else:
        generalUsage()
    exit()

def parseArgs():
    _ , *args = sys.argv
    config = dict()
    config['verbose'] = False
    config['srcRelPath'] = None
    config['destRelPath'] = './api_name'
    config['apiName'] = 'api_name'
    config['cwd'] = os.getcwd()
    config['lang'] = 'php'
    config['fileExtensions'] = dict()
    config['fileExtensions']['php'] = 'php'
    config['fileExtensions']['python'] = 'py'
    config['fileExtensions']['java'] = 'java'
    if args[0] == 'help':
        usage()
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
                if config['apiName'] == 'api_name':
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
            pass
        else:
            usage()

    if config['srcRelPath'] is None:
        usage()
    return config

def updateConfigFromDatabase(config, dbModel):
    if config['apiName'] == 'api_name':
        config['apiName'] = dbModel.name
    if config['destRelPath'] == './api_name':
        config['destRelPath'] = './{0}'.format(dbModel.name)
    config['libroot'] = os.path.dirname(os.path.realpath(__file__))
    config['destAbsPath'] = config['cwd']+'/'+config['destRelPath']
    config['templateRoot'] = config['libroot']+'/builder/'+config['lang']+'/src'

def buildFolderStructure(config):
    tableNameVarPattern = re.compile('\{\{\$([a-z\_]+)\}\}')
    if not os.path.isdir(config['destAbsPath']):
        os.mkdir(config['destAbsPath'])
    for root, dirs, files in os.walk(config['templateRoot']):
        for name in dirs:
            relpath = os.path.relpath(os.path.join(root, name), config['templateRoot'])
            if not os.path.isdir(config['destAbsPath']+'/'+relpath):
                os.mkdir(config['destAbsPath']+'/'+relpath)
        
        for name in files:
            relpath = os.path.relpath(os.path.join(root, name), config['templateRoot'])
            if not os.path.exists(config['destAbsPath']+'/'+relpath):
                fileEnding = config['fileExtensions'][config['lang']]
                templateFileEnding = '.template.'+config['fileExtensions'][config['lang']]
                if not (name.find(templateFileEnding) == len(name) - len(templateFileEnding)):
                    shutil.copy(os.path.join(root, name), config['destAbsPath']+'/'+relpath)
                elif tableNameVarPattern.match(name) is None :
                    newFileName = name[0:len(name) - len(templateFileEnding) + 1] + fileEnding
                    print(name)
                    processGenericFile(
                        os.path.join(root, name),
                        os.path.join(config['destAbsPath'], relpath[0:-len(name)], newFileName),
                        config
                    )

def processGenericFile(src, dest, config):
    api_name = re.compile('\{\{\$api_name\}\}')
    with open(src, "r") as template:
        with open(dest, "w+") as output:
            for line in template.readlines():
                newline = api_name.sub(config['apiName'], line)
                output.write(newline)


            


if __name__ == "__main__":
    config = parseArgs()
    dbModel = MySQLParser.buildFromFile(config['cwd'] + '/' + config['srcRelPath'])
    updateConfigFromDatabase(config, dbModel)
    buildFolderStructure(config)
    
    



