var Councilmatic = Councilmatic || {};

(function($) {
  var CM = Councilmatic;

  CM.TopUIView = Backbone.View.extend({
    el: 'body > .container',

    initialize: function() {
      this.navbarView = new CM.MainNavbarView({model: this.options.subscriber});
      this.navbarTemplate = Mustache.template('main-navbar').render;
    },

    render: function() {
      this.navbarView.render();
    }
  });

  CM.MainNavbarView = Backbone.View.extend({
    el: '.navbar .container',

    initialize: function() {
      this.template = Mustache.template('main-navbar').render;
      this.model.bind('change', this.render, this);
      this.render();
    },

    render: function() {
      var html = this.template(this.model.toJSON());
      this.$el.html(html);
      return this.$el;
    }
  })

  /*
   * ProfileView is a top-level view, with a navbar and all.
   */
  CM.ProfileView = CM.TopUIView.extend({
    initialize: function() {
      CM.TopUIView.prototype.initialize.call(this);
      this.subscriber = this.model = this.options.subscriber;
      this.template = Mustache.template('profile-admin');
    },

    render: function() {
      this.$el.html(this.template.render(this.subscriber.toJSON()));
      CM.TopUIView.prototype.render.call(this);
      return this.$el;
    }
  });

  CM.SubscriptionView = Backbone.View.extend({
    initialize: function() {
      var self = this;
      
      this.template = Mustache.template('')
    },

    render: function() {

    }
  });

})(jQuery);
