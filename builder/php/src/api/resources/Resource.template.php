<?php
namespace {{$api_name}}\api\resources;
abstract class Resource{
    public abstract function processRequest(array $request);

    public function response_404(){
        $response = new Response(
            404, 
            'Error 404: Resource Not Found',
            ['content-type'=> 'text/html']
        );
        return $response;
        
    }
    public function response_400(){
        return new Response(
            400,
            'Error 400: Malformed Request',
            ['content-type'=> 'text/html']
        );
    }
}