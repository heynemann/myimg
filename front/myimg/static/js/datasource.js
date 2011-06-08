(function(global){

    var DataSource = global.DataSource = new Class({
        Implements: Promise,

        register: function(source, shouldUpdate){
            this.source = source;
            if (shouldUpdate == null || shouldUpdate === true) this.update();
        },

        update: function(){
            this.source.call(this, this.call.bind(this, 'success'), this.call.bind(this, 'fail'));
        },

        subscribe: Promise.prototype.success
    });

})(this);

