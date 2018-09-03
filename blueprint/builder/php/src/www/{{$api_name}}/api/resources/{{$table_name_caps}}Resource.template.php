<?php
namespace {{$api_name}}\api\resources;
use {{$api_name}}\api\business\security\Secure{{$table_name_caps}};
use {{$api_name}}\api\data\models\{{$table_name_single_caps}};
use {{$api_name}}\api\resources\Response;
use \stdClass;


class {{$table_name_caps}}Resource extends Resource{

    private $security;

    public function __construct(){
        $this->security = new Secure{{$table_name_caps}}();
    }

    public function processRequest(array $request){
        switch($_SERVER['REQUEST_METHOD']){
            case "GET":
                if (count($request) == 0 || $request[0] == ""){
                    if(count($_GET) == 0){
                        return $this->getAll{{$table_name_caps}}(); // api/api.php/{{$table_name}} | api/api.php/{{$table_name}}/
                    }else{
                        return $this->genericQuery($_GET);
                    }
                }else{
                    return $this->get{{$table_name_single_caps}}ById($request[0]); // api/api.php/{{$table_name}}/{${{$table_name_single}}_id}
                }
                
                break;
            case "POST":
                return $this->add{{$table_name_single_caps}}(json_decode(file_get_contents('php://input')));
            case "PUT":
                if (count($request) == 0 || $request[0] == ""){
                    return $this->response_404();
                }
                return $this->update{{$table_name_single_caps}}($request[0], json_decode(file_get_contents('php://input')));
                break;
            case "DELETE":
                if (count($request) == 0 || $request[0] == ""){
                    return $this->response_404();
                }
                return $this->delete{{$table_name_single_caps}}($request[0]);
                break;
            default:
                return $this->response_400();
                break;
        }
    }

    public function genericQuery($constraints){
        $response = new Response();
        try{
            $response->setEntity($this->security->genericQuery($constraints));
        }catch (Exception $e){
            $response->setStatus(500);
            $response->setEntity($e->get_message());
        }
        return $response;
    }

    public function getAll{{$table_name_caps}}(){
        $response = new Response();
        try{
            $response->setEntity($this->security->getAll{{$table_name_caps}}());
        }catch (Exception $e){
            $response->setStatus(500);
            $response->setEntity($e->get_message());
        }
        return $response;
    }

    public function get{{$table_name_single_caps}}ById(string $id){
        $response = new Response();
        try{
            ${{$table_name_single}} = $this->security->get{{$table_name_single_caps}}ById($id);
            if(${{$table_name_single}} == null){
                $response = $this->response_404();
                return $response;
            }
            $response->setEntity(${{$table_name_single}});
        }catch (Exception $e){
            $response->setStatus(500);
            $response->setEntity($e->get_message());
        }
        return $response;
    }

    public function add{{$table_name_single_caps}}(stdClass ${{$table_name_single}}){
        $response = new Response();
        $new{{$table_name_single_caps}} = new {{$table_name_single_caps}}(${{$table_name_single}});
        try{
            $response->setEntity($this->security->add{{$table_name_single_caps}}($new{{$table_name_single_caps}}));
        }catch (Exception $e){
            $response->setStatus(500);
            $response->setEntity($e->get_message());
        }
        return $response;
    }

    public function update{{$table_name_single_caps}}(string $id, stdClass ${{$table_name_single}}){
        $updated{{$table_name_single_caps}} = new {{$table_name_single_caps}}(${{$table_name_single}});
        $response = new Response();
        try{
            $response->setEntity($this->security->update{{$table_name_single_caps}}($id, $updated{{$table_name_single_caps}}));
        }catch (Exception $e){
            $response->setStatus(500);
            $response->setEntity($e->get_message());
        }
        return $response;
    }

    public function delete{{$table_name_single_caps}}(string $id){
        
        try{
            $response = new Response(
                204,
                $this->security->delete{{$table_name_single_caps}}($id),
                array("Content-type"=>"text/html")
            );
        }catch (Exception $e){
            $response->setStatus(500);
            $response->setEntity($e->get_message());
        }
        return $response;
    }
}