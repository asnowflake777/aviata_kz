<template>
  <div class="day" @click="checkFlight">
    <span class="price"> {{ dayInfo.price }} </span>
    <span class="currency"> {{ dayInfo.currency }} </span>
  </div>
</template>

<script>
export default {
  name: "Day",
  props: [
    'dayInfo'
  ],
  methods: {
    checkFlight() {
      console.log(this.$props.dayInfo.booking_token)
    }
  }
}
</script>

<style scoped>
.day {
  display: inline-block;
  height: 30px;
  width: 30px;
}
.price{
  font-size: 10px;
}
.currency{
  font-size: 8px;
}
</style>