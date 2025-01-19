import { createRouter, createWebHistory } from "vue-router";

import HomeView from "@/views/HomeView.vue";
import HowUseView from "@/views/HowUseView.vue"
import CreateMLView from "@/views/CreateMLView.vue"
import UserModelsInfoView from "@/views/UserModelsInfoView.vue"
import SignUpView from "@/views/SignUpView.vue"
import SignInView from "@/views/SignInView.vue";
import NotFoundView from "@/views/NotFoundView.vue"


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
    },
    {
        path: "/sign_up",
        component: SignUpView,
        meta: {
            hideNavbar: true,
           }
    },
    {
        path: "/sign_in",
        component: SignInView,
        meta: {
            hideNavbar: true,
           }
    },
    {
        // path: "*",
        path: "/:catchAll(.*)",
        name: "NotFoundView",
        component: NotFoundView,
        meta: {
            hideNavbar: true,
           }
    }
]

const router =  createRouter({
    history: createWebHistory(),
    routes
})

export default router;