<template>
  <div class="flex">
    <!-- Sidebar -->
    <aside class="h-screen border-r px-4 mr-4">
      <!-- Logo -->
      <RouterLink class="container py-2 flex items-center space-x-2 border-b border-black mb-2" to="/">
        <img src="" alt="Logo">
        <h1 class="font-bold text-xl">TrainMe</h1>
      </RouterLink>
      <!-- Navigation -->
      <nav class="flex flex-col space-y-2">
        <!-- Create algo -->
        <RouterLink 
        class="flex items-center px-4 text-medium transition py-2 delay-100 rounded hover:bg-gray-100" 
        to="/create">
          <img src="./assets/icons/add.png" height="20px" width="20px" alt="">
          <span class="ml-2">Create algorithm</span>
        </RouterLink>
        <!-- User models -->
        <RouterLink 
        class="flex items-center px-4 text-medium transition py-2 delay-100 rounded hover:bg-gray-100" 
        to="/my_models">
        <img src="./assets/icons/ai.png" height="20px" width="20px" alt="">
          <span class="ml-2">Models</span>
        </RouterLink>
        <!-- About -->
        <RouterLink 
        class="flex items-center px-4 text-medium transition py-2 delay-100 rounded hover:bg-gray-100" 
        to="/how_use">
        <img src="./assets/icons/info.png" height="20px" width="20px" alt="">
          <span class="ml-2">How use</span>
        </RouterLink>        
      </nav>
    </aside>
    <!-- Main -->
    <main>
      <RouterView/>
    </main>
  </div>
</template>

<script>
export default {
  name: 'App',

}
</script>

<style>

</style>
