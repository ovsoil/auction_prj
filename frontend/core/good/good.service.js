'use strict';

angular.
  module('core.good').
  factory('Good',['$resource',
    function($resource){
      return $resource('/api/v1/goods/:goodId/',
        {goodId: '@goodId'},
        {}
      );
    }
  ]);
