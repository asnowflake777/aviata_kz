<template>
  <div id="header">
    <p>Популярные направления</p>
    <select v-model="selectedDirection" @change="changeDirection">
      <option v-for="(direction, index) in $props.directions" :key="index" v-bind:value="direction">
        {{ direction.name }}
      </option>
    </select>
  </div>
</template>

<script>

export default {
  name: "Header",
  props: [
    'directions'
  ],
  data() {
    return {
      selectedDirection: [],
    }
  },
  methods: {
    changeDirection: function () {
      this.$emit('set-direction', this.$data.selectedDirection)
    }
  },
}
</script>

<style scoped>

</style>