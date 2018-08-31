<?php
namespace {{$api_name}}\api\data\models;
use {{$api_name}}\api\data\models\DataModel;
use \DateTime;
use \JsonSerializable; 
use \stdClass;
use \InvalidArgumentException;
class {{$table_name_single_caps}} extends DataModel{
    
    {{$column_name_properties}}

    public function __construct($obj = null, $ignoreExtraValues = false){
        parent::__construct($obj, $ignoreExtraValues);
        if(!$this->{{$primary_key}}){
            $this->{{$primary_key}} = ((new UUID())->toString());
        }
    }

    public function newId(){
        $this->{{$primary_key}} = (new UUID())->toString();
    }

    public function setId($id){
        $this->{{$primary_key}} = $id;
    }

    public function getId(){
        return $this->{{$primary_key}};
    }

    {{$getter_setter_functions}}

    protected function generateLinks(){
        $links = array((new HateoasLink('self', ['{{$table_name}}', $this->getId()]))->jsonSerialize());
        return $links;
    }
    
}