from enum import Enum

class KeyType(Enum):
    NONE = 0
    PRIMARY = 1
    FOREIGN = 2
    COMPOSITE_PRIMARY = 3
    COMPOSITE_PRIMARY_FOREIGN = 5

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

class Table:
    def __init__(self, name, columns = dict(), isRelationalTable = False):
        self.columns = dict()
        self.name = name
        self.primaryKey = None
        self.isRelationalTable = isRelationalTable
        if (not isinstance(self.name, str)) or (len(self.name) == 0):
            raise ValueError("Table name must be a non-empty str")
        
        if (not self.isRelationalTable) and (self.name.find("rltn") == (len(self.name) - len("rltn"))):
            self.isRelationalTable = True
        for column in columns.values():
            self.addColumn(column)

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

    def __str__(self, indent=""):
        output = indent + "Table '{0}': [\n".format(self.name + (" (Relational)" if self.isRelationalTable else ""))
        for column in self.columns:
            output += indent +"    " + str(column) + "\n"
        return output + indent + "]"

class Database:

    def __init__(self, name, tables = dict(), dbType = 'mysql'):
        self.tables = tables
        self.name = name
        self.dbType = dbType
        if(self.name == ''):
            raise ValueError("Table name cannot be null")

    def addTable(self, table):
        if table.name in self.tables.keys():
            raise ValueError("Column names must be unique")
        self.tables[table.name]=table

    def __str__(self):
        output = "Database '{0}': [\n".format(self.name)
        for table in self.tables.values():
            output += table.__str__(indent = "    ") + "\n"
        return output + "]"