'use strict';

/**
 * @ngdoc function
 * @name clientWebApp.controller:HomeCtrl5
 * @description
 * # HomeCtrl5
 * Controller of the clientWebApp
 */
angular
  .module('clientWebApp')
  .controller('HomeCtrl5', function ($scope) {
      $(document).ready(function() {
          $.material.init();
      });

    this.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];
  });
