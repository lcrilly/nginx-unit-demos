<?php

$body = file_get_contents('php://input');
$json = json_decode($body);
$json = $json->operands;

$r["result"] = 0;
foreach ($json as &$operand)
    $r["result"] += $operand;

header("Content-Type: application/json; charset=utf-8");
echo json_encode($r, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES);

?>
