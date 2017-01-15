(function (){
  'use strict';

  angular.
    module('login').
    component('login', {
      templateUrl: '/static/login/login.html',
      controller: LoginController
    });

  LoginController.$inject = ['$location', 'Authentication'];

  function LoginController($location, Authentication) {
    var self = this;
    self.login = login;
    activate();

    function activate() {
      if (Authentication.isAuthenticated()) {
        $location.url('/');
      }
    }

    function login() {
      Authentication.login(self.email, self.password);
    }
  }

})();
