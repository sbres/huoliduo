/**
 * Created by sbres on 12/11/15.
 */


angular.module('sbAdminApp')
  .controller('StoresCtrl', function($scope, $http) {


        $scope.stores = [];
        $scope.errors = [];
        $scope.refresh_stores = function() {
            $http({
                method: 'POST',
                url: '/api/v0/stores/admin/getall',
                data: $.param({'secret' : 'cfdgvshbfjnkvemrgjw4hipfeuovyackfdsjhvafds'}),
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            }).then(function successCallback(response) {
                //console.log(response.data);
                if (angular.toJson($scope.flavours) != angular.toJson(response.data))
                {
                    $scope.stores = response.data;
                    console.log(response.data);
                }
            }, function errorCallback(response) {
                $scope.errors.push("Error");
            });
        }
        $scope.refresh_stores();

        $scope.update_store = function(id, action){
            $http({
                method: 'POST',
                url: '/api/v0/stores/admin/ocstore',
                data: $.param({id: id,
                               'secret' : 'cfdgvshbfjnkvemrgjw4hipfeuovyackfdsjhvafds',
                               action: action
                }),
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            }).then(function successCallback(response) {
                console.log(response.data);
                 $scope.refresh_stores();
            }, function errorCallback(response) {
                $scope.refresh_stores();
                console.log(response.data);
                $scope.errors.push("Error");
            });
        };


        $scope.add_new_store = function(name, city, lat, lng){
            $http({
                method: 'POST',
                url: '/api/v0/stores/admin/new',
                data: $.param({'secret' : 'cfdgvshbfjnkvemrgjw4hipfeuovyackfdsjhvafds',
                                name: name,
                                city: city,
                                lat: lat,
                                lng: lng
                }),
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            }).then(function successCallback(response) {
                 $scope.refresh_stores();
            }, function errorCallback(response) {
                $scope.refresh_stores();
                console.log(response.data);
                $scope.errors.push("Error");
            });
        }


        $scope.new_flavour = "";
        $scope.new_cn_name = "";
        $scope.new_price = 0;

        $scope.add_new_flavour = function(name, cn_name, price){
            if (name == "")
            {
                alert("Please add a name");
                return;
            }
            if (cn_name == "")
            {
                alert("Please add a Chinese name");
                return;
            }
            $http({
                method: 'POST',
                url: '/api/v0/product/flavours/new',
                data: $.param({name: name,
                                secret: 'cfdgvshbfjnkvemrgjw4hipfeuovyackfdsjhvafds',
                                CNname: cn_name,
                                price: price
                }),
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            }).then(function successCallback(response) {
                //console.log(response.data);
                $scope.refresh_stores();
            }, function errorCallback(response) {
                $scope.refresh_stores();
                $scope.errors.push("Error");
            });

        };

        $scope.change_flavour_value = function(id, type, old_val){
            var res;
            res = prompt("What is the new value ?", old_val);
            if (res == undefined)
            {
                alert("Nope");
                return;
            }
            if (res == old_val)
            {
                return;
            }
            $http({
                method: 'POST',
                url: '/api/v0/product/flavours/edit_existing',
                data: $.param({secret: 'cfdgvshbfjnkvemrgjw4hipfeuovyackfdsjhvafds',
                                type: type,
                                value: res,
                                id: id
                }),
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            }).then(function successCallback(response) {
                //console.log(response.data);
                $scope.refresh_stores();
            }, function errorCallback(response) {
                $scope.refresh_stores();
                $scope.errors.push("Error");
            });


        };

    });

