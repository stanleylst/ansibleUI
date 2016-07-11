app.factory('timer',['$rootScope',function($rootScope){
    var updateClock = function()
    {    
        $rootScope.clock = new Date();
    };
    var timer = setInterval(function()
    {    
      $rootScope.$apply(updateClock);
    }, 1000);
}]);
