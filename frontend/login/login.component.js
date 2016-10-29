(function (){
  'use strict';

  angular.
    module('login').
    component('login', {
      templateUrl: '/static/login/login.html',
      controller: LoginController
    });

  LoginController.$inject = ['$location', 'Authentication'];

  /**
  * @namespace LoginController
  */
  function LoginController($location, Authentication) {
    var self = this;
    self.login = login;
    activate();

    /**
    * @name activate
    * @desc Actions to be performed when this controller is instantiated
    * @memberOf thinkster.authentication.controllers.LoginController
    */
    function activate() {
      // If the user is authenticated, they should not be here.
      if (Authentication.isAuthenticated()) {
        $location.url('/');
      }
    }

    /**
    * @name login
    * @desc Log the user in
    * @memberOf thinkster.authentication.controllers.LoginController
    */
    function login() {
      Authentication.login(self.email, self.password);
    }
  }

})();
