<template>	
  <div>
		<h1>Logged in as {{display_name}}</h1>
		<div class="media">
			<div class="pull-left">
				<img class="media-object" width="150" :src="image" />
			</div>
			<div class="media-body">
				<dl class="dl-horizontal">
					<dt>Display name</dt><dd class="clearfix">{{display_name}}</dd>
					<dt>Id</dt><dd>{{uid}}</dd>
					<dt>Email</dt><dd>{{email}}</dd>
					<dt>Spotify URI</dt><dd><a :href="external_url">{{external_url}}</a></dd>
					<dt>Link</dt><dd><a :href="link">{{link}}</a></dd>
					<dt>Profile Image</dt><dd class="clearfix"><a :href="image">{{image}}</a></dd>
					<dt>Country</dt><dd>{{country}}</dd>
				</dl>
			</div>
		</div>
	</div>
</template>

<script>
import axios from 'axios';

export default {
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
    var self = this;
    var access_token = this.$cookie.get('access_token');
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
}
</script>

<style scoped>
</style>
