(function(global, $){

    var DataSource = global.DataSource = new Class({
        Implements: [Options, Events],

        initialize: function(element, options){
            this.setOptions(options);
            this.sources = {};
        },

        register: function(id, source){
            this.sources[id] = source;
        },

        update: function(id){
            this.sources[id].call(this, this._notifier.bind(this, id));
        },

        _notifier: function(id, data){
            this.fireEvent(id, [data]);
        }
    });

})(this, document.id);


