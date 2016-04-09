'use strict';

/**
 * @ngdoc function
 * @name clientWebApp.controller:OrderCtrl2
 * @description
 * # OrderCtrl2
 * Controller of the clientWebApp
 */

angular
  .module('clientWebApp')
  .controller('OrderCtrl2', function($scope) {

    $scope.order = {
        activity: 1,
    };

      $scope.getActivity = function() {
        var item = localStorage.getItem("clientWebApp-activity");
        if (item)
        { $scope.order.ctivity = Number(item); }
      }

      $scope.setActivity = function() {
        localStorage.setItem("clientWebApp-activity", $scope.order.activity);
      }

      $(document).ready(function() {

          $.material.init();

          $scope.getActivity();

          // var slider = document.getElementById('behaviour');

          // noUiSlider.create(slider, {
          //   orientation: "vertical",
          //   start: 1,
          //   step: 1,
          //   range: {
          //   'min': 0,
          //   'max': 2
          //   }
          // });

      });
    this.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];
  });