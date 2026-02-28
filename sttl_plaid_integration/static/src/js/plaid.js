

async function getLinktoken(){
  try {
    
    var record = getIdFromURL(location.href);
    // var record = this.model.loadParams.res_id

    if (record) {
      var handler = Plaid.create({
        token: (await $.post('/create_link_token')).link_token,  // calling our custom created endpoint to get link token which establishes connection with plaid using link token using onSuccess callback and return public_token.
        onLoad: function () {
        },
        onSuccess: async function (public_token, metadata) {
          await $.post('/exchange_public_token', {  // Calling our custom created endpoint to exhchange public token with access token(Access token is a token without expiration and is necessary for fetching data from plaid).
            public_token: public_token,
            current: record
          });
          location.reload();
        }
      });

      handler.open();
    }
    else {
      alert("Unable to fetch record. Please save the record and refresh the page.")
    }
  }
  catch (error) {
    alert(error.responseText);
  }

}

function getIdFromURL(url) {  // Fetches current record id from url
  var fragments = url.split('#');
  
  if (fragments.length < 2 || fragments[1].indexOf('=') === -1) {
      return null;
  }
  
  var params = fragments[1].split('&');
  
  for (var i = 0; i < params.length; i++) {
      var param = params[i].split('=');
      if (param[0] === 'id') {
          return param[1];
      }
  }
  
  return null;
}
