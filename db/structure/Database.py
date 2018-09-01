from structure.Table import Table


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
        for table in self.tables:
            output += "    " + str(table) + "\n"
        return output + "]"