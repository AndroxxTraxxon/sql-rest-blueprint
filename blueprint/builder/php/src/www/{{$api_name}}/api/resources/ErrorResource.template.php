<?php
namespace {{$api_name}}\api\resources;
use {{$api_name}}\api\resources\Response;
use \stdClass;


class ErrorResource extends Resource{

  public function processRequest(array $request){
    switch($_SERVER['REQUEST_METHOD']){
      case "GET":
        if (count($request) == 0 || $request[0] == ""){
          if(count($_GET) == 0){
            return $this->response_404();
          }else{
            return $this->response_404();
          }
        }else{
          return $this->response_404();
        }
        
        break;
      case "POST":
        return $this->response_404();
      case "PUT":
        if (count($request) == 0 || $request[0] == ""){
          return $this->response_404();
        }
        return $this->response_404();
        break;
      case "DELETE":
        if (count($request) == 0 || $request[0] == ""){
          return $this->response_404();
        }
        return $this->response_404();
        break;
      default:
        return $this->response_400();
        break;
    }
  }
}