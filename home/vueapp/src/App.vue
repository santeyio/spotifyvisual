<template>
  <div class="container">
    <div id="loggedin" class="row">
      <div id="user-profile" class="col-md-5">
        <user-profile></user-profile>
      </div>
      <div id="playlists-root" class="col-md-3">
        <h1>Playlists</h1>
        <playlist-select></playlist-select>
      </div>
      <div id="songs-root" class="col-md-4">
        <h1>Songs</h1>
        <song-select></song-select>
      </div>
    </div>
    <div class="row">
      <bubble-chart></bubble-chart>
    </div>
  </div>
</template>

<script>
import UserProfile from './components/UserProfile.vue';
import PlaylistSelect from './components/PlaylistSelect.vue';
import BubbleChart from './components/BubbleChart.vue';
import SongSelect from './components/SongSelect.vue';

export default {
  name: 'app',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App'
    }
  },
  components: {
    UserProfile,
    PlaylistSelect,
    BubbleChart,
    SongSelect,
  }
}
</script>

<style>
</style>
