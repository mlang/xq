declare variable $query external;
for $tr in //a[contains(data(.), $query)]/ancestor::tr
let $item := normalize-space(data($tr/td[2]/b/a))
let $currency := normalize-space(data($tr/td[3]))
let $sell := normalize-space(data($tr/td[4]))
let $buy := normalize-space(data($tr/td[5]))
let $avg := normalize-space(data($tr/td[6]))
let $date := normalize-space(data($tr/td[7]))
return concat("On ", $date, ", ", $item, " was bought for ", $sell, " ", $currency, ".")
