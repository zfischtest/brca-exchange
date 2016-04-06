var backend = require('./backend');
var $ = require('jquery');

module.exports = {
    login: function (username, pass, cb) {
        if (localStorage.token) {
            if (cb) cb(true);
            return
        }
        this.getToken(username, pass, (res) => {
            if (res.authenticated) {
                localStorage.token = res.token;
                if (cb) cb(true)
            } else {
                if (cb) cb(false)
            }
        })
    },

    logout: function () {
        delete localStorage.token;
    },

    loggedIn: function () {
        return !!localStorage.token
    },

    getToken: function (username, password, cb) {
        var url = backend.databaseUrl + '/accounts/token-auth/';
        $.ajax({
            url: url,
            data: {
                username: username,
                password: password
            },
            dataType: 'json',
            crossDomain: true,
            method: 'POST',
            success: function (res) {
                cb({
                    authenticated: true,
                    token: res.token
                })
            }
        });
    }
};