<?php
namespace {{$api_name}}\api\business\security;
use bravo\api\business\Business{{$table_name_caps}};
use bravo\api\business\rules\Rules{{$table_name_caps}};
use bravo\api\data\models\{{$table_name_single_caps}};
class Secure{{$table_name_caps}} implements Business{{$table_name_caps}} {
    private $rules;
    private $users;
    private $user_token;

    public function __construct(){
        $this->rules = new Rules{{$table_name_caps}}();
        // $this->users = new UsersDAO(); 
        //you'll need to link this up to your users for authentication, if you want security.
    }

    public function genericQuery($constraints){
        $entity = $this->rules->genericQuery($constraints);
        return $entity;
    }

    public function getAll{{$table_name_caps}}(){
        $entity = $this->rules->getAll{{$table_name_caps}}();
        return $entity;
    }
    public function get{{$table_name_single_caps}}ById(string $id){
        $entity = $this->rules->get{{$table_name_single_caps}}ById($id);
        return $entity;
    }
    public function add{{$table_name_single_caps}}({{$table_name_single_caps}} ${{$table_name_single}}){
        $entity = $this->rules->add{{$table_name_single_caps}}(${{$table_name_single}});
        return $entity;
    }
    public function update{{$table_name_single_caps}}(string $id, {{$table_name_single_caps}} ${{$table_name_single}}){
        $entity = $this->rules->update{{$table_name_single_caps}}($id, ${{$table_name_single}});
        return $entity;
    }
    public function delete{{$table_name_single_caps}}(string $id){
        $entity = $this->rules->delete{{$table_name_single_caps}}($id);
        return $entity;
    }
}