'use strict';

/**
 * @ngdoc function
 * @name clientWebApp.controller:InfoCtrl
 * @description
 * # InfoCtrl
 * Controller of the clientWebApp
 */

angular
  .module('clientWebApp')
  .controller('InfoCtrl', function($scope) {

    $scope.profile = {
        sex: 'Male' ,
        age: '',
        weight: '',
        height: ''
    };

      $scope.getAge = function() {
        var item = localStorage.getItem("clientWebApp-age");
        if (item)
        { $scope.profile.age = Number(item); }
      }
      $scope.getWeight = function() {
        var item = localStorage.getItem("clientWebApp-weight");
        if (item)
        { $scope.profile.weight = Number(item); }
      }
      $scope.getHeight = function() {
        var item = localStorage.getItem("clientWebApp-height");
        if (item)
        { $scope.profile.height = Number(item); }
      }
      $scope.getSex = function() {
        var item = localStorage.getItem("clientWebApp-sex");
        if (item)
        { $scope.profile.sex = item; }
      }

      $scope.setAge = function() {
        localStorage.setItem("clientWebApp-age", $scope.profile.age);
      }
      $scope.setWeight = function() {
        localStorage.setItem("clientWebApp-weight", $scope.profile.weight);
      }
      $scope.setHeight = function() {
        localStorage.setItem("clientWebApp-height", $scope.profile.height);
      }
      $scope.setSex = function() {
        localStorage.setItem("clientWebApp-sex", $scope.profile.sex);
      }

      $scope.update = function() {
        $scope.setAge();
        $scope.setWeight();
        $scope.setHeight();
        $scope.setSex();
      };

      $scope.clearData = function() {
        $scope.profile.age = '';
        $scope.profile.weight = '';
        $scope.profile.height = '';
      }

      $(document).ready(function() {

          $scope.getAge();
          $scope.getWeight();
          $scope.getHeight();
          $scope.getSex();

          $.material.init();
      });
    this.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];
  });


