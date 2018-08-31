from structure.Table import Table


class Database:

    def __init__(self, name, tables = list()):
        self.tables = tables
        self.name = name
        if(self.name == ''):
            raise ValueError("Table name cannot be null")
        tableNames = list()
        for table in self.tables:
            if table.name in tableNames:
                raise ValueError("Column names must be unique")

    def addTable(self, table):
        for oldtable in self.tables:
            if table.name == oldtable.name:
                raise ValueError("Column names must be unique")
        self.tables.append(table)

    def __str__(self):
        output = "Database '{0}': [\n".format(self.name)
        for table in self.tables:
            output += "    " + str(table) + "\n"
        return output + "]"