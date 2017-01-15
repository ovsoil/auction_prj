(function () {
    'use strict';

    angular
        .module('core.good')
        .factory('Good', Good);

    Good.$inject = ['$resource']

    function Good($resource){
        return $resource('/api/v1/goods/:goodId/', {goodId: '@goodId'},{
            }
        );
    }
})();
