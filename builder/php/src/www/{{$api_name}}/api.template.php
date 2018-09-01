<?php
include_once('../autoloader.php');
{{$use_table_resources}}
$request = explode("/", substr($_SERVER['PATH_INFO'], 1));
$resource = null;
switch($request[0]){
    // case "test":
    //     $resource = (object)["key"=>"value"];
    //     break;
    {{$table_resource_switch_case}}
    default:
        $resource = new ErrorResource();
        break;
}
/**
 * If the provided resource is not an instance of 
 * bravo\api\resources\Resource, then throw an error.
 * Resource provides necessary functionality and constraints.
 */
if(!in_array("{{$api_name}}\\api\\resources\\Resource", class_parents($resource))){
    throw new UnexpectedValueException("$resource must implement {{$api_name}}\\api\\resources\\Resource\n");
}
array_shift($request);
$resource->processRequest($request)->send();


