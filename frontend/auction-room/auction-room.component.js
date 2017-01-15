(function () {
    'use strict';

    angular
        .module('auctionRoom')
        .component('auctionRoom', {
            templateUrl: '/static/auction-room/auction-room.html',
            controller: AuctionRoomController
        });
    AuctionRoomController.$inject = ['$routeParams', '$http', '$timeout', 'Authentication', 'Good', 'Bid']
    function AuctionRoomController($routeParams, $http, $timeout, Authentication, Good, Bid){
        var self = this;
        self.submit_bid = submit_bid;
        self.setImage = setImage;
        self.setBids = setBids;
        self.auction_begin = auction_begin;
        self.auction_done = auction_done;
        self.start_time = new Date();
        self.stop_time = new Date();

        activate();

        function activate() {
            self.bids = [];
            self.current_bid = null;
            self.amount = 0;
            self.user_num = 0;
            self.good = Good.get({goodId: $routeParams.goodId}, function(good) {
                self.setImage(good.images[0]);
                self.start_time.setTime(Date.parse(good.start_time));
                self.stop_time.setTime(Date.parse(good.stop_time));
                // set status and deal callback
                var now = new Date()
                if (now < self.start_time) {
                    self.before_start = (self.start_time - now) / 1000;
                    // $timeout(self.auction_begin, self.start_time - now);
                    self.status = 'comming';
                }
                else if (now < self.stop_time) {
                    self.before_stop = (self.stop_time - now) / 1000;
                    // $timeout(self.auction_done, self.stop_time - now);
                    self.status = 'going';
                }
                else {
                    self.status = 'done';
                }
                self.setBids();
                });
        }

        function setImage(imageUrl) {
            self.mainImageUrl = imageUrl;
        }

        function setBids() {
            Bid.filterbygood($routeParams.goodId).
                success(function(data, status, headers, config) {
                    self.bids = data;
                    self.current_bid = data[0];
                    self.amount = self.current_bid.amount + self.good.bid_range;
                }).
                error(function(data, status, headers, config) {
                    self.bids = [];
                    alert(data);
                });
        }

        function submit_bid() {
            if (valid_bid(self.amount)) {
                Bid.bid.new({},{
                    good_id: self.good.id,
                    amount: self.amount
                },function(){
                    self.setBids();
                });
                // Bid.bid.new({
                //     good_id: self.good.id,
                //     amount: self.amount
                // }).
                //     $promise.
                //     then(
                //         self.setBids()
                //     ).
                //     catch(function(data){
                //         alert(data.data.good);
                //     });
            } else {
                alert('bid not valid!');
            }

            function valid_bid(amount) {
                if (self.status != 'going') {
                    return false;
                }
                if(self.bids == 0) {
                    return amount >= self.good.start_price &&
                        0 == (amount - self.good.start_price) % self.good.bid_range;
                } else {
                    return amount > self.current_bid.amount &&
                        0 == (amount - self.current_bid.amount) % self.good.bid_range;
                }
            }
        }

        function auction_begin() {
            // TODO begin auction
            // alert("Auction Start!");
            self.status = 'going';
        }

        function auction_done() {
            // TODO auction start
            // alert("Deal! Auction Done.");
            self.status = 'done';
        }
    }

})();
