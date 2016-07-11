var app = angular.module('myApp', ['ngFileUpload', 'angularUtils.directives.dirPagination']);
app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('((');
    $interpolateProvider.endSymbol('))');
});
app.run(function($http) {
    //$http.defaults.headers.post['X-CSRFToken'] = $.cookie('csrftoken');
    // Add the following two lines
    $http.defaults.xsrfCookieName = 'csrftoken';
    $http.defaults.xsrfHeaderName = 'X-CSRFToken';
});


