<template>
	<div class="col-md-12">
		<div v-show="loading" class="text-center" style="margin-top:200px;">
			<h3>Please be patient, this can take at least a few minutes.</h3>
			<img src="/site_media/home/ajax-loader.gif"/>
		</div>
		<div v-show="nolyrics" class="text-center" style="margin-top:200px;">
			<h3>Whoops, couldn't find any lyrics for that song.</h3>
		</div>
		<div v-show="!loading">
			<svg width="960" height="960" font-family="sans-serif" font-size="10" text-anchor="middle"></svg>
		</div>
	</div>

</template>

<script>
import axios from 'axios';
import bus from '../bus';
import create_bubble_chart from '../helpers/create_bubble_chart';

export default {
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
        axios.interceptors.request.use(function(config){
          self.nolyrics = false;
          self.loading = true;
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
              self.loading = false;
              var data = response.data;
              var mdata = [];
              for (var prop in data){
                if (data.hasOwnProperty(prop)){
                  mdata.push({word: prop, count: data[prop]});
                }
              }
              create_bubble_chart(mdata);
            }
          });
      }
    })
  },
}
</script>

<style scoped>
</style>
