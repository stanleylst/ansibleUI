app.controller('demo_operate_interface_ctrl',function($scope, $http){

    get_all_data = function () {
        $http.get('/demo_2/ansible_yml_register_api/')
        .success(function (res) {
            console.log(res);
            _.each(res, function(i){
                i['yml_parameter'] = JSON.parse(i['yml_parameter']);
                i['operate'] = {};
                _.each(i['yml_parameter'], function(j){
                    if(!_.isEmpty(j['values'])){
                        i['operate'][j['name']] = j['values'].split('\n')[0];
                        j['values'] = j['values'].split('\n')
                    }else{
                        i['operate'][j['name']] = '';
                        j['values'] = '';
                    }
                })
                console.log(i['yml_parameter'])
            })
            $scope.data = res;
        })
    }
    get_all_data()

    $scope.fill_data_func = function(data){
        $scope.fill_data = data;
        console.log(data['accept_host_group'])
        $http.get('/demo_2/ansible_host_api/')
        .success(function (res) {
            $scope.select_servers = [];
            console.log(res)
            _.each(res, function(i){
                if(i['group'] == data['accept_host_group']){
                    i['checked'] = true;
                    $scope.select_servers.push(i)
                }
            })
        })

    }


    $scope.read_flag = false;
    $scope.execute_read = function() {
        fill_data = angular.copy($scope.fill_data);
        fill_data['ansible_hosts'] = [];
        console.log($scope.select_servers)
        _.each($scope.select_servers, function(j){
            if(j['checked']){
                fill_data['ansible_hosts'].push(j['name']);
            }
        });
        console.log(fill_data)
        if(_.isEmpty(fill_data)){
            alert('hosts不能为空')
            return;
        }else{
            fill_data['operate']['ansible_hosts'] = fill_data['ansible_hosts'].join(':')
        }
        $scope.ansible_log = '';
        $scope.read_flag = true;
        $scope.state = 'PENDING';
        $scope.yml_file = fill_data.yml_file;
        data = {'yml_file': fill_data.yml_file, 'operate': fill_data.operate};
        $http.post('/demo_2/demo2_api/execute_yml_ansible/', data)
        .success(function(result){
            $scope.task_id = result['task_id'];
            read_log({'seek': 0 , 'task_id': result['task_id'], 'log_file': result['log_file']});
            $scope.ansible_log += '\nstart read\n';
        }).error(function(err){
            console.log(err)
        });
    };

    function read_log(data){
        $http.post('/demo_2/demo2_api/read_long_ansible/', data)
        .success(function(result){
            console.log(result);
            data = result;
            $scope.ansible_log += result['logs'];            // add logs to model(ansible_log)
            if($scope.state == 'REVOKED'){
                 $scope.ansible_log += '\nend read\n';
            	$scope.read_flag = false;
                 return;
            }
            $scope.state = data['state'];
            $scope.read_flag = data['read_flag']     
            if($scope.read_flag == false){
                document.getElementById("textscroll").scrollTop=document.getElementById("textscroll").scrollHeight;
                $scope.ansible_log += '\nend read\n';
                alert('task ' + result['task_id'] + ' is over')
            }else{
                if($scope.read_flag == false){
                    alert('task ' + result['task_id'] + ' is over')
                    document.getElementById("textscroll").scrollTop=document.getElementById("textscroll").scrollHeight;
                    $scope.ansible_log += '\nend read\n';
                }else{
                    setTimeout(function() { read_log(data)}, 5000);  // wait every 5 second to read log
                    if(document.getElementById("textscroll").scrollTop + 1000>=document.getElementById("textscroll").scrollHeight || document.getElementById("textscroll").scrollTop == 0){
                        setTimeout(function(){
                            document.getElementById("textscroll").scrollTop=document.getElementById("textscroll").scrollHeight;
                        },100);
                    }
                }
            }
        }).error(function(err){
            console.log('err')
        });
    }

    $scope.revoke_task = function(task_id){
        data = {'task_id': task_id}
        $http.post('/demo_2/demo2_api/long_ansible_revoke/', data)
        .success(function(result){
            alert('任务已经停止')
            $scope.task_id = '';
            $scope.state = 'REVOKED';
        }).error(function(err){
            console.log('err')
        });
    };

});
