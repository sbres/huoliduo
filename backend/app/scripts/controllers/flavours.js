/**
 * Created by sbres on 12/11/15.
 */


angular.module('sbAdminApp')
  .controller('FlavoursCtrl', function($scope, $http) {


        $scope.flavours = [];
        $scope.errors = [];
        $scope.refresh_flavours = function() {
            $http({
                method: 'POST',
                url: '/api/v0/product/flavours/getadmin',
                data: $.param({'secret' : 'cfdgvshbfjnkvemrgjw4hipfeuovyackfdsjhvafds'}),
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            }).then(function successCallback(response) {
                //console.log(response.data);
                if (angular.toJson($scope.flavours) != angular.toJson(response.data))
                {
                    $scope.flavours = response.data;
                    console.log(response.data);
                }
            }, function errorCallback(response) {
                $scope.errors.push("Error");
            });
        }
        $scope.refresh_flavours();

        $scope.update_flavour = function(id, action){
            console.log(id);
            console.log(action);
            $http({
                method: 'POST',
                url: '/api/v0/product/flavours/setstatus',
                data: $.param({id: id,
                               'secret' : 'cfdgvshbfjnkvemrgjw4hipfeuovyackfdsjhvafds',
                               status: action
                }),
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            }).then(function successCallback(response) {
                //console.log(response.data);
                 $scope.refresh_flavours();
            }, function errorCallback(response) {
                $scope.refresh_flavours();
                $scope.errors.push("Error");
                console.log(response);
            });
        };

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
                $scope.refresh_flavours();
            }, function errorCallback(response) {
                $scope.refresh_flavours();
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
                $scope.refresh_flavours();
            }, function errorCallback(response) {
                $scope.refresh_flavours();
                $scope.errors.push("Error");
            });


        };

});