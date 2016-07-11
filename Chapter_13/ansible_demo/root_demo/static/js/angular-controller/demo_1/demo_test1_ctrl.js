app.controller('demo_test1_ctrl',function($scope, $http){
    $scope.touch_file = function() {
        alert('开始创建文件');
        $http.get('/demo_1/demo_api/touch_2/')
        .success(function(result){
            alert('创建文件成功');
            console.log(result)
        }).error(function(err){
            alert('创建文件失败');
            console.log(err)
        });
    };
});