<template>
  <div class="calendar">
<!--    <p v-for="(flight, index) in flightsInfo" :key="index">{{ flight.price }}</p>-->
    <Day v-for="(flight, index) in flightsInfo" :key="index" v-bind:day-info="flight" class="day" />
  </div>
</template>

<script>
import Day from "@/components/Day";

export default {
name: "Calendar",
  components: {
    Day
  },
  props: [
      'flightsInfo'
  ]
}
</script>

<style scoped>

</style>