(function(global){

    var slice = Array.prototype.slice;

    var Promise = global.Promise = new Class({
        Implements: Events,
        call: function(name){
            var args = slice.call(arguments, 1);
            if (this.promiseState){
                this.removeEvents(this.promiseState.name);
            }
            this.promiseState = {
                name: name,
                args: args
            };
            this.fireEvent(name, args);
        },
        then: function(success, fail){
            this.success(success).fail(fail);
        },
        success: function(callback){
            this.add('success', callback);
        },
        fail: function(callback){
            this.add('fail', callback);
        },
        add: function(name, callback){
            if (this.promiseState && this.promiseState.name == name){
                callback.apply(this, this.promiseState.args);
            } else {
                this.addEvent(name, callback);
            }
        }
    });

})(this);
