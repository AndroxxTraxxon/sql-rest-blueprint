<?php
namespace {{$api_name}}\api\business\rules;
use {{$api_name}}\api\data\db\{{$table_name_caps}}DAO;
use {{$api_name}}\api\business\Business{{$table_name_caps}};
use {{$api_name}}\api\data\models\{{$table_name_single_caps}};
use {{$api_name}}\api\business\rules\RulesException;
class Rules{{$table_name_caps}} implements Business{{$table_name_caps}}{
    private $db;

    public function __construct(){
        $this->db = new {{$table_name_caps}}DAO();
    }

    public function genericQuery($constraints){
        $entity = $this->db->genericQuery($constraints);
        return $entity;
    }

    public function getAll{{$table_name_caps}}(){
        $entity = $this->db->getAll{{$table_name_caps}}();
        return $entity;
    }
    public function get{{$table_name_single_caps}}ById(string $id){
        $entity = $this->db->get{{$table_name_single_caps}}ById($id);
        return $entity;
    }
    public function add{{$table_name_single_caps}}({{$table_name_single_caps}} ${{$table_name_single}}){
        $entity = $this->db->add{{$table_name_single_caps}}(${{$table_name_single}});
        return $entity;
    }
    public function update{{$table_name_single_caps}}(string $id, {{$table_name_single_caps}} ${{$table_name_single}}){
        $this->verifyUUID($id);
        $entity = $this->db->update{{$table_name_single_caps}}($id, ${{$table_name_single}});
        return $entity;
    }
    public function delete{{$table_name_single_caps}}(string $id){
        $entity = $this->db->delete{{$table_name_single_caps}}($id);
        return $entity;
    }

    private function verifyUUID(string $id){
        if(!preg_match(
            '/[A-Za-z0-9\~\_+]{10}\-[A-Za-z0-9\~\_\+]{9}\-[A-Za-z0-9\~\_\+]{9}\-[A-Za-z0-9\~\_\+]{9}/m',
            $id
        )){
            throw new RulesException("Invalid UUID");
        }
    }
}