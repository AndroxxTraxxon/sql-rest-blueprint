from . import KeyType
from structure.Column import Column

class Table:
    
    def __init__(self, name, columns = list(), isRelationalTable = False):
        self.columns = dict()
        self.name = name
        self.primaryKey = None
        self.isRelationalTable = isRelationalTable
        if (not isinstance(self.name, str)) or (len(self.name) == 0):
            raise ValueError("Table name must be a non-empty str")
        
        if (not self.isRelationalTable) and (self.name.find("rltn") == (len(self.name) - len("rltn"))):
            self.isRelationalTable = True
        columnNames = list()
        for column in columns:
            addColumn(column)

    def addColumn(self, column):
        if column.name in self.columns.keys():
            raise ValueError("Column names must be unique")
                
        self.columns[column.name] = column
        if column.keyType == KeyType.PRIMARY:
            if self.primaryKey is None:
                self.primaryKey = column
            elif isinstance(self.primaryKey, Column):
                self.primaryKey.keyType = KeyType.COMPOSITE_PRIMARY
                column.keyType = KeyType.COMPOSITE_PRIMARY
                self.primaryKey = list((self.primaryKey, column))
            elif isinstance(self.primaryKey, list):
                column.keyType = KeyType.COMPOSITE_PRIMARY
                self.primaryKey.append(column)

    def __str__(self):
        output = "Table '{0}': [\n".format(self.name + (" (Relational)" if self.isRelationalTable else ""))
        for column in self.columns:
            output += "        " + str(column) + "\n"
        return output + "    ]"
            
