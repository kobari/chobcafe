<template>

  <div class="container">
    <div class="row" v-for="item in cafe_list" v-bind:key="item.place_id">
        <b-card
            v-bind:title="item.name"
            v-bind:img-src="'/images/' + item.name + '.png'"
            v-bind:img-alt="item.name"
            img-top
            tag="article"
            class="mb-2"
        >
          <b-card-text>
            {{item.formatted_address}}
          </b-card-text>
          <b-link target="_blank" v-bind:href="item.place_details.website" class="card-link">website</b-link>
          <b-link target="_blank" v-bind:href="item.place_details.url" class="card-link">map</b-link>

        </b-card>
    </div>
  </div>
</template>

<script>
import Axios from "axios";

export default {
  name: 'CafeList',
  props: {
    msg: String,
    cafe_list: Array
  },
  data(){
    return {
      test:0
    }
  },
  beforeCreate() {
    console.log(this)
    console.log(this.vue)
    let self = this
    //console.log(Vue)
    Axios.get('http://localhost:8000/places/list/', {
      headers:{
       // 'Access-Control-Allow-Origin' : '*',
      }
    }).then(function (response){
      console.log(response.data)
      self.cafe_list = response.data.results
      console.log(self.cafe_list)
    })
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
