from enum import Enum

class KeyType(Enum):
    NONE = 0
    PRIMARY = 1
    FOREIGN = 2
    COMPOSITE_PRIMARY = 3
    COMPOSITE_PRIMARY_FOREIGN = 5

class Column:
    def __init__(self, name, dataType, notNull= False, keyType = KeyType.NONE, reference = None):
        if (not isinstance(name, str)) or (len(name) == 0):
            raise ValueError("Column name must be a non-empty str")
        self.name = name
        self.dataType = dataType
        self.notNull = notNull
        self.keyType = keyType
        self.reference = reference
        self.table = None

    def setReference(self, table, column):
        self.reference = (table, column)

    def __str__(self):
        return "Column '{0}': {1}".format(
            self.name,
            self.dataType + 
            str(" NOT NULL" if self.notNull else "") +
            str(" "+str(self.keyType) if self.keyType != KeyType.NONE else "") + 
            str(" REFERENCES {0}({1})".format(
                *self.reference if isinstance(self.reference, tuple) else \
                (self.reference.table.name, self.reference.name))\
                if self.reference is not None else "")
        )

class Table:
    def __init__(self, name, columns = dict(), isRelationalTable = False):
        self.columns = dict()
        self.name = name
        self.isRelationalTable = isRelationalTable
        self.database = None
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
        primaryKey = None
        if column.keyType == KeyType.PRIMARY:
            if self.primaryKey() is None:
                pass
            elif isinstance(self.primaryKey(), Column):
                self.primaryKey().keyType = KeyType.COMPOSITE_PRIMARY
                column.keyType = KeyType.COMPOSITE_PRIMARY
            elif isinstance(primaryKey, list):
                column.keyType = KeyType.COMPOSITE_PRIMARY
        del(primaryKey)
    
    def foreignKeys(self):
        """ 
        @return a list of tuples of pattern (col:Column, refTableName:str, refColumnName:str)
        """
        keys = list()
        for col in self.columns.values():
            if col.keyType in (KeyType.FOREIGN, KeyType.COMPOSITE_PRIMARY_FOREIGN):
                if isinstance(col.reference, tuple) and len(col.reference) == 2:
                    keys.append((col, *col.reference))
                elif isinstance(col.reference, Column):
                    keys.append((col, col.reference))
                else:
                    raise ValueError("Unknown reference type: Expected 2-tuple or Column, found {0}".format(col.reference.__class__))
        return keys

    def primaryKey(self):
        key = None
        for col in self.columns.values():
            if col.keyType == KeyType.PRIMARY:
                return col
            elif col.keyType in (KeyType.COMPOSITE_PRIMARY, KeyType.COMPOSITE_PRIMARY_FOREIGN):
                if key is None:
                    key = list()
                key.append(col)
        return key

    def foreignRefs(self, onlyRelationalRefs = False):
        refs = None
        if not isinstance(self.database, Database):
            return None
        if not onlyRelationalRefs:
            tables = self.database.tables.values # passing the function
        else:
            tables = self.database.relationalTables # passing the function
        for table in tables():
            if table.name is not self.name: # make sure we're not checking ourselves.
                for fk in table.foreignKeys():
                    if isinstance(fk, tuple):
                        if len(fk) == 3:
                            column = self.database.tables[fk[1]].columns[fk[2]]
                        elif len(fk) == 2:
                            column = fk[1]
                        else:
                            raise ValueError("Unexpected value for fk in Table.relationalRefs(): expected tuple, but found {0}".format(fk.__class__))
                    else:
                        raise ValueError("Unexpected value for fk in Table.relationalRefs(): expected tuple, but found {0}".format(fk.__class__))
                    if not isinstance(column, Column):
                        raise ValueError("Unexpected value for column in Table.relationalRefs(): expected Column, but found {0}".format(column.__class__))
                    if column.table.name == self.name:
                        if refs is None:
                            refs = list()
                        refs.append(column)
        return refs

    def __str__(self, indent="    "):
        output = indent + "Table '{0}': [\n".format(self.name + (" (Relational)" if self.isRelationalTable else ""))
        for column in self.columns.values():
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

    def linkReferences(self):
        for table in self.tables.values():
            for col, tableName, columnName in table.foreignKeys():
                col.reference = self.tables[tableName].columns[columnName]
        print("Linking Refs in {0}({1})".format(table.database.name, table.name))

    def __str__(self):
        output = "Database '{0}': [\n".format(self.name)
        for table in self.tables.values():
            output += table.__str__(indent = "    ") + "\n"
        return output + "]"
    
    def relationalTables(self):
        tables = list()
        for table in self.tables.values():
            if table.isRelationalTable:
                tables.append(table)

        return tables