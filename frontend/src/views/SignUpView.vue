<template> 
    <div class="flex flex-col items-center justify-center px-6 py-8 mx-auto md:h-screen lg:py-0 bg-gray-50">
        <div class="mb-4 flex justify-between space-x-2 items-center">
            <img src="" alt="Logo">
            <span class="block text-xl font-bold">TrainMe</span>
        </div>
        <div class="w-[480px] bg-white flex flex-col p-10 rounded space-y-3 shadow-xl">
            <h1 class="text-xl font-bold">Create an account </h1>
            <div class="flex flex-col space-y-1">
                <label for="login">Email</label>
            <input v-model="this.login" class="px-4 py-2 rounded border" id="login" type="text" placeholder="pattern@mail.com">
            </div>
            <div class="flex flex-col space-y-1">
                <label for="login">Password</label>
                <input v-model="this.password" class="px-4 py-2 rounded border" id="login" type="password" placeholder="!@#$%^&*()">
            </div>
            <p></p>
            <button class="bg-[#0d9488] transition delay hover:bg-[#0f766e] px-4 py-2 rounded text-white">Sign up</button>
            <p>Already have account? <span @click="this.$router.push('/sign_in')" class="cursor-pointer text-[#0d9488] transition delay hover:text-[#0f766e]">Sign in</span></p>
        </div>
        {{ this.login }}
    </div>
</template>

<script>
    export default {
        name: "SignUpView",
        data() {
            return {
                login: "",
                password: "",
            }
        },
        methods: {

        }
    }
</script>