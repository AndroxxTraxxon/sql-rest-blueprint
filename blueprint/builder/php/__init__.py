import re
import os

from blueprint.db.structure import KeyType

class PHPFileBuilder:

    @classmethod
    def buildAPIFile(cls, src, destFolder, options, dbModel):
        templateFileName = src.split(os.sep)[-1]
        destFileName = re.sub(
            'template.php',
            'php',
            cls.processReplacement(
                options,
                dbModel,
                templateFileName
            )
        )
        destFilePath = os.path.join(destFolder, destFileName)
        with open(src, "r") as template:
            with open(destFilePath, "w+") as output:
                for line in template.readlines():
                    newline = cls.processReplacement(options, dbModel, line)
                    output.write(newline)
                        


    @classmethod
    def buildTableFile(cls, src, destFolder, options, dbModel):
        for table in dbModel.tables.values():
            if not table.isRelationalTable:

                templateFileName = src.split(os.sep)[-1]
                destFileName = re.sub(
                    'template.php',
                    'php',
                    cls.processReplacement(
                        options, 
                        table, 
                        templateFileName
                    )
                )
                destFilePath = os.path.join(destFolder, destFileName)
                with open(src, "r") as template:
                    with open(destFilePath, "w+") as output:
                        for line in template.readlines():
                            newline = cls.processReplacement(options, table, line)
                            output.write(newline)
                        


    @classmethod
    def processReplacement(cls, options, subject, text):
        newText = text
        
        tag_sequence = re.compile(r"\{\{\$([a-zA-Z\_]+)\}\}")
        
        search = tag_sequence.search(newText)

        while search is not None:
            fullCapture = r'\{\{\$'+search.group(1)+r'\}\}'
            replacement = cls.getReplacementText(search.group(1), options, subject)
            newText = re.sub(
                fullCapture,
                replacement.replace("\\", r"\\"), 
                newText
            )
            search = tag_sequence.search(newText)
        return newText

    @classmethod
    def getReplacementText(cls, varKey, options, subject = None):
        tableReplaceVars = {
            "api_name": options['apiName'],
            "db_type": options['dbType'],
            "table_name": cls.getTableName,
            "table_name_caps": cls.getTableNameCaps,
            "table_name_single": cls.getTableNameSingle,
            "table_name_single_caps": cls.getTableNameSingleCaps,
            "table_columns_array": cls.getTableColumnsArray,
            "primary_key": cls.getPrimaryKey,
            "column_names_commas": cls.getTableColumnNamesCommas,
            "columns_question_marks": cls.getTableColumnsForUpdate,
            "non_primary_object_properties": cls.getTableObjectModelProperties,
            "column_name_properties": cls.getTableColumnNameProperties,
            "getter_setter_functions": cls.getTableGetterSetterFunctions,
            "non_primary_columns_commas_questions": cls.getTableNonPrimaryColumnsQuestion,
            "use_table_resources": cls.getUseTableResources,
            "table_resource_switch_case": cls.getTableResourceSwitchCase
        }
        if callable(tableReplaceVars[varKey]):
            return tableReplaceVars[varKey](subject, options)
        else:
            return tableReplaceVars[varKey]

    @classmethod
    def getTableResourceSwitchCase(cls, dbModel, options, indent = "    "):
        output = ""
        for table in dbModel.tables.values():
            if not table.isRelationalTable:
                output += "\n{0}case \"{1}\":\n".format(
                    indent, cls.getTableName(table, options)
                )
                output += "    {0}$resource = new {1}Resource();\n".format(
                    indent, cls.getTableNameCaps(table, options)
                )
                output += "    {0}break;".format(indent)
        return output

    @classmethod
    def getUseTableResources(cls, dbModel, options, indent = ""):
        output = ""
        for table in dbModel.tables.values():
            if not table.isRelationalTable:
                output += "use {0}\\api\\resources\\{1}Resource;\n".format(
                    options['apiName'],
                    cls.getTableNameCaps(table, options)
                )
        return output
            

    @classmethod
    def getTableNonPrimaryColumnsQuestion(cls, table, options = None, indent = "            "):
        output = ""
        for column in table.columns.values():
            if len(output) > 0:
                output += ", \n{0}".format(indent)
            if column.keyType != KeyType.PRIMARY:
                output += "{0} = ?".format(column.name)
        return output

    @classmethod
    def getTableGetterSetterFunctions(cls, table, options = None, indent=""):
        return "/* getter and setter functions go here. */"

    @classmethod
    def getTableColumnNameProperties(cls, table, options = None, indent = "    "):
        output = ""
        for column in table.columns.values():
            output += "private ${0};\n{1}".format(column.name, indent)
        return output

    @classmethod
    def getTableObjectModelProperties(cls, table, options = None, indent = "            "):
        output = ""
        for column in table.columns.values():
            if column.keyType != KeyType.PRIMARY:
                if len(output) > 0:
                    output += "\n{0}".format(indent)
                output += "${0},".format(column.name)
        return output

    @classmethod
    def getTableColumnsForUpdate(cls, table, options = None, indent = "        "):
        output = ""
        for column in table.columns.values():
            if column.keyType != KeyType.PRIMARY:
                if len(output) > 0:
                    output += ",\n"+indent
                output += column.name
        return output

    @classmethod
    def getTableColumnNamesCommas(cls, table, options = None, indent = "            "):
        output = ""
        for column in table.columns.values():
            if len(output) > 0:
                output += ",\n"+indent
            output += column.name
        return output

    @classmethod
    def getPrimaryKey(cls, table, options = None):
        for column in table.columns.values():
            if column.keyType == KeyType.PRIMARY:
                return column.name

    @classmethod
    def getTableColumnsArray(cls, table, options = None):
        return str(list(table.columns.keys()))

    @classmethod
    def getTableName(cls, table, options = None):
        return str(table.name).lower()
         

    @classmethod
    def getTableNameCaps(cls, table, options = None):
        return str(cls.getTableName(table)).capitalize()
    
    @classmethod
    def getTableNameSingle(cls, table, options = None):
        name = str(cls.getTableName(table))
        if name[-1] == 's':
            return name[0:-1]
        else:
            return name
    
    @classmethod
    def getTableNameSingleCaps(cls, table, options = None):
        return str(cls.getTableNameSingle(table)).capitalize()
         


    