/**
 * Represents a data for a single hashtag
 */
var HashtagData = Backbone.Model.extend({
	
	defaults: function() {
		return {
			hashtag: null,
			total: null,
			tweets: []
		}
	},
	
	initialize: function(options) {
		if (!options.hashtag) {
			throw "Missing hashtag parameter!"
		}
		
		this.set('hashtag', options.hashtag);
	},
	
	url: function() {
		return "http://kafka-sentiments.local:9200/processed_tweets/_search?q=%23" + this.get('hashtag') + '&size=100';
	},
	
	parse: function(data) {
		var tweets = [];

		_.each(data.hits.hits, function(hit) {
			tweets.push(hit._source);
		});
		
		return {
			total: data.hits.total.value,
			tweets: tweets
		};
	}
});

/**
 * Renders Hashtag Data as a Pie Chart
 */ 
var PieView = Backbone.View.extend({

	initialize: function(options) {
		if (!options.model || !options.model instanceof HashtagData) {
			throw "Invalid model provided!";
		};
		
		Backbone.View.prototype.initialize.apply(this, arguments);
	},

	render: function() {
		// this.$el.addClass('pie-view');
		
		var tpl = _.template($('#pieview-tpl').html());

		// this.$el.html('<h4>Hashtag: #'+this.model.get('hashtag')+'</h4><canvas id="myChart-' + this.cid + '"></canvas>');
		
		var html = tpl({
			cid: this.cid,
			hashtag: this.model.get('hashtag'),
			tweets: this.model.get('tweets')
		});
		
		this.$el.html(html);
		
		
		var positive = negative = neutral = 0;
		
		_.each(this.model.get('tweets'), function(tweet) {
			if (tweet.afinn_score < 0) {
				negative++;
			} else if (tweet.afinn_score == 0.0) {
				neutral++;
			} else {
				positive++;
			}
		});
		
		var config = {
			type: 'pie',
			data: {
				datasets: [{
					data: [
						positive,
						neutral,
						negative
					],
					backgroundColor: [
						window.chartColors.green,
						window.chartColors.orange,
						window.chartColors.red
					],
					label: 'Semantics'
				}],
				labels: [
					'Positive',
					'Neutral',
					'Negative',
				]
			},
			options: {
				responsive: true
			}
		};
		
		var ctx = this.$el.find('canvas')[0].getContext('2d');
		new Chart(ctx, config);
		return this;
	}
});