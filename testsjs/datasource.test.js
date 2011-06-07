describe('datasource', function(){
    beforeEach(function(){
        this.callback = jasmine.createSpy();
        this.datasource = new DataSource();
    });

    it('should fire the "id" event while registering', function(){
        this.datasource.subscribe(this.callback);
        this.datasource.register(function(notifier){
            notifier([1,2,3]);
        });

        expect(this.callback).toHaveBeenCalledWith([1,2,3]);
    });

    it('should not fire the "id" event if the shouldUpdate attribute is set to false', function(){
        this.datasource.subscribe(this.callback);
        this.datasource.register(function(notifier){
            notifier([1,2,3]);
        }, false);

        expect(this.callback).not.toHaveBeenCalled();
    });

    it('should fire the "id" event when data arrives', function(){
        this.datasource.register(function(notifier){
            notifier([1]);
        });
        this.datasource.subscribe(this.callback);
        expect(this.callback).toHaveBeenCalledWith([1]);
    });
});
