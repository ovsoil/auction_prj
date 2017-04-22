(function () {
    'use strict';

    angular
        .module('core.bid')
        .factory('Bid', Bid);

    Bid.$inject = ['$resource', '$http']

    function Bid($resource, $http){
        return {
            bid: $resource('/api/v1/bids/:bidId/', {bidId: '@bidId'},{
                new: {method: 'POST'},
                delete: {method: 'DELETE'}
            }),
            filterbyuser: filterbyuser,
            filterbygood: filterbygood
        };

        function filterbyuser(userId) {
            return $http.get('/api/v1/users/' + userId + '/bids/')
        }

        function filterbygood(goodId) {
            return $http.get('/api/v1/goods/' + goodId + '/bids/')
        }
    }
})();
