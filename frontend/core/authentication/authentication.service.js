(function () {
    'use strict';

    angular
        .module('core.authentication')
        .factory('Authentication', Authentication);

    Authentication.$inject = ['$cookies', '$http', 'User'];

    function Authentication($cookies, $http, User) {
        var Authentication = {
            getCredentials: getCredentials,
            getAuthenticatedUser: getAuthenticatedUser,
            isAuthenticated: isAuthenticated,
            login: login,
            logout: logout,
            register: register,
            setAuthenticatedUser: setAuthenticatedUser,
            unauthenticate: unauthenticate
        };

        return Authentication;

        function getCredentials(){
            return {email: $scope.email, password: $scope.password};
        }

        function getAuthenticatedUser() {
            return  $cookies.getObject('authenticatedUser');
        }

        function isAuthenticated() {
            return !!$cookies.getObject('authenticatedUser');
        }

        function login(email, password) {
            return $http.post('/api/v1/auth/', {
                email: email, password: password
            }).then(loginSuccessFn, loginErrorFn);

            function loginSuccessFn(data, status, headers, config) {
                Authentication.setAuthenticatedUser(data.data);
                window.location = '/';
            }

            function loginErrorFn(data, status, headers, config) {
                console.error('Epic failure!');
            }
        }

        function logout() {
            return $http.delete('/api/v1/auth/')
                .then(logoutSuccessFn, logoutErrorFn);

            function logoutSuccessFn(data, status, headers, config) {
                Authentication.unauthenticate();

                window.location = '/';
            }

            function logoutErrorFn(data, status, headers, config) {
                console.error('Epic failure!');
            }
        }


        function register() {
            return User.create({
                    username: username,
                    email: email,
                    password: password
                }).
                $promise.
                then(registerSuccessFn).
                catch(registerErrorFn);

            function registerSuccessFn(data, status, headers, config) {
                Authentication.login(email, password);
            }

            function registerErrorFn(data, status, headers, config) {
                console.error('Epic failure!');
            }
        }

        function setAuthenticatedUser(user) {
            $cookies.putObject('authenticatedUser', user)
        }

        function unauthenticate() {
            $cookies.remove('authenticatedUser');
        }
    }
})();
