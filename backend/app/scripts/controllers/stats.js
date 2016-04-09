

angular.module('sbAdminApp')
    .controller('StatsCtrl', function($scope, $position, $http, $window, $state, $timeout, $filter) {
        console.log('StatsCtrl');
        $scope.init = function(){
            console.log('StatsCtrl');
            var user = $window.localStorage["username"];
            var password = $window.localStorage["password"];
            $scope.data = {'getregistered': 0,
                           'getactive': 0,
                           'errors': [],
            };
            var req = {
                 method: 'GET',
                 url: '/api/user/getregistered',
                 headers: {
                   'Authorization': user + ':' + password
                 },
                };

            $http(req).then(function(res){
                console.log('OK');
                console.log(res);
                console.log(res.data);
                $scope.data.getregistered = res.data;
            }, function(res){
                $scope.data.errors.push(res.data);
                console.log('KO');
            });
            req.url = '/api/user/getactive';
            $http(req).then(function(res){
                $scope.data.getactive = res.data;
            }, function(res){
                $scope.data.errors.push(res.data);
                console.log('KO');
            });
            req.url = '/api/video/getnbvideos';
            $http(req).then(function(res){
                console.log("RES:");
                console.log(res);
                $scope.data.shoshsent = res.data;
            }, function(res){
                $scope.data.errors.push(res.data);
                console.log('KO');
            });

            req.url = '/api/video/videoviews';
            $http(req).then(function(res){
                console.log("RES:");
                console.log(res);
                $scope.data.videoviews = res.data;
            }, function(res){
                $scope.data.errors.push(res.data);
                console.log('KO');
            });


            $scope.chartUserIncriptionConfig = {
                options: {
                    chart: {
                        zoomType: 'x'
                    },
                    rangeSelector: {
                        enabled: true,
                        selected : 0,
                    },
                    navigator: {
                        enabled: true
                    }
                },
                global: {
		            useUTC: true
	            },
                yAxis: {
                    min: 0,
                    minRange: 0.1,
                },
                series: [],
                title: {
                    text: 'Inscription history'
                },
                useHighStocks: true
            };

            req.url = '/api/user/GetInscriptions';
            //Here we can send since_day param
            $http(req).then(function(res){
                console.log("GetInscriptionsV2:");
                console.log(res);
                //$scope.data.getInscriptionsSince = res.data;
                $scope.chartUserIncriptionConfig.series.push({
                id: 1,
                data: res.data.data
            });
            }, function(res){
                $scope.data.errors.push(res.data);

                console.log('KO');
            });


            $scope.openTimeConfig = {
                options: {
                    chart: {
                        zoomType: 'x'
                    },
                    rangeSelector: {
                        enabled: true,
                        selected : 0,
                    },
                    navigator: {
                        enabled: true
                    }
                },
                series: [],
                title: {
                    text: 'Time spend on the App'
                },
                yAxis: {
                    min: 0,
                    minRange: 0.1,
                },
                useHighStocks: true
            };
            req.url = '/api/shosha/opentime';
            //Here we can send since_day param
            $http(req).then(function(res){
                console.log(res);
                //$scope.data.getInscriptionsSince = res.data;
                $scope.openTimeConfig.series.push({
                id: 1,
                data: res.data.data
            });
            }, function(res){
                $scope.data.errors.push(res.data);

                console.log('KO');
            });

            $scope.openTimeConfigSession = {
                options: {
                    chart: {
                        zoomType: 'x'
                    },
                    rangeSelector: {
                        enabled: true,
                        selected : 0,
                    },
                    navigator: {
                        enabled: true
                    }
                },
                series: [],
                title: {
                    text: 'Time spend on the App per session'
                },
                yAxis: {
                    min: 0,
                    minRange: 0.1,
                },
                useHighStocks: true
            };

            req.url = '/api/shosha/opentimesession';
            //Here we can send since_day param
            $http(req).then(function(res){
                console.log(res);
                //$scope.data.getInscriptionsSince = res.data;
                $scope.openTimeConfigSession.series.push({
                id: 1,
                data: res.data.data
            });
            }, function(res){
                $scope.data.errors.push(res.data);

                console.log('KO');
            });

            $scope.videoday = {
                options: {
                    chart: {
                        polar: true,
                        type: 'line'
                    }
                },
                yAxis: {
                    gridLineInterpolation: 'polygon',
                    lineWidth: 0,
                    min: 0
                },
                xAxis: {
                    categories: ['Sunday/Dim', 'Monday', 'Tuesday',
                    'Wednesday', 'Thursday', 'Friday', 'Saturday'],
                    tickmarkPlacement: 'on',
                    lineWidth: 0
                },
                series: [],
                title: {
                    text: '% Shosh sent per day'
                },

                loading: false
            };

            req.url = '/api/video/videoday';
            //Here we can send since_day param
            $http(req).then(function(res){
                console.log(res);
                $scope.videoday.series.push({
                name: '% Shosh sent per day of the week',
                data: res.data,
                pointPlacement: 'on'
            });
            }, function(res){
                $scope.data.errors.push(res.data);

                console.log('KO');
            });

            ///////////////////////////////////////////////


            $scope.OpenAppPerUser = {
                options: {
                    chart: {
                        zoomType: 'x'
                    },
                    rangeSelector: {
                        enabled: true,
                        selected : 0,
                    },
                    navigator: {
                        enabled: true
                    }
                },
                series: [],
                title: {
                    text: 'Nb of time app was opened / Users'
                },
                yAxis: {
                    min: 0,
                    minRange: 0.1,
                },
                useHighStocks: true
            };

            req.url = '/api/user/OpenAppPerUser ';
            //Here we can send since_day param
            $http(req).then(function(res){
                console.log(res);
                $scope.OpenAppPerUser.series.push({
                name: 'Nb of times app was openned by user',
                data: res.data.data,
                pointPlacement: 'on'
            });
            }, function(res){
                $scope.data.errors.push(res.data);

                console.log('KO');
            });

            $scope.AppErros = {
                options: {
                    chart: {
                        zoomType: 'x'
                    },
                    rangeSelector: {
                        enabled: true,
                        selected : 0,
                    },
                    navigator: {
                        enabled: true
                    }
                },
                series: [],
                title: {
                    text: 'Number of errors'
                },
                yAxis: {
                    min: 0,
                    minRange: 0.1,
                },
                useHighStocks: true
            };

            req.url = '/api/shosha/geterrors ';
            //Here we can send since_day param
            $http(req).then(function(res){
                console.log(res);
                $scope.AppErros.series.push({
                name: 'Nb of erros',
                data: res.data.data,
                pointPlacement: 'on'
            });
            }, function(res){
                $scope.data.errors.push(res.data);

                console.log('KO');
            });




            $scope.getshoshcamera = {
                options: {
                    chart: {
                        polar: true,
                        type: 'pie'
                    }
                },
                xAxis: {
                    categories: ['back camera', 'front camera'],
                    tickmarkPlacement: 'on',
                    lineWidth: 0
                },
                series: [],
                title: {
                    text: 'Camera used to shosh'
                },

                loading: false
            };


            req.url = '/api/shosha/getshoshcamera';
            //Here we can send since_day param
            $http(req).then(function(res){
                console.log(res);
                $scope.getshoshcamera.series.push(
                    {'data': [
                        {name : 'Front',
                            y: res.data.data.front,
                        color: '#33CC33'},
                        {name : 'Back',
                            y: res.data.data.back,
                        color: '#FF33CC'}
                    ]}
                );
            }, function(res){
                $scope.data.errors.push(res.data);

                console.log('KO');
            });



            $scope.OpenAppHour = {
                yAxis: {
                    min: 0,
                    minRange: 0.1,
                    title: {
                        text: "Nombre d'overtures de l'app"
                    }
                },
                xAxis: {
                    title: {
                        text: "Heure d'ouverture"
                    }
                },
                series: [],
                title: {
                    text: 'Open app per hour.'
                },
                useHighStocks: false
            };

            req.url = '/api/shosha/getopenhours';
            //Here we can send since_day param
            $http(req).then(function(res){
                //$scope.data.getInscriptionsSince = res.data;
                $scope.OpenAppHour.series.push({
                id: 1,
                name: 'openings',
                data: res.data
            });
            }, function(res){
                $scope.data.errors.push(res.data);

                console.log('KO');
            });



             $scope.OpenAppDay = {
                yAxis: {
                    min: 0,
                    minRange: 0.1,
                    title: {
                        text: "Nombre d'overtures de l'app"
                    }
                },
                xAxis: {
                    title: {
                        text: "Jour d'ouverture"
                    },
                    categories: ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
                        'Friday', 'Saturday','Sunday']
                },
                series: [],
                title: {
                    text: 'Open app per weekday.'
                },
                useHighStocks: false
            };

            req.url = '/api/shosha/getopendays';
            //Here we can send since_day param
            $http(req).then(function(res){
                //$scope.data.getInscriptionsSince = res.data;
                $scope.OpenAppDay.series.push({
                id: 1,
                name: 'openings',
                data: res.data
            });
            }, function(res){
                $scope.data.errors.push(res.data);

                console.log('KO');
            });



            $scope.last_open_hour = $filter("date")(Date.now(), 'yyyy-MM-dd');


            $scope.SinceLastOpening = {
                yAxis: {
                    min: 0,
                    minRange: 0.1,
                    title: {
                        text: "Nombre d'overtures de l'app"
                    }
                },
                xAxis: {
                    title: {
                        text: "Jour d'ouverture"
                    },
                },
                global: {
		            useUTC: true
	            },
                series: [],
                title: {
                    text: 'Open app per weekday.'
                },
                useHighStocks: true


            };

            req.url = '/api/shosha/sincelastopen';
            req.params = {'since': $scope.last_open_hour};

            //Here we can send since_day param
            $http(req).then(function(res){
                //$scope.data.getInscriptionsSince = res.data;
                $scope.SinceLastOpening.series.push({
                id: 1,
                name: '% of ',
                data: res.data
            });
            }, function(res){
                $scope.data.errors.push(res.data);
                console.log('KO');
            });



            $scope.chartVideoDailyViews = {
                options: {
                    chart: {
                        zoomType: 'x'
                    },
                    rangeSelector: {
                        enabled: true,
                        selected : 0,
                    },
                    navigator: {
                        enabled: true
                    }
                },
                global: {
		            useUTC: true
	            },
                yAxis: {
                    min: 0,
                    minRange: 0.1,
                },
                series: [],
                title: {
                    text: 'Daily views of videos'
                },
                useHighStocks: true
            };

            req.url = '/api/video/videoveiwperday';
            //Here we can send since_day param
            $http(req).then(function(res){
                console.log("videoveiwperday:");
                console.log(res);
                //$scope.data.getInscriptionsSince = res.data;
                $scope.chartVideoDaylyViews.series.push({
                id: 1,
                data: res.data
            });
            }, function(res){
                $scope.data.errors.push(res.data);

                console.log('KO');
            });


            $scope.userContacts = {
                options: {
                    chart: {
                        zoomType: 'x'
                    },
                    rangeSelector: {
                        enabled: true,
                        selected : 0,
                    },
                    navigator: {
                        enabled: true
                    }
                },
                global: {
		            useUTC: true
	            },
                yAxis: {
                    min: 0,
                    minRange: 0.1,
                },
                series: [],
                title: {
                    text: 'Daily views of videos'
                },
                useHighStocks: true
            };

            req.url = '/api/video/videoveiwperday';
            //Here we can send since_day param
            $http(req).then(function(res){
                console.log("videoveiwperday:");
                console.log(res);
                //$scope.data.getInscriptionsSince = res.data;
                $scope.userContacts.series.push({
                id: 1,
                data: res.data
            });
            }, function(res){
                $scope.data.errors.push(res.data);

                console.log('KO');
            });







        /////////////////////////////////////
        /////       End INIT            /////
        /////////////////////////////////////
        };















        $scope.refresh = function(){
            console.log('Refresh');
            $timeout(function() {
            $state.go('dashboard.stats', {}, { reload: true });
                        }, 0);
        };

        $scope.SinceLastOpening_refresh = function(){
            console.log('Hello');
            console.log('SinceLastOpening_refresh' + $scope.last_open_hour);
            var user = $window.localStorage["username"];
            var password = $window.localStorage["password"];
            var req = {
                 method: 'GET',
                 url: '/api/shosha/sincelastopen',
                 headers: {
                   'Authorization': user + ':' + password
                 },
                 params :{'since': $scope.last_open_hour},
                };

            //Here we can send since_day param
            $http(req).then(function(res){
                //$scope.data.getInscriptionsSince = res.data;
                $scope.SinceLastOpening.series = [];
                $scope.SinceLastOpening.series.push({
                id: 2,
                name: '% of ',
                data: res.data
            });
            }, function(res){
                $scope.data.errors.push(res.data);
                console.log('KO');
            });

        }
  });


/**
 * Created by sbres on 08/09/15.
 */
