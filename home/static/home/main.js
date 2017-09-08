var bus = new Vue();

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
        spotify_user = response.data.id;
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
      //console.log('val: ', val);
      rdata = {};
      ({
        owner: {
          id: rdata.owner_id
        },
        id: rdata.playlist_id,
      } = val[0]);
      bus.$emit('playlist-update', rdata);
    }
  },
  mounted: function() {
    var self = this;
    var offset = 0;
    var total = 50;
    var playlist_temp = [];
    axios({
      url: '/api/v1/playlists?',
      params: {
        offset: offset,
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
        offset += 50;
        if (offset < total){
          return axios({
            url: '/api/v1/playlists',
            params: { offset: offset }
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

Vue.component('songs-select', {
  template: '#songs-select-template',
  data: function(){
    return {
      songs: [],
      selected: [],
    }
  },
  watch: {
    selected: function(val) {
      console.log(val)
      console.log(val[0].artist)
      console.log(val[0].name)
      bus.$emit('song-update', val[0]);
    }
  },
  created: function(){
    var self = this;
    bus.$on('playlist-update', function(updates){
      axios({
        url: '/api/v1/playlists/' + updates.playlist_id,
        params: {
          owner_id: updates.owner_id,
        },
      })
        .then(function(response){
          console.log('response: ', response.data);
          self.songs = response.data;
        });
    });
  }
});

Vue.component('bubble-chart', {
  template: '#bubble-chart-template',
  data: function(){
    return {
      loading: false,
      nolyrics: false,
    }
  },
  created: function(){
    var self = this;
    bus.$on('song-update', function(updates){
      if (updates.name){
        //var ajax = axios.create({
        axios.interceptors.request.use(function(config){
          self.nolyrics = false;
          self.loading = true;
          console.log('well....');
          return config;
        }, function(error){
          return Promise.reject(error);
        });
        axios({
          url: '/api/v1/song',
          params: {
            artist: updates.artist,
            name: updates.name,
          },
        })
          .then(function(response){
            if (response.data.error){
              self.loading = false;
              self.nolyrics = true;
              create_bubble_chart([], true);
            } else {
              console.log(response);
              self.loading = false;
              var data = response.data;
              var mdata = [];
              for (var prop in data){
                if (data.hasOwnProperty(prop)){
                  mdata.push({word: prop, count: data[prop]});
                }
              }
              //console.log('mdata: ', mdata);
              create_bubble_chart(mdata);
            }
          });
      }
    })
  },
});

var vm = new Vue({
  el: '#vue-root',
})


function create_bubble_chart(data, clear_only=false){

  var svg = d3.select("svg"),
      width = +svg.attr("width"),
      height = +svg.attr("height");

  svg.selectAll('*').remove();

  if (!clear_only){
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
      .style("fill", function(d) { return color(d.count); });

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
}
