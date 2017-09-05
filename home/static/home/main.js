
Vue.component('user-profile', {
  template: '#user-profile-template',
  data: function(){
    return {
      display_name: false,
      uid: false,
      image: false,
      external_url: false,
      email: false,
      country: false,
      link: false
    }
  },
  mounted: function() {
    self = this;
    axios({
      url: 'https://api.spotify.com/v1/me',
      headers: {'Authorization': 'Bearer ' + access_token},
    })
      .then(function(response) {
        ({
          display_name: self.display_name,
          country: self.country,
          id: self.uid,
          images: [ self.image ],
          external_urls: {
            spotify: self.external_url
          },
          email: self.email,
          country: self.country,
          href: self.link,
        } = response.data);
    });
  }
});

Vue.component('playlists-select', {
  template: '#playlists-select-template',
  data: function(){
    return {
      playlists: [],
      selected: [],
    }
  },
  watch: {
    selected: function(val) {
      console.log('watch triggered', val);
      bus.$emit('select-update', val);
    }
  },
  mounted: function() {
    var self = this;
    var offset = 0;
    var total = 50;
    var playlist_temp = [];
    axios({
      url: '/api/v1/playlists?offset=' + offset,
    })
      .then(function(response) {
        ({
          items: [
            ...playlist_temp
          ],
          total: total,
        } = response.data);
        self.playlists = self.playlists.concat(playlist_temp);
        offset += 50;
        if (offset < total){
          return axios({
            url: '/api/v1/playlists?offset=' + offset,
          });
        }
      })
      .then(function(response) {
        ({
          items: [
            ...playlist_temp
          ],
          total: total,
        } = response.data);
        self.playlists = self.playlists.concat(playlist_temp);
      });
  }
});

Vue.component('bubble-chart', {
  template: '#bubble-chart-template',
  data: function(){
    return {
      selected: [],
      loading: false,
    }
  },
  created: function(){
    bus.$on('select-update', function(updates){
      this.selected = updates;
      //console.log(this.selected);

      var test_data = [
          {word: 'test', count: 10}, 
          {word: 'copy', count: 10}, 
          {word: 'glow', count: 10}, 
          {word: 'love', count: 10}, 
          {word: 'horns', count: 100}, 
          {word: 'temperamental', count: 50}, 
          {word: 'glib', count: 15}, 
          {word: 'soccer', count: 30}, 
          {word: 'pastime', count: 40}, 
      ];

      create_bubble_chart(test_data);
    })
  },
});

var vm = new Vue({
  el: '#vue-root',
})

var bus = new Vue();

function create_bubble_chart(data){

  //console.log('ran function');
  var svg = d3.select("svg"),
      width = +svg.attr("width"),
      height = +svg.attr("height");

  var format = d3.format(",d");

  var color = d3.scaleOrdinal(d3.schemeCategory20c);

  var pack = d3.pack()
      .size([width, height])
      .padding(1.5);

  var root = d3.hierarchy({children: data})
      .sum(function(d) { return d.count; })
      .each(function(d) {
        if (id = d.data.word) {
          var id, i = id.lastIndexOf(".");
          d.id = id;
          d.package = id.slice(0, i);
          d.class = id.slice(i + 1);
          d.count = d.data.count;
        }
      });

  var node = svg.selectAll(".node")
    .data(pack(root).leaves())
    .enter().append("g")
    .attr("class", "node")
    .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });

  node.append("circle")
    .attr("id", function(d) { return d.id; })
    .attr("r", function(d) { return d.r; })
    .style("fill", function(d) { return color(d.word); });

  node.append("clipPath")
    .attr("id", function(d) { return "clip-" + d.id; })
    .append("use")
    .attr("xlink:href", function(d) { return "#" + d.id; });

  node.append("text")
    .attr("clip-path", function(d) { return "url(#clip-" + d.id + ")"; })
    .selectAll("tspan")
    .data(function(d) { return d.class.split(/(?=[A-Z][^A-Z])/g); })
    .enter().append("tspan")
    .attr("x", 0)
    .attr("y", function(d, i, nodes) { return 13 + (i - nodes.length / 2 - 0.5) * 10; })
    .text(function(d) { return d; });

  node.append("title")
    .text(function(d) { return d.id + "\n" + format(d.count); });
}
