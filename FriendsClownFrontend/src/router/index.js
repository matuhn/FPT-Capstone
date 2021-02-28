import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
    {
        path: '/signup',
        name: 'signup',
        component: () => import('../components/signup.vue')
    },
    {
        path: '/login',
        name: 'login',
        component: () => import('../components/login.vue')
    },
    {
        path: '/forgot-password',
        name: 'forgot-password',
        component: () => import('../components/forgotPassword.vue')
    },
    {
        path: "/dashboard",
        name: "dashboard",
        component: () => import('../components/dashboard.vue')
    },
    {
        path: "/profile",
        name: "profile",
        component: () => import('../components/profile')
    },
    {
        path: "/files",
        name: "files",
        component: () => import('../components/files')
    },
    {
        path: "/notfound",
        name: "notfound",
        component: () => import('../components/notFound')
    }
]

const router  = new VueRouter(
    {
        mode: "history",
        base: process.env.BASE_URL,
        routes
    }
)

export default router