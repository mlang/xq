let $result := //table[@class="list"]/tbody/tr
return
  if ($result) then
    for $tr in $result
      let $person := normalize-space(data($tr/td/a/person))
      let $email := data($tr/td/a/mail/img/@alt)
      let $phone := normalize-space(data($tr/td/phone/nobr/nobr/div/a/span))
      let $org := normalize-space(data($tr/td/span/a))
      return ($person, $org, $email, $phone, "--------------------------------")
  else 'No match.'

