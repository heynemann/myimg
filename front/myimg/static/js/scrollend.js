(function(global, $){

    var ScrollEnd = global.ScrollEnd = new Class({
        Implements: [Options, Events],

        options: {
            offset: 200
        },

        initialize: function(element, options){
            this.setOptions(options);
            this.element = $(element || global);
            this.bound = {
                scroll: this.watchScroll.bind(this)
            };
            this.enable();
        },

        enable: function(){
            this.element.addEvent('scroll', this.bound.scroll);
        },

        disable: function(){
            this.element.removeEvent('scroll', this.bound.scroll);
        },

        watchScroll: function(){
            if (this.isEnd()) this.fireEvent('end');
        },

        isEnd: function(){
            var scrollHeight = this.element.getScrollSize().y;
            var height = this.element.getSize().y;
            var scroll = this.element.getScroll().y;
            return (scrollHeight - height - this.options.offset <= scroll);
        }
    });

})(this, document.id);
