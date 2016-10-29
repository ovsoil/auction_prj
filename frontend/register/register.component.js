/**
 * Register controller
 * @namespace register
 */
(function () {
  'use strict';

  angular
    .module('register')
    .component('register', {
      templateUrl: '/static/register/register.html',
      controller: RegisterController
    });

  RegisterController.$inject = ['$location', 'Authentication'];

  /**
   * @namespace RegisterController
   */
  function RegisterController($location, Authentication) {
    self = this;
    self.register = register;
    activate();

    /**
     * @name activate
     * @desc Actions to be performed when this controller is instantiated
     * @memberOf thinkster.authentication.controllers.RegisterController
     */
    function activate() {
      // If the user is authenticated, they should not be here.
      if (Authentication.isAuthenticated()) {
        $location.url('/');
      }
    }

    /**
     * @name register
     * @desc Register a new user
     * @memberOf thinkster.authentication.controllers.RegisterController
     */
    function register() {
      Authentication.register(self.email, self.password, self.username);
    }
  }
})();
