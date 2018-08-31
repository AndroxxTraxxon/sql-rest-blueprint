<?php
namespace {{$api_name}}\api\resources;
use \JsonSerializable;
class Response implements JsonSerializable{
    private $status;
    private $entity;
    private $header;
    private static $has_sent = false;

    public function __construct(int $status = 200, 
                                $entity = null,
                                array $header = array("Content-type"=>"application/json")){
        $this->status = $status;
        $this->entity = $entity;
        $this->header = $header;
    }

    public function send(){
        if(!$this->has_sent){
            http_response_code($this->status);
            if(!headers_sent()){
                foreach ($this->header as $key => $value) {
                    header("$key: $value");
                }
            }
            if(!is_string($this->entity)){
                print(json_encode($this->entity));
            }else{
                print($this->entity);
            }
            
            $this->has_sent = true;
        }else{
            throw new Exception("Response has already been sent!", 1);
            
        }
    }

    public function setStatus(int $status){
        $this->status = $status;
    }

    public function getStatus(){
        return $this->status;
    }

    public function setEntity($entity){
        $this->entity = $entity;
    }

    public function getEntity(){
        return $this->entity;
    }

    public function jsonSerialize(){
        $json = array(
            'status' => $this->status,
            'entity' => $this->entity,
            'header' => $this->header
        );
    }
}