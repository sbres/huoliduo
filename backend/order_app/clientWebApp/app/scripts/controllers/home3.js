'use strict';

/**
 * @ngdoc function
 * @name clientWebApp.controller:HomeCtrl3
 * @description
 * # HomeCtrl3
 * Controller of the clientWebApp
 */
angular
  .module('clientWebApp')
  .controller('HomeCtrl3', function ($scope) {
      $(document).ready(function() {
          $.material.init();
      });

    this.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];
  });
