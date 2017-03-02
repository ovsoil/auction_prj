(function () {
    'use strict';

    angular
        .module('auctionApp')
        .controller('NavbarController', NavbarController);

    NavbarController.$inject = ['$scope', 'Authentication'];

    function NavbarController($scope, Authentication) {
        var self = this;
        self.logout = logout;

        activate();

        function activate() {
            self.authenticated = Authentication.isAuthenticated();
        }

        function logout() {
            Authentication.logout();
        }
    }
})();
