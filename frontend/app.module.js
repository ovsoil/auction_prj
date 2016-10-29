'use strict';

angular.
  module('auctionApp', [
    'ngRoute',
    'ngAnimate',
    'core',
    'auctionGallery',
    'auctionRoom',
    'register',
    'login',
    'account',
    'settings'
  ]);

angular.
  module('auctionApp').
  run(['$http',
    function($http){
      $http.defaults.xsrfHeaderName = 'X-CSRFToken';
      $http.defaults.xsrfCookieName = 'csrftoken';
    }
  ]);
