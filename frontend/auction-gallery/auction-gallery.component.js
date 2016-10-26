'use strict';

// Register `auctionGallery` component, along with its associated controller and template
angular.
  module('auctionGallery').
  component('auctionGallery', {
    templateUrl: '/static/auction-gallery/auction-gallery.html',
    controller: ['Good',
      function AuctionGalleryController(Good){
        this.goods = Good.query();
      }
    ]
  });
