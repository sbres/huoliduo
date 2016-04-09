'use strict';

/**
 * @ngdoc function
 * @name clientWebApp.controller:HomeCtrl
 * @description
 * # HomeCtrl
 * Controller of the clientWebApp
 */
angular
  .module('clientWebApp')
  .controller('HomeCtrl', function ($scope) {
      $(document).ready(function() {
          $.material.init();
      });

    this.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];
  });
