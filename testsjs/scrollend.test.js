describe('scrollend', function(){
    beforeEach(function(){
        this.element = new Element('div', {
            styles: {
                width: 400,
                height: 400,
                overflow: 'scroll'
            }
        });
        this.inner = new Element('div', {
            styles: {
                width: 300,
                height: 800
            }
        });
        $$('body').grab(this.element.grab(this.inner));
        this.scrollend = new ScrollEnd(this.element, {offset: 200});
        this.callback = jasmine.createSpy();
        this.scrollend.addEvent('end', this.callback);
    });
    afterEach(function(){
        this.element.destroy();
    });

    it('should not fire the end event if the offset has not been reached', function(){
        this.element.scrollTo(0, 100);
        // dunno why need the delay, but i know we need it!
        waits(50);
        runs(function(){
            expect(this.callback).not.toHaveBeenCalled();
        });
    });

    it('should fire the end event if the offset has been reached', function(){
        this.element.scrollTo(0, 300);
        waits(50);
        runs(function(){
            expect(this.callback).toHaveBeenCalled();
        });
    });

});
