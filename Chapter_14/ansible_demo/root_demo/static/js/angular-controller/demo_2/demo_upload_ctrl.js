app.controller('demo_upload_ctrl', function($scope, $http, Upload){
    function goupload(url) {
        console.log($scope.upload_file)
        if(!$scope.upload_file) {
            return;
        }else{
            if(!$scope.filename){
                alert('文件未命名，请先输入要创建的文件名')
                return;
            }else{
                Upload.upload({
                    url: url,
                    data: {file: $scope.upload_file, 'para': JSON.stringify($scope.para)},
                }).then(function (resp) {
                    console.log(resp)
                    $scope.flag = resp['data']['flag'];
                    if (resp['data']['flag']) {
                        $scope.msg = resp.config.data.file.name + '上传成功!';
                    } else {
                        $scope.msg = '上传出错: ' + resp['data']['output'];
                    }
                    $scope.filename = '';
                }, function (resp) {
                    console.log('Error status: ' + resp.status);
                }, function (evt) {
                    var progressPercentage = parseInt(100.0 * evt.loaded / evt.total);
                    $scope.proc_log = '上传进度: ' + progressPercentage + '% ' + evt.config.data.file.name;
                });
            }
        }
    };

    $scope.filename = '';
    $scope.$watchCollection('upload_file', function () {
        $scope.para = {'saved_file_name': $scope.filename}
        goupload('/demo_2/demo2_api/file_upload/');
    },true);
});
