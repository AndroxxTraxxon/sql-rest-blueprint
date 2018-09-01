<?php
namespace {{$api_name}}\api\data\models;
use \JsonSerializable;


class HateoasLink implements JsonSerializable{

    private $rel;
    private $href;

    public function __construct(string $rel, array $path){
        $this->rel = $rel;
        $site_root = (!empty($_SERVER['HTTPS']) ? 'https' : 'http') . '://' . $_SERVER['HTTP_HOST'] . '/';
        $apiPath = 'bravo/api.php/';
        $this->href = $site_root.$apiPath.implode("/", $path);
    }

    public function jsonSerialize(){
        return get_object_vars($this);
    }
}