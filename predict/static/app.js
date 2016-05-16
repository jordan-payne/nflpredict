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
  .constant('nfl_teams', [
    {'id': 'ARI', 'name': 'Arizona Cardinals'},
    {'id': 'ATL', 'name': 'Atlanta Falcons'},
    {'id': 'BAL', 'name': 'Baltimore Ravens'},
    {'id': 'BUF', 'name': 'Buffalo Bills'},
    {'id': 'CAR', 'name': 'Carolina Panthers'},
    {'id': 'CHI', 'name': 'Chicago Bears'},
    {'id': 'CIN', 'name': 'Cincinnati Bengals'},
    {'id': 'CLE', 'name': 'Cleveland Browns'},
    {'id': 'DAL', 'name': 'Dallas Cowboys'},
    {'id': 'DEN', 'name': 'Denver Broncos'},
    {'id': 'DET', 'name': 'Detroit Lions'},
    {'id': 'GB', 'name': 'Green Bay Packers'},
    {'id': 'HOU', 'name': 'Houston Texans'},
    {'id': 'IND', 'name': 'Indianapolis Colts'},
    {'id': 'JAX', 'name': 'Jacksonville Jaguars'},
    {'id': 'KC', 'name': 'Kansas City Chiefs'},
    {'id': 'STL', 'name': 'Los Angeles Rams'},
    {'id': 'MIA', 'name': 'Miami Dolphins'},
    {'id': 'MIN', 'name': 'Minnesota Vikings'},
    {'id': 'NE', 'name': 'New England Patriots'},
    {'id': 'NO', 'name': 'New Orleans Saints'},
    {'id': 'NYG', 'name': 'New York Giants'},
    {'id': 'NYJ', 'name': 'New York Jets'},
    {'id': 'OAK', 'name': 'Oakland Raiders'},
    {'id': 'PHI', 'name': 'Philidelphia Eagles'},
    {'id': 'PIT', 'name': 'Pittsburgh Steelers'},
    {'id': 'SD', 'name': 'San Diego Chargers'},
    {'id': 'SEA', 'name': 'Seattle Seahawks'},
    {'id': 'SF', 'name': 'San Francisco 49ers'},
    {'id': 'TB', 'name': 'Tampa Bay Buccaneers'},
    {'id': 'TEN', 'name': 'Tennessee Titans'},
    {'id': 'WAS', 'name': 'Washington Redskins'}

  ])
  .controller('IndexController', function($http, nfl_teams) {
    var index = this;
    index.gridOptions = {};
    index.teams = nfl_teams
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
