app.controller('demo_server_create_ctrl',function($scope, $http){
    get_all_data = function() {
        $http.get('/demo_2/ansible_host_api/')
        .success(function (res) {
            $scope.servers_list_all = res;
        })
    }

    get_all_data()


    $scope.generate_new_ansible_host_func = function() {
        $http.get('/demo_2/demo2_api/create_ansible_hosts/')
            .success(function (res) {
                alert('生成hosts成功')
            }).error(function (res) {
            alert('生成hosts失败')
        })
    }


});