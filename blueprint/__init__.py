import sys, os, pprint, shutil, re, glob, copy

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

class BlueprintHelper:
    defaults = {
        'cwd': os.getcwd(),
        'verbose': False,
        'srcType': 'file',
        'dbType': 'mysql',
        'src': {
            'rel': 'init.sql',
            'abs': None
        },
        'dest': {
            'rel': 'api_name',
            'abs': None
        },
        'apiName': 'api_name',
        'languages': {
            'php':{
                'fileEnding': 'php'
            },
            'python':{
                'fileEnding': 'py'
            },
            'java':{
                'fileEnding': 'java'
            }
        }
    }

    db = None
    fileBuilder = None

    def parseArgs(self):
        _, *args = sys.argv
        self.config = copy.deepcopy(self.defaults)
        if len(args) == 0:
            print("No arguments found. Continuing with defaults...")
            return
        if args[0] == 'help':
            usage()
        """ Parse all the args from the cli"""
        while len(args) > 0:
            currentArg, *args = args
            if(currentArg == '-s' or currentArg == '--source'):
                if len(args) > 0:
                    self.config['src']['rel'], *args = args
                else:
                    usage('source')
            elif(currentArg == '-d' or currentArg == '--dest'):
                if len(args) > 0:
                    arg, *args = args
                    self.config['dest']['rel'] = arg
                else:
                    usage('dest')
            elif(currentArg == '-v' or currentArg == '--verbose'):
                self.config['verbose'] = True
            elif(currentArg == '-n' or currentArg == '--name'):
                if len(args) > 0:
                    self.config['apiName'], *args = args
                else:
                    usage('name')
            elif(
                currentArg == '-l' or 
                currentArg == '--lang' or 
                currentArg == '--language'):
                if len(args) > 0:
                    self.config['lang'], *args = args
                else:
                    usage('lang')
            else:
                print('Unknown argument: {0}'.format(currentArg))
                usage()
        
        self.validateConfig()

    def validateConfig(self):
        """ Verify that the configs are enough to generate a file. """
        # language
        if self.config['lang'] not in self.config['languages'].keys():
            print("Appropriate language not specified")
            print("Acceptable languages are as follows...")
            pprint.pprint(self.config['fileExtensions'])
            raise ValueError("Unrecognized language: {0}".format(self.config['lang']))

    def findSource(self):
        if self.config['srcType'] == 'file':
            self.findSourceFile()
        elif self.config['srcType'] == 'server':
            self.findSourceServer()
        else:
            raise ValueError("Unknown SQL source type: {0}".format(self.config['srcType']))
        
    def findSourceFile(self):
        """ Look for  """
        print(self.config['cwd'], self.config['src']['rel'])
        fileCandidate = os.path.join(self.config['cwd'], self.config['src']['rel'])
        if os.path.exists(fileCandidate):
            self.config['src']['abs'] = fileCandidate
        else:
            print("Could not find file `{0}`. \nLooking for another possibility...".format(fileCandidate))
            """ Go looking for a .sql file, only in the cwd """
            fileSearchPath = os.path.join(self.config['cwd'], '*.sql')
            print("Searching {0} for files...".format(fileSearchPath))
            potentialFiles = glob.glob(fileSearchPath)
            if len(potentialFiles) > 0:
                fileCandidate = potentialFiles[0]
                print("Using `{0}` as db structure source.".format(fileCandidate))
                self.config['src']['abs'] = fileCandidate
            else:
                print("Could not find any sql file in `{0}`".format(self.config['cwd']))
                exit()

    def findSourceServer(self):
        raise NotImplementedError("SQL Server integration has not been implemented.")

    def readDatabase(self):
        raise NotImplementedError("SQL Server integration has not been implemented.")

    def updateConfigFromDatabase(self):
        """ Check if it's default. If it is, override with parsed values from db. """
        if self.config['apiName'] == self.defaults['apiName']:
            print("Overriding Default API Name to `{0}`".format(self.db.name))
            self.config['apiName'] = self.db.name
        """ Check if it's default. If it is, override with parsed values from db. """
        if self.config['dest']['rel'] == self.defaults['dest']['rel']: 
            print("Overriding Default rel Destination to `{0}`".format(self.db.name))
            self.config['dest']['rel'] = self.db.name
        self.config['libroot'] = os.path.dirname(os.path.realpath(__file__))
        self.config['dest']['abs'] = os.path.join(self.config['cwd'],self.config['dest']['rel'])
        self.config['templateRoot'] = os.path.join(self.config['libroot'],'builder',self.config['lang'],'src')
    
    def getSQLFileParser(self):
        if isinstance (self.config['dbType'], str):
            if self.config['dbType'].lower() == 'mysql':
                import blueprint.db.mysql
                return blueprint.db.mysql.MySQLFileParser

    def getDBModel(self):
        if isinstance(self.config['srcType'], str):
            if self.config['srcType'] == 'file':
                fileParser = self.getSQLFileParser()(self.config['src']['abs'])
                
                self.db = fileParser.getDB()
        else:
            raise ValueError("SQL source type (srcType) must be a `str`.")

    def configureFileBuilder(self):
        if isinstance(self.config['lang'], str):
            if self.config['lang'] == 'php':
                import blueprint.builder.php
                self.fileBuilder = blueprint.builder.php.PHPFileBuilder
            else:
                raise NotImplementedError("Language {0} has no specified file builder.".format(self.config['lang']))

    def buildFileStructure(self):
        tableNameVarPattern = re.compile('\\{\\{\\$([a-z\\_]+)\\}\\}')
        if self.fileBuilder is None:
            self.configureFileBuilder()

        """ create a directory at the destination """
        if not os.path.isdir(self.config['dest']['abs']):
            os.mkdir(self.config['dest']['abs'])


        var_pattern = re.compile(r"\{\{\$([a-zA-Z\_]+)\}\}")
        for root, dirs, files in os.walk(self.config['templateRoot']):
            
            """
            Make all of the directories in the template source.
            """
            for name in dirs:
                
                rel = os.path.relpath(os.path.join(root, name), self.config['templateRoot']).split(os.path.sep)
                for i in range(len(rel)):
                    if var_pattern.search(rel[i]) is not None:
                        rel[i] = self.fileBuilder.processReplacement(self.config, self.db, rel[i])
                rel = os.path.join(*rel)
                if not os.path.isdir(os.path.join(self.config['dest']['abs'], rel)):
                    os.mkdir(os.path.join(self.config['dest']['abs'], rel))
            """
            Copy all of the generic supporting files from the template.
            """
            for name in files:
                """ If the path has variables, then pre-process the variable names. """
                rel = os.path.relpath(os.path.join(root, name), self.config['templateRoot']).split(os.path.sep)
                for i in range(len(rel)-1): # -1 so that the file name is not included. this will be processed later.
                    if var_pattern.search(rel[i]) is not None:
                        rel[i] = self.fileBuilder.processReplacement(
                            self.config, 
                            self.db, 
                            rel[i]
                        )
                if os.path.exists(os.path.join(self.config['dest']['abs'], *rel)):
                    print(
                        "Overwriting file `{0}`".format(
                            os.path.join(
                                self.config['dest']['abs'],
                                *rel)))
                """ Figure out what kind of file this is. """
                fileEnding = self.config['languages'][self.config['lang']]['fileEnding']
                templateFileEnding = '.template.'+fileEnding
                if not (name.find(templateFileEnding) == len(name) - len(templateFileEnding)):
                    """ 
                    Completely generic files. Not templated, with static names.

                    Not templated at all. 
                    Just need to be copied (not ending in `.template.*`)
                    """
                    shutil.copy(os.path.join(root, name), os.path.join(self.config['dest']['abs'],*rel))
                elif tableNameVarPattern.search(name) is None :
                    """ 
                    API-specific files, not specifically named after API, 
                    but needed in to support the package

                    Ending in `.template.*, but only one instance of these. 
                    Does not have a generated variable name in it.
                    """
                    newFileName = name[0:len(name) - len(templateFileEnding) + 1] + fileEnding
                    oldFilePath = os.path.join(root, name)
                    newFilePath = os.path.join(self.config['dest']['abs'], *(rel[0:-1]))
                    print(
                        "Make General File ::", 
                        name, 
                        '\n             --->', 
                        os.path.join(newFilePath, newFileName)
                    )
                    self.processGenericFile(
                        oldFilePath,
                        newFilePath
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
                    newFolderPath = os.path.join(self.config['dest']['abs'], *(rel[0:-1]))
                    print(
                        "Make Table Files  ::",
                        name, 
                        '\n             --->', 
                        os.path.join(newFolderPath, newFileNameStar)
                    )
                    self.processTableFile(
                        oldFilePath,
                        newFolderPath,
                    )

    def processGenericFile(self, src, destFolder):
        if self.fileBuilder is None:
            self.configureFileBuilder()
        if self.fileBuilder is not None:
            self.fileBuilder.buildAPIFile(src, destFolder, self.config, self.db)
        else:
            raise NotImplementedError("Internal Error: API File builder for `{0}` not found.".format(self.config['lang']))

    
    def processTableFile(self, src, destFolder):
        if self.fileBuilder is None:
            self.configureFileBuilder()
        if self.fileBuilder is not None:
            self.fileBuilder.buildTableFile(src, destFolder, self.config, self.db)
        else:
            raise NotImplementedError("Internal Error: Table file builder for `{0}` not found.".format(self.config['lang']))


