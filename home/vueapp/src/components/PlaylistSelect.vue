<template>
	<div>
		<select v-model="selected" size=10 multiple>
			<option  v-for="playlist in playlists" :value="playlist">
				{{ playlist.name }}
			</option>
		</select>
	</div>
</template>

<script>
import axios from 'axios';
import bus from '../bus';

export default {
  data: function(){
    return {
      playlists: [], 
      selected: [], 
      test: false,
    }   
  },
  watch: {
    selected: function(val) {
      if (val != []){
        var rdata = {}; 
        ({
          owner: {
            id: rdata.owner_id
          },  
          id: rdata.playlist_id,
        } = val[0]);
        bus.$emit('playlist-update', rdata);
      }
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
}
</script>

<style scoped>
</style>
