'use strict';

/**
 * @ngdoc function
 * @name clientWebApp.controller:InfoCtrl2
 * @description
 * # InfoCtrl2
 * Controller of the clientWebApp
 */

angular
  .module('clientWebApp')
  .controller('InfoCtrl2', function($scope) {

    $scope.profile = {
        name: '',
        address1: '',
        address2: '',
        address3: ''
    };

      $scope.getName = function() {
        var item = localStorage.getItem("clientWebApp-name");
        if (item)
        { $scope.profile.name = item; }
      }
      $scope.getAddress1 = function() {
        var item = localStorage.getItem("clientWebApp-address1");
        if (item)
        { $scope.profile.address1 = item; }
      }
      $scope.getAddress2 = function() {
        var item = localStorage.getItem("clientWebApp-address2");
        if (item)
        { $scope.profile.address2 = item; }
      }
      $scope.getAddress3 = function() {
        var item = localStorage.getItem("clientWebApp-address3");
        if (item)
        { $scope.profile.address3 = item; }
      }

      $scope.setName = function() {
        localStorage.setItem("clientWebApp-name", $scope.profile.name);
      }
      $scope.setAddress1 = function() {
        localStorage.setItem("clientWebApp-address1", $scope.profile.address1);
      }
      $scope.setAddress2 = function() {
        localStorage.setItem("clientWebApp-address2", $scope.profile.address2);
      }
      $scope.setAddress3 = function() {
        localStorage.setItem("clientWebApp-address3", $scope.profile.address3);
      }

      $scope.update = function() {
        $scope.setName();
        $scope.setAddress1();
        $scope.setAddress2();
        $scope.setAddress3();
      };

      $(document).ready(function() {

          $scope.getName();
          $scope.getAddress1();
          $scope.getAddress2();
          $scope.getAddress3();

          $.material.init();
      });
    this.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];
  });
