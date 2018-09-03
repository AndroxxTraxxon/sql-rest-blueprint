class AbstractFileBuilder:

    @classmethod
    def buildAPIFile(cls, src, destFolder, options, dbModel):
        raise NotImplementedError()

    @classmethod
    def buildTableFile(cls, src, destFolder, options, dbModel):
        raise NotImplementedError()
                        
    @classmethod
    def processReplacement(cls, options, subject, text):
        raise NotImplementedError()

    @classmethod
    def getReplacementText(cls, varKey, options, subject = None):
        raise NotImplementedError()