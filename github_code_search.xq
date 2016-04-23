declare function local:source-lines($table as node()*) as xs:string*
{
  for $tr in $table/tr return normalize-space(data($tr))
};

let $results := html//div[@id="code_search_results"]/div[@class="code-list"]
for $div at $i in $results/div
let $repo := data($div/p/a[1])
let $file := data($div/p/a[2])
let $link := resolve-uri(data($div/p/a[2]/@href))
return (concat($i, ". ", $repo, "//", $file),
        $link,
        local:source-lines($div//table),
        "---------------------------------------------------------------------")

