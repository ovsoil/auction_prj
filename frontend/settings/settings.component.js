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

    function SettingsController($location, $routeParams, Authentication, User) {
        var self = this;

        self.destroy = destroy;
        self.update = update;

        activate();

        function activate() {
            var authenticatedUser = Authentication.getAuthenticatedUser();
            var userId = $routeParams.userId.substr(1)

            // Redirect if not logged in
            if (!authenticatedUser) {
                console.warn(authenticatedUser);
                $location.url('/');
                // Snackbar.error('You are not authorized to view this page.');
            } else {
                // Redirect if logged in, but not the owner of this user.
                if (authenticatedUser.id.toString() !== userId) {
                    // debugger;
                    $location.url('/');
                    // Snackbar.error('You are not authorized to view this page.');
                }
            }

            User.get({userId: userId}).
                $promise.
                then(userSuccessFn).
                catch(userErrorFn);

            function userSuccessFn(data, status, headers, config) {
                self.user = data;
            }

            function userErrorFn(data, status, headers, config) {
                $location.url('/');
                // Snackbar.error('That user does not exist.');
            }
        }


        function destroy() {
            User.destroy(self.user.id).
                $promise.
                then(deleteUserSuccessFn).
                catch(deleteUserErrorFn);

            function deleteUserSuccessFn(data, status, headers, config) {
                Authentication.unauthenticate();
                window.location = '/';

                // Snackbar.show('Your user has been deleted.');
            }


            function deleteUserErrorFn(data, status, headers, config) {
                // Snackbar.error(data.error);
            }
        }


        function update() {
            User.update({userId: $routeParams.userId.substr(1)}, self.user).
                $promise.
                then(updateUserSuccessFn).
                catch(updateUserErrorFn);

            function updateUserSuccessFn(data, status, headers, config) {
                // Snackbar.show('Your user has been updated.');
                $location.url('/');
            }


            function updateUserErrorFn(data, status, headers, config) {
                // Snackbar.error(data.error);
            }
        }
    }
})();
