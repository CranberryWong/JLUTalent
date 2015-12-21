var myApp = angular.module('myapp', []);

myApp.config(function ($logProvider) {
  $logProvider.debugEnabled(false);
});

myApp.controller('UserController', function ($scope, $log, $timeout) {
  $scope.user = {};
  $scope.user.name = 'wangchen';
  $scope.user.email = 'i@wangchen0413.cn';
  $log.log('用户登录')
  $log.info('用户登录中')
  $log.warn('用户尝试登录次数过多')
  $log.error('登录失败')
  $log.debug('调试中')

  $scope.user.subscribe = function () {
    console.log($scope.user.name + ',您订阅的新闻将会发送到：' + $scope.user.email);
  };

  $scope.gameOn = function () {
    $log.log('游戏开始..');
    $timeout($scope.gameOver, 3000);
  };

  $scope.gameOver = function () {
    $log.info('游戏结束');
  };
});

myApp.controller('ShowController', function ($scope) {
  $scope.query = '';
  $scope.comparator = function (actual, expected) {
    return actual > expected;
  };
  $scope.shows = [
  {title:'浴血黑帮', subscribe:true, rate:9.2, updated:1409632203,
  description:'Donec id elit non mi porta gravida at eget metus. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus. Etiam porta sem malesuada magna mollis euismod. Donec sed odio dui.Donec id elit non mi porta gravida at eget metus. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus. Etiam porta sem malesuada magna mollis euismod. Donec sed odio dui.'},
  {title:'权力的游戏', subscribe:false, rate:9.6, updated:1401712225,
  description:'Donec id elit non mi porta gravida at eget metus. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus. Etiam porta sem malesuada magna mollis euismod. Donec sed odio dui.Donec id elit non mi porta gravida at eget metus. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus. Etiam porta sem malesuada magna mollis euismod. Donec sed odio dui.'},
  {title:'冰雪暴', subscribe:true, rate:8.9, updated:1407673821,
  description:'Donec id elit non mi porta gravida at eget metus. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus. Etiam porta sem malesuada magna mollis euismod. Donec sed odio dui.Donec id elit non mi porta gravida at eget metus. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus. Etiam porta sem malesuada magna mollis euismod. Donec sed odio dui.'},
  {title:'摩登家庭', subscribe:true, rate:9.5, updated:142072023,
  description:'Donec id elit non mi porta gravida at eget metus. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus. Etiam porta sem malesuada magna mollis euismod. Donec sed odio dui.Donec id elit non mi porta gravida at eget metus. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus. Etiam porta sem malesuada magna mollis euismod. Donec sed odio dui.'},
  {title:'行尸走肉', subscribe:false, rate:9.3, updated:1420115455,
  description:'Donec id elit non mi porta gravida at eget metus. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus. Etiam porta sem malesuada magna mollis euismod. Donec sed odio dui.Donec id elit non mi porta gravida at eget metus. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus. Etiam porta sem malesuada magna mollis euismod. Donec sed odio dui.'}

  ];
});
