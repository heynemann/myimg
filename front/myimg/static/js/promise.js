(function(global){

    var slice = Array.prototype.slice;

    var Promise = global.Promise = new Class({
        Implements: Events,
        call: function(name){
            var args = slice.call(arguments, 1);
            this.promiseState = {
                name: name,
                args: args
            };
            this.fireEvent(name, args);
        },
        then: function(success, failure){
            this.success(success).failure(failure);
        },
        success: function(callback){
            this.add('success', callback);
        },
        failure: function(callback){
            this.add('failure', callback);
        },
        isResolved: function(){
            return !!this.promiseState;
        },
        add: function(name, callback){
            if (!this.promiseState){
                this.addEvent(name, callback);
            } else if (this.promiseState.name == name){
                callback.apply(this, this.promiseState.args);
            }
        }
    });

})(this);
