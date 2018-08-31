import re
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from structure.Database import Database
from structure.Table import Table
from structure.Column import Column
from structure import KeyType

import pprint

class MySQLParser:
    db_name_regex = re.compile('USE ([a-zA-Z\_]+);')
    table_regex = re.compile('CREATE TABLE(?: IF NOT EXISTS)* (?P<tableName>[A-Za-z\_]+)[\s]*\((?P<columns>[\s\w\(\),]+)\)\;')
    column_regex = re.compile('(?P<column_name>[a-zA-Z\_]+)\s+(?P<type>[a-zA-Z0-9\(\)]+)(?P<nullity>[NOT NUL]*),\s')
    primary_regex = re.compile('PRIMARY KEY\(([a-zA-Z\,\_\s]*)\)')
    foreign_regex = re.compile('FOREIGN KEY\(([a-zA-Z\_]*)\) ')

    @classmethod
    def buildFromFile(cls, sqlfilepath):
        db = None
        with open(sqlfilepath) as sqlfile:
            text = sqlfile.read()
            db_name = cls.db_name_regex.findall(text)[0]
            tables = cls.table_regex.findall(text)
            table_names = list()
            db = Database(db_name)
            for table in tables:
                name, content = table
                tbl = Table(name)
                table_names.append(name)
                columns = cls.column_regex.findall(content)
                for column in columns:
                    notNull = False
                    if str(column[2]).find("NOT NULL") >=0:
                        notNull = True
                    col = Column(column[0], column[1], notNull = notNull)
                    tbl.addColumn(col)
                pks = cls.primary_regex.findall(content)
                if len(pks) > 0:
                    pks = [key.strip() for key in pks[0].split(',')]
                if len(pks) == 1:
                    keyType = KeyType.PRIMARY
                elif len(pks) > 1:
                    keyType = KeyType.COMPOSITE_PRIMARY
                for columnName, column in tbl.columns.items():
                    if columnName in pks:
                        column.keyType = keyType
                db.addTable(tbl)
        return db
