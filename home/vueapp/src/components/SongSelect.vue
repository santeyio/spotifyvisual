<template>
  <div>
    <select v-model="selected" size=10 multiple>
      <option v-for="song in songs" :value="song">
        {{ song.name }} -- {{ song.artist }}
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
      songs: [{name: 'Please Select a Playlist'}],
      selected: [],
    }
  },
  watch: {
    selected: function(val) {
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
          self.songs = response.data;
        });
    });
  }
}
</script>

<style scoped>
</style>
