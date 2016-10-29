'use strict';

// Register `auctionRoom` component, along with its associated controller and template
angular.
  module('auctionRoom').
  component('auctionRoom', {
    templateUrl: '/static/auction-room/auction-room.html',
    controller: ['$routeParams', 'Good',
      function AuctionRoomController($routeParams, Good){
        var self = this;
        self.hi = true;
        self.good = Good.get({goodId: $routeParams.goodId}, function(good) {
          self.setImage(good.images[0]);
        });

        self.setImage = function setImage(imageUrl) {
          self.mainImageUrl = imageUrl;
        // $scope.$apply();
        };
      }
    ]
  });
