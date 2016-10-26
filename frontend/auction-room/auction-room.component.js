'use strict';

// Register `auctionRoom` component, along with its associated controller and template
angular.
  module('auctionRoom').
  component('auctionRoom', {
    templateUrl: '/static/auction-room/auction-room.html',
    controller: ['$routeParams', 'Good',
      function AuctionRoomController($routeParams, Good){
        this.good = Good.get({goodId: $routeParams.goodId});
      }
    ]
  });
