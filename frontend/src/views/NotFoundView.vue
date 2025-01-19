<template>
    <div class="py-8 px-4 mx-auto max-w-screen-xl lg:py-16 lg:px-6">
        <div class="mx-auto max-w-screen-sm text-center">
            <h1 class="mb-4 text-7xl tracking-tight font-extrabold lg:text-9xl text-primary-600 dark:text-primary-500">404</h1>
            <p class="mb-4 text-3xl tracking-tight font-bold text-gray-900 md:text-4xl">Something's missing.</p>
            <p class="mb-4 text-lg font-light">Sorry, we can't find that page. You'll find lots to explore on the home page. </p>
            <p @click="this.$router.push('/')" class="inline-flex text-white bg-[#0d9488] focus:ring-4  font-medium rounded text-sm px-5 py-2.5 text-center my-4">Back to Homepage</p>
        </div>   
    </div>
</template>

<script>

</script>