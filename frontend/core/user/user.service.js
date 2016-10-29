'use strict';

angular.
  module('core.user').
  factory('User',['$resource',
    function($resource){
      return $resource('/api/v1/users/:userId/',
        {userId: '@userId'},
        {}
      );
    }
  ]);
