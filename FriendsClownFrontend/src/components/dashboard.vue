<template>
  <div class="hello">
    <h1>Welcome!</h1>
    <p>
      The function is being finalized, please come back later.
    </p>
  </div>
</template>

<script>
export default {
  name: 'dashboard',
  props: {
    msg: String
  },
  mounted() {
    this.$parent.checkAuthenticaion();
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
