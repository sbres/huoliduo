var myApp = angular.module('clientWebApp', ['ngTouch', 'ngStorage', 'ui.router']);

myApp.config(function($stateProvider, $urlRouterProvider) {

  // For any unmatched url, redirect to /home
  $urlRouterProvider.otherwise("/home");

  // Now set up the states
  $stateProvider
    .state('home', {
        url: '/home',
        templateUrl: 'views/home.html',
        controller: 'HomeCtrl',
        controllerAs: 'home'
    })
    .state('home2', {
        url: '/home2',
        templateUrl: 'views/home2.html',
        controller: 'HomeCtrl2',
        controllerAs: 'home2'
    })
    .state('home3', {
        url: '/home3',
        templateUrl: 'views/home3.html',
        controller: 'HomeCtrl3',
        controllerAs: 'home3'
    })
    .state('home4', {
        url: '/home4',
        templateUrl: 'views/home4.html',
        controller: 'HomeCtrl4',
        controllerAs: 'home4'
    })
    .state('home5', {
        url: '/home5',
        templateUrl: 'views/home5.html',
        controller: 'HomeCtrl5',
        controllerAs: 'home5'
    })
    .state('order', {
        url: '/order',
        templateUrl: 'views/order.html',
        controller: 'OrderCtrl',
        controllerAs: 'order'
    })
    .state('order2', {
        url: '/order2',
        templateUrl: 'views/order2.html',
        controller: 'OrderCtrl2',
        controllerAs: 'order2'
    })
    .state('information', {
        url: '/information',
        templateUrl: 'views/information.html',
        controller: 'InfoCtrl',
        controllerAs: 'information'
    })
    .state('information2', {
        url: '/information2',
        templateUrl: 'views/information2.html',
        controller: 'InfoCtrl2',
        controllerAs: 'information2'
    });
});

myApp.run(['$rootScope', '$state', function($rootScope, $state) { $rootScope.$state = $state; }]);
