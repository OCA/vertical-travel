<html>
  <head>
    <style type="text/css">
      ${css}
    </style>
  </head>

  <body>
    %for o in objects:
      <h1>${_("Mission Manifest").upper()}</h1>
      <h2>XXXXXXXXXXXXXXXXXXXXXXXXXXX</h2>
      <h3>${who()}</h3>
      ${_("prescribed for")}
      ${passenger(o)}

      <table width="100%">
        <tr>
          <td width="175">
            ${_("to travel to")}
          </td>
          <td width="40%" class="field_input">
            %if o.destination and o.destination.name_get() and len(o.destination.name_get()[0]) > 1:
              ${o.destination.name_get()[0][1]}
            %endif
          </td>
          <td align="center" width="50">
            ${_("from")}
          </td>
          <td class="field_input">
            ${o.date_start}
          </td>
          <td align="center" width="50">
            ${_("to")}
          </td>
          <td class="field_input">
            ${o.date_stop}
          </td>
        </tr>
      </table>

      <table width="100%">
        <tr>
          <td width="175">
            ${_("means of transport")}
          </td>
          <td class="field_input">
            ${o.type or ''}
          </td>
        </tr>
      </table>

      <table width="100%">
        <tr>
          <td width="175">
            ${_("purpose of the mission")}
          </td>
          <td>
            <p>
              ${o.travel or ''}
            </p>
          </td>
        </tr>
      </table>
      <p>
        ${who()} <br/>
        ${_("thanks civilian and miliary authorities of the countries visited "
            "of the facilities they choose to equip bearer of this order for "
            "the smooth running of the mission.")}
      </p>
      <div class="sign_date">
        ${_("Made in %s, the") % (company.partner_id.city or '')}
      </div>
      <div class="sign_name">
        ${signer()}
      </div>
    %endfor
  </body>
</html>
