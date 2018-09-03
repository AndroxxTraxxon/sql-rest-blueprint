<?php
namespace {{$api_name}}\api\data\models;
use DateTime;
class UUID{
    private $id_string;
    
    public function __construct(){
        $now = new DateTime();
        $tmpstr = $now->format('Y-m-d H:i:s.u')."new_uuid_object";
        $tmpstr = base64_encode(hash("sha3-256", $tmpstr, true));
        $this->id_string =str_replace("/", "~",
             substr($tmpstr, 0, 10).'-'
            .substr($tmpstr, 10, 9).'-'
            .substr($tmpstr, 19, 9).'-'
            .substr($tmpstr, 28, 9));
        $this->id_string = str_replace(
            "=-", "_", $this->id_string
        );
        unset($tmpstr);
    }

    public function toString(){
        return $this->id_string;
    }
}