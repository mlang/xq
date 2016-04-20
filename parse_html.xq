declare variable $url external;
let $html := xqilla:parse-html(fn:unparsed-text($url))
return $html

