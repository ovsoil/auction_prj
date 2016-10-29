/**
 * Authentication
 * @namespace core.authentication
 */
(function () {
  'use strict';

  angular
    .module('core.authentication')
    .factory('Authentication', Authentication);

  Authentication.$inject = ['$cookies', '$http'];


  /**
   * @namespace Authentication
   * @returns {Factory}
   */
  function Authentication($cookies, $http) {
    /**
     * @name Authentication
     * @desc The Factory to be returned
     */
    var Authentication = {
      getAuthenticatedUser: getAuthenticatedUser,
      isAuthenticated: isAuthenticated,
      login: login,
      logout: logout,
      register: register,
      setAuthenticatedUser: setAuthenticatedUser,
      unauthenticate: unauthenticate
    };

    return Authentication;

    ///////////////////

    /**
     * @name getAuthenticatedUser
     * @desc Return the currently authenticated user
     * @returns {object|undefined} User if authenticated, else `undefined`
     * @memberOf thinkster.authentication.services.Authentication
     */
    function getAuthenticatedUser() {
      if (!$cookies.authenticatedUser) {
        return;
      }

      return JSON.parse($cookies.authenticatedUser);
    }


    /**
     * @name isAuthenticated
     * @desc Check if the current user is authenticated
     * @returns {boolean} True is user is authenticated, else false.
     * @memberOf thinkster.authentication.services.Authentication
     */
    function isAuthenticated() {
      return !!$cookies.authenticatedUser;
    }


    /**
     * @name login
     * @desc Try to log in with email `email` and password `password`
     * @param {string} email The email entered by the user
     * @param {string} password The password entered by the user
     * @returns {Promise}
     * @memberOf thinkster.authentication.services.Authentication
     */
    function login(email, password) {
      return $http.post('/api/v1/auth/login/', {
        email: email, password: password
      }).then(loginSuccessFn, loginErrorFn);

      /**
       * @name loginSuccessFn
       * @desc Set the authenticated user and redirect to index
       */
      function loginSuccessFn(data, status, headers, config) {
        Authentication.setAuthenticatedUser(data.data);

        window.location = '/';
      }

      /**
       * @name loginErrorFn
       * @desc Log "Epic failure!" to the console
       */
      function loginErrorFn(data, status, headers, config) {
        console.error('Epic failure!');
      }
    }


    /**
     * @name logout
     * @desc Try to log the user out
     * @returns {Promise}
     * @memberOf thinkster.authentication.services.Authentication
     */
    function logout() {
      return $http.post('/api/v1/auth/logout/')
        .then(logoutSuccessFn, logoutErrorFn);

      /**
       * @name logoutSuccessFn
       * @desc Unauthenticate and redirect to index with page reload
       */
      function logoutSuccessFn(data, status, headers, config) {
        Authentication.unauthenticate();

        window.location = '/';
      }

      /**
       * @name logoutErrorFn
       * @desc Log "Epic failure!" to the console
       */
        function logoutErrorFn(data, status, headers, config) {
          console.error('Epic failure!');
        }
      }


      /**
       * @name register
       * @desc Try to register a new user
       * @param {string} email The email entered by the user
       * @param {string} password The password entered by the user
       * @param {string} username The username entered by the user
       * @returns {Promise}
       * @memberOf thinkster.authentication.services.Authentication
       */
      function register(email, password, username) {
        return $http.post('/api/v1/users/', {
          username: username,
          password: password,
          email: email
        }).then(registerSuccessFn, registerErrorFn);

        /**
         * @name registerSuccessFn
         * @desc Log the new user in
         */
        function registerSuccessFn(data, status, headers, config) {
          Authentication.login(email, password);
        }

        /**
         * @name registerErrorFn
         * @desc Log "Epic failure!" to the console
         */
        function registerErrorFn(data, status, headers, config) {
          console.error('Epic failure!');
        }
      }


      /**
       * @name setAuthenticatedUser
       * @desc Stringify the user object and store it in a cookie
       * @param {Object} user The acount object to be stored
       * @returns {undefined}
       * @memberOf thinkster.authentication.services.Authentication
       */
      function setAuthenticatedUser(user) {
        $cookies.authenticatedUser = JSON.stringify(user);
      }


      /**
       * @name unauthenticate
       * @desc Delete the cookie where the user object is stored
       * @returns {undefined}
       * @memberOf thinkster.authentication.services.Authentication
       */
      function unauthenticate() {
        delete $cookies.authenticatedUser;
      }
    }
})();
