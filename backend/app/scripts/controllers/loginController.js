angular.module('sbAdminApp')
  .controller('LoginCtrl', function($scope, $http, $window, $state, $rootScope) {
  $scope.data = {"password": "",
				"username": ""};
  console.log('Hello');
  delete $window.localStorage["username"];
  delete $window.localStorage["password"];
       

  $scope.login = function () {
  	if ($scope.data["username"] == "" && $scope.data["password"] == "")
  	{
  		alert("Please enter a username or passw");
  		return;
  	}
  	console.log('Sending login.')
    $http({
            url: '/user/login',
            method: "POST",
            params: {'username': $scope.data["username"],
                     'password': $scope.data["password"]}
      }).then(
            function(results) {
                $window.localStorage["username"] = $scope.data["username"];
                $window.localStorage["password"] = $scope.data["password"];
                $state.go('dashboard.stats');
                //return to home 
            },
            function(errors) {
                alert("Worng passw or login.")
                console.log(errors);
            }
    );
  };

});