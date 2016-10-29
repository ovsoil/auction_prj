(function () {
  'use strict';

  angular
    .module('account')
    .component('account', {
      templateUrl: '/static/account/account.html',
      controller: AccountController
    });

  AccountController.$inject = ['$location', '$routeParams', 'User'];

  /**
  * @namespace AccountController
  */
  function AccountController($location, $routeParams, User) {
    var self = this;

    self.user = undefined;

    activate();

    /**
    * @name activate
    * @desc Actions to be performed when this controller is instantiated
    * @memberOf thinkster.users.controllers.UserController
    */
    function activate() {
      User.get({userId: $routeParams.userId}).then(userSuccessFn, userErrorFn);

      /**
      * @name userSuccessUser
      * @desc Update `user` on viewmodel
      */
      function userSuccessFn(data, status, headers, config) {
        self.user = data.data;
      }


      /**
      * @name userErrorFn
      * @desc Redirect to index and show error Snackbar
      */
      function userErrorFn(data, status, headers, config) {
        $location.url('/');
        // Snackbar.error('That user does not exist.');
      }
    }
  }

})();
