$(function() {

  //This will make a ajax post request to the member detail controller which return html and we render that in ajax response.
  let languages = {
    "availableLanguages": [{
      "type": "published",
      "url": "http:\/\/bni-ahmedabad.in\/en-IN\/memberdetails",
      "descriptionKey": "English (IN)",
      "id": 47,
      "localeCode": "en_IN"
    }],
    "activeLanguage": {
      "id": 47,
      "localeCode": "en_IN",
      "descriptionKey": "English (IN)"
    }
  };
  let parameters = window.location.href.slice(window.location.href.indexOf('?') + 1);
  let mappedWidgetSettings = '[{"key":124,"name":"Direct","value":"Direct"},{"key":125,"name":"Mobile","value":"Mobile"},{"key":126,"name":"Freephone","value":"Freephone"},{"key":127,"name":"Fax","value":"Fax"},{"key":128,"name":"Website","value":"Website"},{"key":129,"name":"Company Name","value":"Company Name"},{"key":130,"name":"Address","value":"Address"},{"key":131,"name":"Send Message","value":"Send Message"},{"key":217,"name":"Phone","value":"Phone"}]';
  let pageMode = "Live_Site";
  let memberId = getParameterByName("memberId");

  for (let i = 5000; i < 11000; i++) {



    $.get('https://bni-india-list.firebaseio.com/bni/' + i + '.json', function(data) {
      console.log(data);
      let parameters = data.split("?")[1];
      $.post("/bnicms/v3/frontend/memberdetail/display", {
        parameters: parameters,
        languages: languages,
        pageMode: pageMode,
        mappedWidgetSettings: mappedWidgetSettings,
        memberId: memberId
      }, function(data) {
        let html = $.parseHTML(data);
        let memberDetails = {
          name: $(html).find('h2').html(),
          title: $(html).find('h2').next().html(),
          chapter: $(html).find('.photoCol a').html(),
          contact: $(html).find('.contactCol').html(),
          website: $(html).find('.contactCol a').html(),
          company: $(html).find('.companyCol').html(),
          business: $(html).find('.rowBusiness').html(),

        }

        $.ajax({
          url: 'https://bni-india-list.firebaseio.com/data/' + i + '.json',
          type: 'PUT',
          data: JSON.stringify(memberDetails),
          success: function(result) {
            console.log(result);
          },
        });

      })

    });

    setTimeout(function() {
      console.log("this is delay!", new Date())
    }, 5000);
  }
});
