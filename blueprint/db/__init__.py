from blueprint.db.structure import KeyType

class AbstractSQLFileParser:

    def getDB(self):
        raise NotImplementedError("You must extend an abstract class.")

    def buildDB(self, name, tableTextList):
        raise NotImplementedError("You must extend an abstract class.") 

    def buildTable(self, name, content):
        raise NotImplementedError("You must extend an abstract class.")

    def buildColumn(self, name, dataType, nullity, keytype = KeyType.NONE):
        raise NotImplementedError("You must extend an abstract class.")
