angular.module('sbAdminApp')
  .controller('HoursStoresCtrl', function($scope, $http) {
    var date = new Date();
    var d = date.getDate();
    var m = date.getMonth();
    var y = date.getFullYear();

        $scope.stores = [];
        $scope.errors = [];
        $scope.selected = null;
        $scope.show_add = false;
        $scope.new_time = {open: new Date(1970, 0, 1, 8, 0, 0),
                            close: new Date(1970, 0, 1, 18, 0, 0),
                            day:null};
        $scope.events = [];
        $scope.eventSources = [$scope.events];
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

        $scope.alertOnEventClick = function( date, jsEvent, view){
            var r = confirm("Do want to delete it ?");
            if (r != true) {
                return;
            }

            $http({
                method: 'POST',
                url: '/api/v0/stores/admin/delopenhstore',
                data: $.param({'secret' : 'cfdgvshbfjnkvemrgjw4hipfeuovyackfdsjhvafds',
                                'id': date.id}),
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            }).then(function successCallback(response) {
                $scope.get_hours($scope.selected);
            }, function errorCallback(response) {
                $scope.errors.push("Error");
            });
        };

        $scope.alertOnResize = function(event, delta, revertFunc, jsEvent, ui, view ){
            var id = event.id;
            var start =  moment(event._start._d);
            var end = moment(event._end._d);

            if (start.get('day') != end.get('day'))
            {
                console.log(start);
                console.log(start.weekday());
                console.log(end.utcOffset());
                console.log(start._d.getUTCDay());
                console.log(end._d.getUTCDay());
                //check if end time is midnight...
                alert("We cant have two days on the same opening. Make a new opening.")
                return;
            }
            console.log("Frist :" + event._start._d);
            console.log("Send hour :" + start.utc().get('hour'));

            $http({
                method: 'POST',
                url: '/api/v0/stores/admin/editopenhstore',
                data: $.param({'secret' : 'cfdgvshbfjnkvemrgjw4hipfeuovyackfdsjhvafds',
                                'id': id,
                                'open_h': start.utc().get('hour'),
                                'open_min': start.get('minute'),
                                'close_h': end.utc().get('hour'),
                                'close_min': end.get('minute'),
                                'day': start.get('day')}),
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            }).then(function successCallback(response) {
                $scope.get_hours($scope.selected);

            }, function errorCallback(response) {
                console.log(response.data);
                $scope.errors.push("Error");
            });

        };

        $scope.uiConfig = {
          calendar:{
            height: "auto",
            editable: true,
              left: '',

            dayClick: $scope.alertEventOnClick,
            eventDrop: $scope.alertOnDrop,
            eventResize: $scope.alertOnResize,
              defaultView: 'agendaWeek',
              firstDay:1,
              eventClick: $scope.alertOnEventClick,
              eventResize: $scope.alertOnResize,
              eventDrop: $scope.alertOnResize,

          }
        };

        $scope.get_hours = function(id) {

            $http({
                method: 'POST',
                url: '/api/v0/stores/admin/getopenhstore',
                data: $.param({'secret' : 'cfdgvshbfjnkvemrgjw4hipfeuovyackfdsjhvafds',
                                'id': id}),
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            }).then(function successCallback(response) {
                console.log(response.data);
                console.log('get_hours');
                //$scope.eventSources = [];
                //$scope.eventSources.push(response.data);
                //$scope.events.push(response.data);
                $scope.is_data = true;
                $scope.events.splice(0,$scope.events.length)
                angular.forEach(response.data, function (event) {
                    $scope.events.push(event);
                });
                $scope.selected = id;

            }, function errorCallback(response) {
                $scope.errors.push("Error");
            });
        }

        $scope.addhour_stores = function() {
            console.log($scope.new_time);

            if ($scope.new_time.open == null ||
                $scope.new_time.close == null ||
                $scope.new_time.day == null )
            {
                alert("Please fill all the fields");
                return;
            }
            if ($scope.new_time.open >= $scope.new_time.close)
            {
                alert("You need to close the shop after you open it.");
                return;
            }

            console.log($scope.new_time.open.value);
            console.log($scope.new_time.open);
            var mom_o = moment($scope.new_time.open);
            var mom_c = moment($scope.new_time.close);

            //console.log(Date.parse($scope.new_time.open).getTime());
            $http({
                method: 'POST',
                url: '/api/v0/stores/admin/newopenhstore',
                data: $.param({'secret' : 'cfdgvshbfjnkvemrgjw4hipfeuovyackfdsjhvafds',
                                'id': $scope.selected,
                                'open_h': mom_o.get('hour'),
                                'open_min': mom_o.get('minute'),
                                'close_h': mom_c.get('hour'),
                                'close_min': mom_c.get('minute'),
                                'day': $scope.new_time.day}),
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            }).then(function successCallback(response) {
                $scope.get_hours($scope.selected);

            }, function errorCallback(response) {
                console.log(response.data);
                $scope.errors.push("Error");
            });
        }




        //Get open hours
        // Faire un fonction que avec le
    });

