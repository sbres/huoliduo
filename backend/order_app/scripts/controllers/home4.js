'use strict';

/**
 * @ngdoc function
 * @name clientWebApp.controller:HomeCtrl4
 * @description
 * # HomeCtrl4
 * Controller of the clientWebApp
 */
angular
  .module('clientWebApp')
  .controller('HomeCtrl4', function ($scope) {
      $(document).ready(function() {
          $.material.init();
      });

    this.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];
  });
