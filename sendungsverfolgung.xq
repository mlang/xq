declare variable $verbosity external;

declare function local:fix-umlauts($input as xs:string*) as xs:string*
{
  replace(replace(replace(replace($input, "Ã¼", "ü"), "Ã¶", "ö"), "Ã¤", "ä"),
          "Ã", "ß")
};

let $div-table := //div[@class="cut"]/div[@style="display:table;"]
return if ($div-table) then
       (concat(normalize-space(data($div-table/div[1])), " ",
               normalize-space(data($div-table/div[2]))),
        "Sendungsverlauf:",
        for $item in //div[@class="sendungsstatus-history"]//li//div[@class="media-body"]
        let $when := normalize-space($item/em/b)
        let $what := local:fix-umlauts(normalize-space($item/b))
        let $tooltip := local:fix-umlauts(normalize-space($item/a/@title))
        return (concat($when, ": ", $what),
                if ($verbosity = "please") then concat("* ", $tooltip) else ()))
       else "Es konnten keine Daten zu ihrer Anfrage gefunden werden."
