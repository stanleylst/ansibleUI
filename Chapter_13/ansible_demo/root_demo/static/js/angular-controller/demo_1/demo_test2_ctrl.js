app.controller('demo_test2_ctrl',function($scope, $http){
    $scope.touch_file = function(filename) {
        $scope.ansible_log = '';
        if(_.isEmpty(filename)){
            alert('输入不能为空')
            return;
        }
        $scope.main_msg = '开始创建文件,请耐心等待';
        data = {'filename': filename}
        $http.post('/demo_1/demo_api/touch_8/', data)
        .success(function(result){
            alert(result['msg']);
            console.log(result)
            $scope.ansible_log = result['output'];
            $scope.main_msg = '';
        }).error(function(err){
            console.log(err)
        });
    };
});