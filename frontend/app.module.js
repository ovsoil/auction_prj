'use strict';

angular.
  module('auctionApp', [
  'ngRoute',
  'core',
  'auctionGallery',
  'auctionRoom'
]);

angular.
  module('auctionApp').
  run(['$http',
    function($http){
      $http.defaults.xsrfHeaderName = 'X-CSRFToken';
      $http.defaults.xsrfCookieName = 'csrftoken';
    }
  ]);
