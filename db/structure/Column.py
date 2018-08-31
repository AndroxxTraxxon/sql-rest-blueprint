from . import KeyType

class Column:
    def __init__(self, name, dataType, notNull= False, keyType = KeyType.NONE):
        self.name = name
        self.dataType = dataType
        self.notNull = notNull
        self.keyType = keyType

    def __str__(self):
        return "Column '{0}': {1}".format(
            self.name,
            self.dataType + 
            (" NOT NULL" if self.notNull else "") +
            (" "+str(self.keyType) if self.keyType != KeyType.NONE else "")
        )