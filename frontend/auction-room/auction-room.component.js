(function () {
    'use strict';

    angular
        .module('auctionRoom')
        .component('auctionRoom', {
            templateUrl: '/static/auction-room/auction-room.html',
            controller: AuctionRoomController
        });
    AuctionRoomController.$inject = ['$routeParams', '$http', '$timeout', '$sce', 'Authentication', 'Good', 'Bid']
    function AuctionRoomController($routeParams, $http, $timeout, $sce, Authentication, Good, Bid){
        var self = this;
        self.setImage = setImage;
        self.setBids = setBids;
        self.valid_price = valid_price;
        self.valid_bid = valid_bid;
        self.proposal_price = proposal_price;
        self.raise_price = raise_price;
        self.submit_bid = submit_bid;
        self.auction_begin = auction_begin;
        self.auction_done = auction_done;
        self.get_info = get_info;
        self.start_time = new Date();
        self.stop_time = new Date();

        activate();

        function activate() {
            self.bids = [];
            self.price = 0;
            self.user_num = 0;
            self.get_info();
            self.good = Good.get({goodId: $routeParams.goodId}, function(good) {
                self.setImage(good.images[0]);
                self.start_time.setTime(Date.parse(good.start_time));
                self.stop_time.setTime(Date.parse(good.stop_time));
                self.details = $sce.trustAsHtml(good.details);
                // set status and deal callback
                var now = new Date()
                if (now < self.start_time) {
                    self.before_start = (self.start_time - now) / 1000;
                    $timeout(self.auction_begin, self.start_time - now);
                    self.status = 'comming';
                }
                else if (now < self.stop_time) {
                    self.before_stop = (self.stop_time - now) / 1000;
                    $timeout(self.auction_done, self.stop_time - now);
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
            Bid.filterbygood($routeParams.goodId).then(
                function(data, status, headers, config) {
                    self.bids = data.data;
                    // TODO: check consistency of the bids data
                    // 时间顺序是否与价格顺序一致
                    self.price = self.proposal_price();
                },
                function(data, status, headers, config) {
                    self.bids = [];
                    alert(data);
                }
            );
        }

        function valid_price(price) {
            if(self.bids == 0) {
                return price >= self.good.start_price && 0 == (price - self.good.start_price) % self.good.bid_range;
            } else {
                return price > self.bids[0].price && 0 == (price - self.bids[0].price) % self.good.bid_range;
            }
        }

        function valid_bid(price) {
            return self.status == 'going' && self.valid_price(price);
        }

        function proposal_price() {
            if(self.bids == 0) {
                return self.good.start_price;
            } else {
                return self.bids[0].price + self.good.bid_range;
            }
        }

        function raise_price() {
            if(self.valid_price(self.price + self.good.bid_range)){
                self.price = self.price + self.good.bid_range;
            } else {
                self.price = self.proposal_price();
            }
        }

        function submit_bid() {
            if (self.valid_bid(self.price)) {
                Bid.bid.new({},{
                    good_id: self.good.id,
                    price: self.price
                },function(){
                    self.setBids();
                });
            } else {
                alert('bid not valid!');
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
            if (self.bids == 0){
                // TODO 流拍
                alert("Not bidder!")
            }
        }

        function get_info() {
            $http.get('/api/v1/webinfo/').then(
                function(data, status, headers, config) {
                    self.webinfo = data.data;
                },
                function(data, status, headers, config) {
                    alert(data);
                }
            );
        }
    }

})();
