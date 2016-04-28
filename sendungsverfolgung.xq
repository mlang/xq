declare function local:fix-umlauts($input as xs:string*) as xs:string*
{
  replace(replace($input, "Ã¼", "ü"), "Ã¶", "ö")
};

let $history := //div[@class="sendungsstatus-history"]
for $li in $history//li
let $div := $li//div[@class="media-body"]
let $a := normalize-space($div/em/b)
let $b := local:fix-umlauts(normalize-space($div/b))
let $c := local:fix-umlauts(normalize-space($div/a/@title))
return ($a, $b, $c)
