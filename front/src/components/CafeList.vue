<template>

  <div class="container">
    <transition-group tag="div" name="fade">
      <div class="row" v-for="(item,index) in cafe_list" v-bind:key="item.place_id">

          <b-card
              v-bind:title="item.name"
              v-bind:img-src="'/images/' + item.place_id + '/' + item.name + '.png'"
              v-bind:img-alt="item.name"
              img-top
              tag="article"
              class="mb-2"
              v-on:click="detail(index)"
          >
            <b-card-text>
              {{item.formatted_address}}
            </b-card-text>
            <b-link target="_blank" v-bind:href="item.place_details.website" class="card-link">website</b-link>
            <b-link target="_blank" v-bind:href="item.place_details.url" class="card-link">map</b-link>

          </b-card>
        <LightBox ref="lightbox" :media="item.place_details.photos" :show-light-box="false" :show-caption="true" />
      </div>
    </transition-group>
    <transition name="load-more" :duration="5000">
      <div><b-button v-if="next" variant="outline-primary" v-on:click="loadMoreCafeList">Load more</b-button></div>
    </transition>

  </div>
</template>

<script>
import Vue from 'vue'
import Axios from "axios";
import LightBox from 'vue-image-lightbox'
import VueLazyLoad from 'vue-lazyload'

Vue.use(VueLazyLoad)

export default {
  name: 'CafeList',
  props: {
    msg: String,
    //cafe_list: Array
  },
  components: {
    LightBox,
  },
  data(){
    return {
      disable: true,
      cafe_list: null,
      page: 1,
      next: null,
    }
  },
  beforeCreate() {
    let self = this
    Axios.get('http://localhost/api/places/list/', {
      params:{
       page: 1
      }
    }).then(function (response){
      self.cafe_list = response.data.results
      self.next = response.data.next
    })
  },
  methods:{
    detail: function (index){
      this.$refs.lightbox[index].showImage(0)
    },
    loadMoreCafeList : function (){
      let self = this
      Axios.get(self.next, {
      }).then(function (response){
        self.cafe_list.push(...response.data.results)
        self.next = response.data.next
      })
    }
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
.fade-enter-active, .fade-leave-active {
  transition: opacity .5s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
.load-more-leave-to {
  transition: opacity 5s;
}
</style>
