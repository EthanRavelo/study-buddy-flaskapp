window.onload = function () {

    setInterval(function () {
        localStorage.currency += 1;
    }, 60 * 1000); // 60 * 1000 milsec

    function fn60sec() {
        // runs every 60 sec and runs on init.
    }
    fn60sec();
    setInterval(fn60sec, 60 * 1000);

}

window.BeforeUnloadEvent = function(){
    window.clearInterval(int);

}