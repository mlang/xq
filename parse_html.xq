declare variable $url external;
let $html := xqilla:parse-html(unparsed-text($url)) return $html
