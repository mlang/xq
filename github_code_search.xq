declare function local:source_lines($table as node()*) as xs:string*
{
  for $tr in $table/tr return normalize-space(data($tr))
};

let $results := html//div[@id="code_search_results"]/div[@class="code-list"]
for $div in $results/div
let $user := data($div/p/a[1])
let $file := data($div/p/a[2])
let $link := data($div/p/a[2]/@href)
return ($user, concat($file, ": ", $link), local:source_lines($div//table),
        "---------------------------------------------------------------")


