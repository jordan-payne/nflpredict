angular.module('nflpredict', ['ui.router', 'ui.grid', 'ui.grid.pinning', 'ui.grid.resizeColumns', 'ui.grid.autoResize'])
  .config(function ($stateProvider, $urlRouterProvider) {
    $urlRouterProvider.otherwise('/')

    $stateProvider
      .state('home', {
        url: '/',
        templateUrl: 'index.html'
      })
      .state('roster', {
        url: '/roster',
        templateUrl: 'roster.html',
        controller: 'IndexController as index'
      })
      .state('player_stats', {
        url: '/player_stats',
        templateUrl: 'player_stats.html'
      });

  })
  .controller('IndexController', function($http) {
    var index = this;

    index.gridOptions = {};

    index.gridOptions.columnDefs = [
      { name:'last_name', width:120},
      { name:'first_name', width:120},
      { name:'position', width:120},
      { name:'weight', width:120},
      { name:'height', width:120},
      { name:'years_pro', width:120},
      { name:'college', width:120}
    ];

    index.getPlayer = function(player) {
      $http.post('/get_player', player)
        .then(function successCallback(response) {
          index.result = response.data;
      }, function errorCallback(response) {
          index.result = response.data;
      });
    };

    index.getTeamRoster = function(team) {
      $http.post('/get_team_roster', team)
        .then(function successCallback(response) {
          index.result = response.data;
          index.gridOptions.data = response.data;
      }, function errorCallback(response) {
          index.result = response.data;
      });
    };

  })
