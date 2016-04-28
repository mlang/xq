declare function local:fix-umlauts($input as xs:string*) as xs:string*
{
  replace(replace(replace(replace($input, "Ã¼", "ü"), "Ã¶", "ö"), "Ã¤", "ä"),
          "Ã", "ß")
};

let $div-table := //div[@class="cut"]/div[@style="display:table;"]
return (concat(normalize-space(data($div-table/div[1])), " ",
               normalize-space(data($div-table/div[2]))),
        "Verlauf:",
        let $history := //div[@class="sendungsstatus-history"]
        for $li in $history//li
        let $div := $li//div[@class="media-body"]
        let $when := normalize-space($div/em/b)
        let $what := local:fix-umlauts(normalize-space($div/b))
        let $tooltip := local:fix-umlauts(normalize-space($div/a/@title))
        return (concat($when, ": ", $what), concat("* ", $tooltip)))
