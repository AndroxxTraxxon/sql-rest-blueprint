import re
import os

from blueprint.db.structure import KeyType, Column

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
                print(
                    '             --->', 
                    os.path.join(
                        destFolder, 
                        destFileName
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
            "columns_question_marks": cls.getPreparedQuestionMarks,
            "non_primary_object_properties": cls.getTableObjectModelProperties,
            "column_name_properties": cls.getTableColumnNameProperties,
            "getter_setter_functions": cls.getTableGetterSetterFunctions,
            "non_primary_columns_commas_questions": cls.getTableNonPrimaryColumnsQuestion,
            "use_table_resources": cls.getUseTableResources,
            "table_resource_switch_case": cls.getTableResourceSwitchCase,
            "all_table_values": cls.getAllTableValues,
            "fetch_relational_object_functions": cls.getReferenceIDArrayDAOFunctions
        }
        if callable(tableReplaceVars[varKey]):
            return tableReplaceVars[varKey](subject, options)
        else:
            return tableReplaceVars[varKey]

    @classmethod
    def getReferenceIDArrayDAOFunctions(cls, table, options, indent = "    "):
        output = ""
        header = """
/****************************************************************************
                {table_name_single_caps} {foreign_table_name_caps}
 ****************************************************************************/"""
        getFnStr = """
    public function get{foreign_rltn_name}(string $id){{
        $sql = "SELECT {foreign_id_col_name} FROM {rltn_table_name} WHERE {local_id_col_name} = ?";
        $values = array($id);
        $conn = $this->getConnection();
        if($stmt = $conn->prepare($sql)){{
            if(!$stmt->execute($values)){{
                throw new Exception(json_encode($stmt->errorInfo));
            }}
            $entity = $stmt->fetchAll(PDO::FETCH_COLUMN);
        }}else{{
            throw new Exception(json_encode($stmt->errorInfo));
        }}
        return $entity;
    }}"""
        addFnStr = """
    public function add{foreign_rltn_name}(string ${local_id_col_name}, string ${foreign_id_col_name}){{
        $sql = "INSERT INTO {rltn_table_name} ({local_id_col_name}, {foreign_id_col_name}) VALUES (?,?)";
        $conn = $this->getConnection();
        if($stmt = $conn->prepare($sql)){{
            if(!$stmt->execute($values)){{
                throw new Exception(json_encode($stmt->errorInfo));
            }}
        }}else{{
            throw new Exception(json_encode($stmt->errorInfo));
        }}
    }}"""
        delFnStr = """
    public function remove{foreign_rltn_name}(string ${local_id_col_name}, string ${foreign_id_col_name}){{
        $sql = "DELETE FROM {rltn_table_name} WHERE {local_id_col_name} = ? and {foreign_id_col_name} = ?";
        $values = array(${local_id_col_name}, ${foreign_id_col_name});
        $conn = $this->getConnection();
        if($stmt = $conn->prepare($sql)){{
            if(!$stmt->execute($values)){{
                throw new Exception(json_encode($stmt->errorInfo));
            }}
        }}else{{
            throw new Exception(json_encode($stmt->errorInfo));
        }}
    }}"""

        for siblingTable in table.database.tables.values():
            if siblingTable is not table: # don't need to check against ourselves.               
                if siblingTable.isRelationalTable: # When it's just a table of foreign keys related to each other
                    refColumns = cls.getRelationalReferences(table, siblingTable) # returns an array of foreign columns
                    if len(refColumns) == 0: # if there aren't any other references, this is just 
                        # print("{} -> {}: reference columns empty".format(siblingTable.name, table.name))
                        continue
                    
                    for column in refColumns: # this is the column in the other table!
                        _header = header.format(
                            table_name_single_caps = cls.getTableNameSingleCaps(table, options),
                            foreign_table_name_caps = cls.getTableNameCaps(column.reference.table, options)
                        )
                        _getFnStr = getFnStr.format(
                            rltn_table_name = siblingTable.name,
                            foreign_rltn_name = cls.getTableNameCaps(column.reference.table, options),
                            local_id_col_name = table.primaryKey().name,
                            foreign_id_col_name= column.name
                        )
                        _addFnStr = addFnStr.format(
                            rltn_table_name = siblingTable.name,
                            foreign_rltn_name = cls.getTableNameSingleCaps(column.reference.table, options),
                            local_id_col_name = table.primaryKey().name,
                            foreign_id_col_name= column.name
                        )
                        _delFnStr = delFnStr.format(
                            rltn_table_name = siblingTable.name,
                            foreign_rltn_name = cls.getTableNameSingleCaps(column.reference.table, options),
                            local_id_col_name = table.primaryKey().name,
                            foreign_id_col_name= column.name
                        )
                        output += "{_div}{_get}\n{_add}\n{_del}".format(
                            _div = _header,
                            _get = _getFnStr,
                            _add = _addFnStr,
                            _del = _delFnStr
                        )
                else:
                    continue # if it's a direct reference, then this isn't the place.
        return output

    @classmethod
    def getRelationalReferences(cls, table, siblingTable):
        refColumns = []
        selfRefColumn = None
        for column in siblingTable.columns.values(): # find a reference column to myself
            if (isinstance(column, Column) and
                column.keyType in (KeyType.COMPOSITE_PRIMARY_FOREIGN, KeyType.FOREIGN)):
                if isinstance(column.reference, Column):
                    pass
                else:
                    raise ValueError("Foreign Key Referencing unknown value: {0}".format(
                        str(column.reference)
                    ))
                if (column.reference is table.primaryKey() or 
                        (isinstance(table.primaryKey(), (list, tuple)) and 
                        column.reference in table.primaryKey())):
                        # print("Validated Reference: {table}.{col} -> {f_table}.{f_col}".format(
                        #     table = column.table.name,
                        #     col=column.name,
                        #     f_table=column.reference.table.name,
                        #     f_col=column.reference.name
                        # ))
                        selfRefColumn = column
                        break
                # else:
                #     pk = None
                #     if isinstance(table.primaryKey(), list):
                #         pk=[x.name for x in table.primaryKey()] 
                #     else :
                #         pk=table.primaryKey().name
                #     raise ValueError("Foreign Key {0}.{1} referencing non-Primary Key {2}.{3}\n (PK: {4})".format(
                #         column.table.name, column.name, 
                #         column.reference.table.name, column.reference.name, 
                #         pk
                #     ))
        # print("Self ref", str(selfRefColumn))
        if selfRefColumn is None: # if this sibling table doesn't reference the current table, I'm done
            return refColumns
        for column in siblingTable.columns.values(): # find the foreign reference.
            if (isinstance(column, Column) and # this this is actually a Column object.
                column.keyType in (KeyType.COMPOSITE_PRIMARY_FOREIGN, KeyType.FOREIGN) and  # it's a foreign key
                column is not selfRefColumn): # it's not the column referencing myself
                # print(siblingTable.name,".",column.name, "->", column.reference.table.name)
                refColumns.append(column)
        return refColumns

    @classmethod
    def getAllTableValues(cls, table, options, indent = "            "):
        output = ""
        for column in table.columns.values():
            if len(output) > 0:
                output += ", \n"+indent
            if column.keyType is KeyType.PRIMARY:
                output += "${0}->getId()".format(cls.getTableNameSingle(table, options))
            else:
                output += "${0}->{1}".format(
                    cls.getTableNameSingle(table, options),
                    cls.makeGetterFunctionSignature(column.name)
                )
        return output

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
        output += "use {0}\\api\\resources\\{1}Resource;\n".format(
                    options['apiName'],
                    'Error'
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
    def getFunctionName(cls, prefix, varName):
        words = varName.split('_')
        for i in range(len(words)):
            words[i] = words[i].capitalize()
        words.insert(0, prefix)
        return "".join(words)

    @classmethod
    def makeGetterFunctionSignature(cls, varName):
        return cls.getFunctionName("get", varName) + "()"

    @classmethod
    def makeSetterFunctionSignature(cls, varName):
        return cls.getFunctionName("set", varName) + "(${0})".format(varName)

    @classmethod
    def getTableGetterSetterFunctions(cls, table, options = None, indent="    "):
        output = "\n"
        for column in table.columns.values():
            if column.keyType is not KeyType.PRIMARY:
                output += "{0}public function {1}\n".format(indent, cls.makeGetterFunctionSignature(column.name) + "{")
                output += "{0}    return $this->{1};\n".format(indent, column.name)
                output += "{0}\n\n".format(indent + "}")

                output += "{0}public function {1}\n".format(indent, cls.makeSetterFunctionSignature(column.name) + "{")
                output += "{0}    $this->{1} = ${1};\n".format(indent, column.name)
                output += "{0}\n\n".format(indent + "}")
        
        return output[0:-1]

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
                output += "${0}->{1},\n{2}".format(
                    cls.getTableNameSingle(table, options),
                    cls.makeGetterFunctionSignature(column.name),
                    indent
                )
        return output

    @classmethod
    def getPreparedQuestionMarks(cls, table, options = None, indent = "        "):
        output = ""
        for column in table.columns.values():
            if len(output) > 0:
                output += ", "
            output += "?"
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
        return table.primaryKey().name

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
         


    