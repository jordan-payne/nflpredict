angular.module('nflpredict', [])
  .controller('IndexController', function($http, $scope) {
    var index = this;

    index.getPlayer = function(player) {
      console.log('Executing...')
      $http.post('/get_player', player)
        .then(function successCallback(response) {
          console.log(response);
          index.result = response;
      }).then(function errorCallback(response) {
          index.result = response.data;
      });
    };

  })
