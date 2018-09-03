<?php
namespace {{$api_name}}\api\business;
use {{$api_name}}\api\data\models\{{$table_name_single_caps}};
interface Business{{$table_name_caps}} {
    public function genericQuery($constraints);
    public function getAll{{$table_name_caps}}();
    public function get{{$table_name_single_caps}}ById(string $id);
    public function add{{$table_name_single_caps}}({{$table_name_single_caps}} ${{$table_name_single}});
    public function update{{$table_name_single_caps}}(string $id, {{$table_name_single_caps}} ${{$table_name_single}});
    public function delete{{$table_name_single_caps}}(string $id);
}