<?php
namespace {{$api_name}}\api\data\db;
use \PDO;
class Connection{

  private static $servername = "db";
  private static $username = "root";
  private static $password = "test";
  private static $dbname = "bravo";

  public static function getConnection(){
    $conn = new PDO(
      'mysql:host='.self::$servername.';'.
      'dbname='.self::$dbname,
      self::$username,
      self::$password
    );
    return $conn;
  }

}