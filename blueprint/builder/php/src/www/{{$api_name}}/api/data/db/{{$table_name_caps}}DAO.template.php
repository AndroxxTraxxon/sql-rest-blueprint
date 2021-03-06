<?php
namespace {{$api_name}}\api\data\db;
use {{$api_name}}\api\data\models\{{$table_name_single_caps}};
use \PDO;
use \Exception;
class {{$table_name_caps}}DAO{

    private function getConnection(){
        return Connection::getConnection();
    }

    public function genericQuery(array $constraints){
        if(sizeof($constraints) == 0){
            throw new IllegalArgumentException("Query must specify constraints.");
        }
        $sql = "SELECT A.* FROM {{$table_name}} A WHERE ";
        $conditions = [];
        $params = [];
        $pattern = "";
        foreach ($constraints as $key => $value) {
            if(in_array($key, {{$table_columns_array}})){
                if($value){
                    $conditions[] = $key." = ?";
                    $params[] = $value;
                }
            }else{
                throw new IllegalArgumentException("Illegal path parameter name.");
            }
            
        }
        $sql .= implode(" AND ", $conditions);
        $conn = $this->getConnection();
        if($stmt = $conn->prepare($sql)){
            if(!$stmt->execute($params)){
                throw new Exception($stmt->errorInfo());
            }
            $result = $stmt->fetchAll(PDO::FETCH_CLASS, "{{$api_name}}\\api\\data\\models\\{{$table_name_single_caps}}");
            return $result;
        }else{
            return [
                'conn'=> $conn, 
                'errors'=>$conn->error_list, 
                'query'=> $sql
            ];
        }        
    }
    
    public function getAll{{$table_name_caps}}(){
        try{
            $conn = $this->getConnection();
            $sql = "SELECT * FROM {{$table_name}}";
            $stmt = $conn->prepare($sql);
            if(!$stmt->execute()){
                throw new Exception($stmt->errorInfo());
            }
            $entity = $stmt->fetchAll(PDO::FETCH_CLASS, "{{$api_name}}\\api\\data\\models\\{{$table_name_single_caps}}");
            
        }catch(Exception $e){
            // var_dump(get_class($e)."::".$e->getMessage());
        }
        return $entity;
    }

    public function get{{$table_name_single_caps}}ById(string $id){
        try{
            $conn = $this->getConnection();
            $sql = "SELECT * FROM {{$table_name}} WHERE {{$primary_key}} = ?";
            $stmt = $conn->prepare($sql);
            if(!$stmt->execute(array($id))){
                throw new Exception($stmt->errorInfo());
            }
            $entity = $stmt->fetchAll(PDO::FETCH_CLASS, "{{$api_name}}\\api\\data\\models\\{{$table_name_single_caps}}");

        }catch(Exception $e){
            // var_dump(get_class($e)."::".$e->getMessage());
        }
        if(sizeof($entity) == 0){
            return null;
        }
        return $entity[0];
    }

    public function add{{$table_name_single_caps}}({{$table_name_single_caps}} ${{$table_name_single}}){
        $insert_success = false;
        $conn = $this->getConnection();
        $first_try = true;
        $sql = "INSERT INTO {{$table_name}} (
            {{$column_names_commas}}
        ) 
        VALUES ({{$columns_question_marks}})";
        $values = [
            {{$all_table_values}}
        ];
        while(!$insert_success){
            if(!$first_try){
                ${{$table_name_single}}->newId();
            }
            if($stmt = $conn->prepare($sql)){
                if(!$stmt->execute($values)){
                    throw new Exception($stmt->errorInfo());
                }
                $insert_success = true; 
            }else{
                return [
                    'conn'=> $conn, 
                    'errors'=>$conn->error_list, 
                    'query'=> $sql,
                    'message'=> 'Malformed Request'];
            }
            $first_try = false; 
                      
        }
        return ${{$table_name_single}};
    }

    public function update{{$table_name_single_caps}}(string $id, {{$table_name_single_caps}} ${{$table_name_single}}){
        
        $sql = "UPDATE {{$table_name}} SET
            {{$non_primary_columns_commas_questions}}
        WHERE {{$primary_key}} = ?";
        
        $values = [
            {{$non_primary_object_properties}}$id.""
        ];
        $conn = $this->getConnection();
        if($stmt = $conn->prepare($sql)){
            if(!$stmt->execute($values)){
                throw new Exception($stmt->errorInfo());
            }

        }else{
            return [
                'conn'=> $conn, 
                'errors'=>$conn->error_list, 
                'query'=> $sql,
                'message'=> 'Malformed Request'];
        }  
        ${{$table_name_single}}->setId($id);             
        return ${{$table_name_single}};
    }
{{$fetch_relational_object_functions}}

    public function delete{{$table_name_single_caps}}(string $id){
        try{
            $conn = $this->getConnection();
            $sql = "DELETE FROM {{$table_name}} WHERE {{$primary_key}} = ?";
            $stmt = $conn->prepare($sql);
            if(!$stmt->execute(array($id))){
                throw new Exception($stmt->errorInfo());
            }
        }catch(Exception $e){
            // var_dump(get_class($e)."::".$e->getMessage());
        }
        return "BAND DELETED";
    }
}