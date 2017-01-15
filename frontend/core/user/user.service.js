(function () {
    'use strict';

    angular
        .module('core.user')
        .factory('User', User);

    User.$inject = ['$resource'];

    function User($resource) {
        return $resource('/api/v1/users/:userId/', {userId: '@userId'}, {
            get: {method: 'GET'},
            create: {method: 'POST'},
            update: {method: 'PUT'},
            delete: {method: 'DELETE'}
        });
    }
})();
