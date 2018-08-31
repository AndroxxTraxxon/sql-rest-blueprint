<?php
function loadClass($class)
{
    $files = array(
        str_replace('\\', '/', $class) . '.php'
    );
    foreach (
        array_merge(
            array($_SERVER['DOCUMENT_ROOT']),
            explode(PATH_SEPARATOR, ini_get('include_path'))
            ) as $base_path)
    {
        foreach ($files as $file)
        {
            $path = "$base_path/$file";
            if (file_exists($path) && is_readable($path))
            {
                
                include_once $path;
                return;
            }
        }
    }
}
spl_autoload_register(loadClass);