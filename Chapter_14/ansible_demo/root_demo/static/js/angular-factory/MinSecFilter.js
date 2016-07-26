app.filter('MinSecFilter', function () {
    return function (value, max) {      
        if (value == max) return 'All';
            var m = parseInt(value / 60);
            var s = parseInt(value % 60);
            var mStr = (m > 0) ? m >= 10 ? m  : '0' + m : '00';
            var sStr = (s > 0) ? s >= 10 ? s  : '0' + s : '00';
            var glue = (mStr && sStr) ? ':' : '';
        return mStr + glue + sStr;    
            };
}); 
