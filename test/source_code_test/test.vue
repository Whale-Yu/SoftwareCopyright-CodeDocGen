<template>
  <div class="test">
    <h1>Hello, World!</h1>
    <p>{{ message }}</p>
  </div>
</template>

<script>
export default {
  name: 'Test',
  data() {
    return {
      message: 'Welcome to Vue!'
    }
  }
}
</script>

<style scoped>
.test {
  padding: 20px;
}
</style>