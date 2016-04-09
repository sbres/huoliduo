/*
**
**
*/

angular.module('sbAdminApp')
    .controller('AllOrdersCtrl', function($scope, $position, $http, $window, $state, $timeout, $filter, $interval) {
        console.log('AllOrdersCtrl');

        /*
        **    START NEW ORDERS
        */
        $scope.new_orders = [];
        $scope.show_data = false;
        $scope.sound_on = true;

        var refresh_neworders = function(sound) {
            $http({
                method: 'POST',
                url: '/api/v0/product/orders/get_new',
                data: $.param({'secret' : 'cfdgvshbfjnkvemrgjw4hipfeuovyackfdsjhvafds'}),
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            }).then(function successCallback(response) {
                //console.log(response.data);
                if (angular.toJson($scope.new_orders) != angular.toJson(response.data))
                {
                    $scope.new_orders = response.data;
                    if (sound) {
                        if ($scope.sound_on) {
                            $.playSound('http://www.myinstants.com/media/sounds/alarm');
                        }
                    }
                }
            }, function errorCallback(response) {
                //TODO add Error message
            });
        }
        refresh_neworders(false);
        $scope.new_order_update = function(iod, secret, action){
            $http({
                method: 'POST',
                url: '/api/v0/product/order/maker_accept',
                data: $.param({oid: iod,
                               osecret: secret,
                               action: action,
                               secret : 'cfdgvshbfjnkvemrgjw4hipfeuovyackfdsjhvafds'
                }),
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            }).then(function successCallback(response) {
                //console.log(response.data);
                refresh_neworders(false);
                refresh_makingorders();
            }, function errorCallback(response) {
                refresh_neworders(false);
            });


        }

        $scope.makesound = function(){
            console.log("sound !");
            $.playSound('http://www.myinstants.com/media/sounds/sound-9______');
        }

        /*
        **    END NEW ORDERS
        */

        /*
        **    START MAKING ORDERS
        */
        $scope.making_orders = [];
        var refresh_makingorders = function() {
            $http({
                method: 'POST',
                url: '/api/v0/product/orders/get_making',
                data: $.param({'secret' : 'cfdgvshbfjnkvemrgjw4hipfeuovyackfdsjhvafds'}),
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            }).then(function successCallback(response) {
                //console.log(response.data);
                if (angular.toJson($scope.making_orders) != angular.toJson(response.data))
                {
                    $scope.making_orders = response.data;
                }
            }, function errorCallback(response) {
                //TODO add Error message
            });
        }
        refresh_makingorders();

        $scope.manufacturing_order_update = function(iod, secret){
            $http({
                method: 'POST',
                url: '/api/v0/product/orders/done',
                data: $.param({oid: iod,
                               osecret: secret,
                               secret : 'cfdgvshbfjnkvemrgjw4hipfeuovyackfdsjhvafds'
                }),
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            }).then(function successCallback(response) {
                //console.log(response.data);
                refresh_makingorders();
                refresh_waitingorders();
            }, function errorCallback(response) {
                refresh_makingorders();
            });


        }
        /*
        **    END MAKING ORDERS
        */



        /*
        **    START ORDERS TO PICK UP
        */
        $scope.wating_orders = [];
        var refresh_waitingorders = function() {
            $http({
                method: 'POST',
                url: '/api/v0/product/orders/waiting',
                data: $.param({'secret' : 'cfdgvshbfjnkvemrgjw4hipfeuovyackfdsjhvafds'}),
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            }).then(function successCallback(response) {
                //console.log(response.data);
                if (angular.toJson($scope.wating_orders) != angular.toJson(response.data))
                {
                    $scope.wating_orders = response.data;
                }
            }, function errorCallback(response) {
                //TODO add Error message
            });
        }
        refresh_waitingorders();

        $scope.waiting_update = function(iod, secret){
            $http({
                method: 'POST',
                url: '/api/v0/product/orders/sent',
                data: $.param({oid: iod,
                               osecret: secret,
                               secret : 'cfdgvshbfjnkvemrgjw4hipfeuovyackfdsjhvafds'
                }),
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            }).then(function successCallback(response) {
                //console.log(response.data);
                refresh_waitingorders();
            }, function errorCallback(response) {
                refresh_waitingorders();
            });


        }
        /*
        **    END ORDERS TO PICK UP
        */



        /*
         *      This is for refreshing the page
         */


        function updateTime() {
            //refresh_neworders(true);
            // Normally there is no need to refresh all
            // But you know if there is someone else
            // playing arround....
            //refresh_waitingorders();
            //refresh_makingorders();
            console.log('test');
          }
        var refresh = $interval(updateTime, 1000);

        $scope.$on("$destroy", function(){
             $interval.cancel(refresh);
        });


  });

