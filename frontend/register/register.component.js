(function () {
    'use strict';

    angular
        .module('register')
        .component('register', {
            templateUrl: '/static/register/register.html',
            controller: RegisterController
        });

    RegisterController.$inject = ['$location', 'Authentication', 'User'];

    function RegisterController($location, Authentication, User) {
        self = this;
        self.register = register;
        activate();

        function activate() {
            // If the user is authenticated, they should not be here.
            if (Authentication.isAuthenticated()) {
                $location.url('/');
            }
        }

        function register($event){
            User.create({
                username: self.username,
                email: self.email,
                password: self.password
            }).
                $promise.
                then(
                    Authentication.login(self.email, self.password)).
                catch(function(data){
                    alert(data.data.username);
                });
        }
    }
})();
