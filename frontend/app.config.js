'use strict';

angular.
  module('auctionApp').
  config(['$locationProvider' ,'$routeProvider','$resourceProvider',
    function config($locationProvider, $routeProvider, $resourceProvider) {
      $locationProvider.html5Mode(true);
      $locationProvider.hashPrefix('!');
      $resourceProvider.defaults.stripTrailingSlashes = false;

      $routeProvider.
        when('/', {
        template: '<auction-gallery></auction-gallery>'
        }).
        when('/auction-room/:goodId', {
          template: '<auction-room></auction-room>'
        }).
        otherwise('/');
    }
  ]);
