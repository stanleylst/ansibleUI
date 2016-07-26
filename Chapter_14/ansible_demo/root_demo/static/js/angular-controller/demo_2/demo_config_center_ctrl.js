app.controller('demo_config_center_ctrl', function($scope, $http) {
    get_all_data = function () {
        $http.get('/demo_2/ansible_yml_register_api/')
        .success(function (res) {
            console.log(res);
            _.each(res, function(i){
                i['yml_parameter'] = JSON.parse(i['yml_parameter']);
            })

            $scope.data = res;
        })
    }
    get_all_data()

    $scope.create_tag = function(tag, ins){
        $scope.operate_type = tag;
        if(tag == 'create'){
            $scope.yml_parameter = [];
        }
        if(tag == 'remove'|| tag == 'modify'){
            $scope.id = ins.id;
            $scope.yml_file = ins.yml_file;
            $scope.yml_maintenancer = ins.yml_maintenancer;
            $scope.yml_parameter = ins.yml_parameter;
            $scope.accept_host_group = ins.accept_host_group;
            $scope.comment = ins.comment;
        }
    };

    function guid() {
        function s4() {
            return Math.floor((1 + Math.random()) * 0x10000)
                .toString(16)
                .substring(1);
        }
        return s4() + s4() + '-' + s4() + '-' + s4() + '-' +
            s4() + '-' + s4() + s4() + s4();
    }


    $scope.add_more_parameter_func = function(){
        $scope.yml_parameter.push({'id': guid(), 'name': '', 'type': 'choice', 'values': '', 'comment': ''})
    };

    $scope.delete_parameter_func = function(id){
        console.log(id)
        console.log($scope.yml_parameter)
        $scope.yml_parameter = _.reject($scope.yml_parameter, function (i){ return i['id'] == id})
    };

    $scope.generate_config_func = function() {
        $scope.save_wait = true;
        if($scope.operate_type == 'create') {
            data = {'yml_file': $scope.yml_file,
                'yml_maintenancer': $scope.yml_maintenancer,
                'yml_parameter': JSON.stringify($scope.yml_parameter),
                'accept_host_group': $scope.accept_host_group,
                'comment': $scope.comment
            }
            $http.post('/demo_2/demo2_api/create_yml_file_define/', data)
                .success(function (res) {
                    if (res['flag'] == true) {
                        alert('定义创建成功')
                        get_all_data()
                    } else {
                        alert('定义创建失败')
                    }
                    $scope.save_wait = '';
                }).error(function (res) {
                alert('定义创建失败')
                $scope.save_wait = '';
            })
        }
        if($scope.operate_type == 'remove') {
            data = {'remove_id': $scope.id};
            $http.post('/demo_2/demo2_api/delete_yml_file_define/', data)
                .success(function (res) {
                    if (res['flag'] == true) {
                        alert('定义删除成功')
                        get_all_data()
                    } else {
                        alert('定义删除失败')
                    }
                    $scope.save_wait = '';
                }).error(function (res) {
                alert('定义删除失败')
                $scope.save_wait = '';
            })
        }
        if($scope.operate_type == 'modify') {
            data = {'id': $scope.id,
                'yml_file': $scope.yml_file,
                'yml_maintenancer': $scope.yml_maintenancer,
                'yml_parameter': JSON.stringify($scope.yml_parameter),
                'accept_host_group': $scope.accept_host_group,
                'comment': $scope.comment
            }
            $http.post('/demo_2/demo2_api/update_yml_file_define/', data)
                .success(function (res) {
                    if (res['flag'] == true) {
                        alert('定义更新成功')
                        get_all_data()
                    } else {
                        alert('定义更新失败')
                    }
                    $scope.save_wait = '';
                }).error(function (res) {
                    alert('定义更新失败')
                    $scope.save_wait = '';
            })
        }
    }


});