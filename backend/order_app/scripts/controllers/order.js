'use strict';

/**
 * @ngdoc function
 * @name clientWebApp.controller:OrderCtrl
 * @description
 * # OrderCtrl
 * Controller of the clientWebApp
 */

angular
  .module('clientWebApp')
  .controller('OrderCtrl', function($scope) {

    $scope.order = {
        shake1: '',
        shake2: '',
        shake3: '',
        shake4: ''
    };

    $scope.shake1 = false;
    $scope.shake2 = false;
    $scope.shake3 = false;
    $scope.shake4 = false;

    $scope.updateShakes = function(shakeNb) {
      if (shakeNb >= 1)
      { $scope.shake1 = true; $scope.order.shake1 = 'flavor'; }
      else
      { $scope.shake1 = false; $scope.order.shake1 = ''; }

      if (shakeNb >= 2)
      { $scope.shake2 = true; $scope.order.shake2 = 'flavor'; }
      else
      { $scope.shake2 = false; $scope.order.shake2 = ''; }
    
      if (shakeNb >= 3)
      { $scope.shake3 = true; $scope.order.shake3 = 'flavor'; }
      else
      { $scope.shake3 = false; $scope.order.shake3 = ''; }
    
      if (shakeNb >= 4)
      { $scope.shake4 = true; $scope.order.shake4 = 'flavor'; }
      else
      { $scope.shake4 = false; $scope.order.shake4 = ''; }
    
    };

      $(document).ready(function() {
          $scope.shake1 = false;
          $scope.shake2 = false;
          $scope.shake3 = false;
          $scope.shake4 = false;

          $.material.init();
      });
    this.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];
  });