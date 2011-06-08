(function(global){

    var DataSource = global.DataSource = new Class({
        Implements: Promise,

        register: function(source, shouldUpdate){
            this.source = source;
            if (shouldUpdate == null || shouldUpdate === true) this.update();
        },
        registerJson: function(url, shouldUpdate){
            this.request = new Request.JSON({url: url, method: 'get'});
            this.register(function(success, failure){
                this.request
                    .addEvent('success', success)
                    .addEvent('failure', failure);
                this.request.send();
            }.bind(this), shouldUpdate);
        },
        update: function(){
            this.source.call(this, this.call.bind(this, 'success'), this.call.bind(this, 'fail'));
        },
        subscribe: Promise.prototype.success
    });

})(this);

