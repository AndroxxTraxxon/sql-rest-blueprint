<?php
namespace {{$api_name}}\api\data\models;
use \JsonSerializable;
abstract class DataModel implements JsonSerializable{

    abstract protected function generateLinks();

    public function __construct($obj = null, $ignoreExtraValues = false){
        if($obj){
            foreach (((object)$obj) as $key => $value) {
                if(isset($value) && in_array($key, array_keys(get_object_vars($this))) && !isset($this->$key)){
                    $this->$key = $value;
                }else if (!$ignoreExtraValues){
                    throw new UnexpectedArgumentException(get_class($this).' does not have property '.$key);
                }
            }
        }
    }

    public function jsonSerialize(){
        $json = get_object_vars($this);
        if ($links = $this->generateLinks()){
            $json['links'] = $links;
        }
        return $json;
    }
}