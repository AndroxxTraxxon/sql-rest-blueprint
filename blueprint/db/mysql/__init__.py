import re
import os,sys,inspect

from blueprint.db import AbstractSQLFileParser
from blueprint.db.structure import Database, Table, Column, KeyType

import pprint

class MySQLFileParser(AbstractSQLFileParser):

    def __init__(self, sqlfilepath = os.path.join(os.getcwd(), "init.sql")):
        self.db_name_regex = re.compile(r'USE ([a-zA-Z\_]+);')
        self.table_regex = re.compile(r'CREATE TABLE(?: IF NOT EXISTS)* (?P<tableName>[A-Za-z\_]+)[\s]*\((?P<columns>[\s\w\(\),]+)\)\;')
        self.column_regex = re.compile(r'(?P<column_name>[a-zA-Z\_]+)\s+(?P<type>[a-zA-Z0-9\(\)]+)(?P<nullity>[NOT NUL]*),\s')
        self.primary_regex = re.compile(r'PRIMARY KEY\(([a-zA-Z\,\_\s]+)\)')
        self.foreign_regex = re.compile(r'FOREIGN KEY\(([a-zA-Z\_]+)\) REFERENCES ([a-zA-Z\_]+)\(([a-zA-Z\_]+)\)')
        self.sqlfilepath = sqlfilepath

    def getDB(self):
        db = None
        with open(self.sqlfilepath) as sqlfile:
            text = sqlfile.read()
            db_name = self.db_name_regex.findall(text)[0]
            tables = self.table_regex.findall(text)
            db = self.buildDB(db_name, tables)
        return db

    def buildDB(self, name, tableTextList):
        db = Database(name, dbType='mysql')
        for table in tableTextList:
            db.addTable(self.buildTable(*table))
        for table in db.tables.values():
            table.database = db
            print("Table {0} put in database {1}".format(
                table.name,
                db.name
            ))
        db.linkReferences()
        return db

    def buildTable(self, name, content):
        table = Table(name)
        columns = self.column_regex.findall(content)
        for column in columns:
            table.addColumn(self.buildColumn(*column))
        for column in table.columns.values():
            column.table = table
        pks = self.primary_regex.findall(content)
        if len(pks) > 0:
            pks = [key.strip() for key in pks[0].split(',')]
        if len(pks) == 1:
            keyType = KeyType.PRIMARY
        elif len(pks) > 1:
            keyType = KeyType.COMPOSITE_PRIMARY
        for columnName, column in table.columns.items():
            if columnName in pks:
                column.keyType = keyType
        fks = self.foreign_regex.findall(content)
        for col, refTable, refCol in fks:
            table.columns[col].reference = (refTable, refCol)
            if table.columns[col].keyType == KeyType.COMPOSITE_PRIMARY:
                table.columns[col].keyType = KeyType.COMPOSITE_PRIMARY_FOREIGN
            else:
                table.columns[col].keyType = KeyType.FOREIGN
        return table

    def buildColumn(self, name, dataType, nullity, keytype = KeyType.NONE):
        notNull = False
        if (isinstance(nullity, str) and nullity.find("NOT NULL") >=0):
            notNull = True
        col = Column(
            name, 
            dataType, 
            notNull=notNull, 
            keyType=keytype
        )
        return col

    
