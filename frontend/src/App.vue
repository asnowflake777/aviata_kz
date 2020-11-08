<template>
  <div id="app">
    <div>
      <Header v-on:set-direction="setDirection" v-bind:directions="$data.availableDirections"/>
    </div>
    <div v-if="flightsInfo">
      <Calendar v-bind:flights-info="flightsInfo" />
    </div>
  </div>
</template>

<script>
import axios from "axios";

import Header from "@/components/Header";
import Calendar from "@/components/Calendar";

export default {
  name: 'App',
  components: {
    Header,
    Calendar
  },
  data() {
    return {
      availableDirections: undefined,
      selectedDirection: undefined,
      flightsInfo: undefined,
    }
  },
  methods: {
    setDirection(direction) {
      axios.get('http://localhost:5000/mount_prices_for_direction',
          {
            params: {
              flyFrom: direction.flyFrom,
              to: direction.to,
            }
      }).then(response => {
        this.$data.flightsInfo = response.data
        console.log(this.$data.flightsInfo)
      })
    }
  },
  mounted() {
    axios.get('http://localhost:5000/available_directions')
        .then(response => {
          console.log(response.data)
          this.$data.availableDirections = response.data
          console.log(this.$data.availableDirections)
        })
        .catch(e => console.log(e))
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 0;
}
#header{
  height: 150px;
  width: 100%;
  background-color: #fdc23a;
}
.calendar{
  display: inline-block;
  height: 300px;
  width: 50%;
  background-color: #00afc6;
}
</style>
