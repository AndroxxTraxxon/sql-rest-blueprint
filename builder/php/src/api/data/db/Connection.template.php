<?php
namespace {{$api_name}}\api\data\db;
use \PDO;
class Connection{

  private static $servername = "db";
  private static $username = "root";
  private static $password = "test";
  private static $dbname = "{{$api_name}}";
  private static $dbtype = "{{$db_type}}";

  public static function getConnection(){
    $conn = new PDO(
      self::$dbtype.':host='.self::$servername.';'.
      'dbname='.self::$dbname,
      self::$username,
      self::$password
    );
    return $conn;
  }

}