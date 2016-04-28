declare function local:fix-umlauts($input as xs:string*) as xs:string*
{
  replace(replace(replace(replace($input, "Ã¼", "ü"), "Ã¶", "ö"), "Ã¤", "ä"),
          "Ã", "ß")
};

let $history := //div[@class="sendungsstatus-history"]
for $li in $history//li
let $div := $li//div[@class="media-body"]
let $when := normalize-space($div/em/b)
let $what := local:fix-umlauts(normalize-space($div/b))
let $tooltip := local:fix-umlauts(normalize-space($div/a/@title))
return ($when, $what, $tooltip)
