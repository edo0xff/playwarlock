var apiURL = 'http://' + window.location.hostname + ':8080/api/v0.1';
var resultsContainer = $("#resultsContainer");
var searchButton = $("#searchButton");
var searchInput = $("#searchInput");
var loadingGIF = $("#loadingGIF");

var endpoint = function(ep) {
   return apiURL + ep;
}

var encodeURI = function(data) {
   urlEncodedDataPairs = [];

   for( name in data ) {
      urlEncodedDataPairs.push(name + '=' + data[name]);
   }

   return '?' + urlEncodedDataPairs.join( '&' ).replace( ' ', '+' );
}

searchButton.on("click", function(event) {
   var searchQuery = searchInput.val();

   if(searchQuery != "") {
      loadingGIF.css('display', 'block');

      $.ajax({
         url: endpoint('/search'),
         data: {
            q: searchQuery
         },
         success: function(response) {
            loadingGIF.css('display', 'none');

            for (var i = 0; i < response['data'].length; i++) {
               var site_name = response['data'][i][0];
               var site_results = response['data'][i][1];

               if (site_results) {
                  for (var j = 0; j < site_results.length; j++) {
                     var result_title = site_results[j][0];
                     var result_url = site_results[j][1];
                     var result_thumb = site_results[j][2];
                     var video_source = endpoint('/video_source' + encodeURI({
                           url: result_url,
                           redir: 1
                        }));

                     var card = '<div class="card"> \
                                    <img src="' + result_thumb + '" class="card-img-top" alt="..."> \
                                    <div class="card-body"> \
                                       <h5 class="card-title">' + site_name + '</h5> \
                                       <p class="card-text">' + result_title + '</p> \
                                       <a href="' + video_source + '" target="__blank" class="btn btn-primary">Mirar ahora</a> \
                                    </div> \
                                 </div>';

                     resultsContainer.append($(card));
                  }
               }
            }
         }
      })
   }
});
