import { createRouter, createWebHistory } from "vue-router";

import HomeView from "@/views/HomeView.vue";
import HowUseView from "@/views/HowUseView.vue"
import CreateMLView from "@/views/CreateMLView.vue"
import UserModelsInfoView from "@/views/UserModelsInfoView.vue"


const routes = [
    {
        path: "/",
        component: HomeView
    },
    {
        path: "/how_use",
        component: HowUseView,
    },
    {
        path: "/create",
        component: CreateMLView,
    },
    {
        path: "/my_models",
        component: UserModelsInfoView
    }
]

const router =  createRouter({
    history: createWebHistory(),
    routes
})

export default router;