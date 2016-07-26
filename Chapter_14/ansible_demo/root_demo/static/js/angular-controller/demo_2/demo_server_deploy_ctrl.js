app.controller('demo_server_deploy_ctrl',function($scope, $http){
    get_all_data = function() {
        $http.get('/demo_2/ansible_host_api/')
        .success(function (res) {
            $scope.servers_list_all = res;
        })
    }

    get_all_data()


});