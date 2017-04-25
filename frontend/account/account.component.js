(function () {
    'use strict';

    angular
        .module('account')
        .component('account', {
            templateUrl: '/static/account/account.html',
            controller: AccountController
        });

    AccountController.$inject = ['$location', '$routeParams', 'User'];

    function AccountController($location, $routeParams, User) {
        var self = this;
        self.user = undefined;
        activate();

        function activate() {
            var userId = $routeParams.userId.substr(1)
            // User.get({userId: userId}, function(user) {
            //     self.user = user;
            // });
            User.get({userId: userId}).
                $promise.
                then(userSuccessFn).
                catch(userErrorFn);

            function userSuccessFn(data, status, headers, config) {
                self.user = data;
            }


            function userErrorFn(data, status, headers, config) {
                $location.url('/');
            }
        }
    }

})();
