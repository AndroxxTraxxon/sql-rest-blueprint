<?php
namespace {{$api_name}}\api\data\models;
use {{$api_name}}\api\data\models\DataModel;
use \DateTime;
use \JsonSerializable; 
use \stdClass;
use \InvalidArgumentException;
class {{$table_name_single_caps}} implements JsonSerializable{
    
    {{$column_name_properties}}

    public function __construct($obj = null, $ignoreExtraValues = false){
        if($obj){
            foreach (((object)$obj) as $key => $value) {
                if(isset($value) && in_array($key, array_keys(get_object_vars($this))) && !isset($this->$key)){
                    $this->$key = $value;
                }else if (!$ignoreExtraValues){
                    throw new InvalidArgumentException(get_class($this).' does not have property '.$key);
                }
            }
        }
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

    public function jsonSerialize(){
        $json = get_object_vars($this);
        if ($links = $this->generateLinks()){
            $json['links'] = $links;
        }
        return $json;
    }
    
}