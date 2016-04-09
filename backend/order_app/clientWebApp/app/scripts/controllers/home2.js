'use strict';

/**
 * @ngdoc function
 * @name clientWebApp.controller:HomeCtrl2
 * @description
 * # HomeCtrl
 * Controller of the  clientWebApp
 */
angular
  .module('clientWebApp')
  .controller('HomeCtrl2', function () {
      $(document).ready(function() {
          $.material.init();
      });
    this.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];
  });
