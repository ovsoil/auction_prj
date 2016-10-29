
/**
 * UserSettingsController
 * @namespace thinkster.users.controllers
 */
(function () {
  'use strict';

  angular
    .module('settings')
    .component('settings', {
      templateUrl: '/static/settings/settings.html',
      controller: SettingsController
    });

  SettingsController.$inject = [
    '$location', '$routeParams', 'Authentication', 'User'
  ];

  /**
   * @namespace SettingsController
   */
  function SettingsController($location, $routeParams, Authentication, User) {
    var self = this;

    self.destroy = destroy;
    self.update = update;

    activate();


    /**
     * @name activate
     * @desc Actions to be performed when this controller is instantiated.
     * @memberOf thinkster.users.controllers.UserSettingsController
     */
    function activate() {
      var authenticatedUser = Authentication.getAuthenticatedUser();

      // Redirect if not logged in
      if (!authenticatedUser) {
        $location.url('/');
        // Snackbar.error('You are not authorized to view this page.');
      } else {
        // Redirect if logged in, but not the owner of this user.
        if (authenticatedUser.id !== $routeParams.userId) {
          debugger;
          $location.url('/');
          // Snackbar.error('You are not authorized to view this page.');
        }
      }

      User.get({userId: $routeParams.userId}).then(userSuccessFn, userErrorFn);

      /**
       * @name userSuccessFn
       * @desc Update `user` for view
       */
      function userSuccessFn(data, status, headers, config) {
        self.user = data.data;
      }

      /**
       * @name userErrorFn
       * @desc Redirect to index
       */
      function userErrorFn(data, status, headers, config) {
        $location.url('/');
        // Snackbar.error('That user does not exist.');
      }
    }


    /**
     * @name destroy
     * @desc Destroy this user
     * @memberOf thinkster.users.controllers.UserSettingsController
     */
    function destroy() {
      User.destroy(self.user.id).then(userSuccessFn, userErrorFn);

      /**
       * @name userSuccessFn
       * @desc Redirect to index and display success snackbar
       */
      function userSuccessFn(data, status, headers, config) {
        Authentication.unauthenticate();
        window.location = '/';

        // Snackbar.show('Your user has been deleted.');
      }


      /**
       * @name userErrorFn
       * @desc Display error snackbar
       */
      function userErrorFn(data, status, headers, config) {
        // Snackbar.error(data.error);
      }
    }


    /**
     * @name update
     * @desc Update this user
     * @memberOf thinkster.users.controllers.UserSettingsController
     */
    function update() {
      User.update($routeParams.userId, self.user).then(userSuccessFn, userErrorFn);

      /**
       * @name userSuccessFn
       * @desc Show success snackbar
       */
      function userSuccessFn(data, status, headers, config) {
        // Snackbar.show('Your user has been updated.');
      }


      /**
       * @name userErrorFn
       * @desc Show error snackbar
       */
      function userErrorFn(data, status, headers, config) {
        // Snackbar.error(data.error);
      }
    }
  }
})();
