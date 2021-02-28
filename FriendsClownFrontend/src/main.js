import Vue from 'vue'
import App from './App.vue'
import router from './router'


import JQuery from 'jquery';

window.$ = JQuery;
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import '@/assets/bootstrap/dist/css/bootstrap.css'

import '@/assets/css/style.css'
import '@/assets/css/animate.css'
import '@/assets/css/colors/default-dark.css'
// import 'bootstrap/dist/css/bootstrap.css'
// import 'bootstrap-vue/dist/bootstrap-vue.css'


import { library } from '@fortawesome/fontawesome-svg-core'
import { faUserSecret } from '@fortawesome/free-solid-svg-icons'
import { faFile } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(faUserSecret,faFile)
Vue.use(BootstrapVue)
Vue.use(IconsPlugin)

Vue.component('font-awesome-icon', FontAwesomeIcon)


Vue.config.productionTip = false
new Vue({
    router,
    data: {
        host : 'http://127.0.0.1:5000'
    },
    methods : {
        htmlEntities(str) {
            return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
        },
        activeToggle(id) {
            window.$('.dropdown-menu').hide();
            window.$('#'+id).show();
        }
    },
    render: h => h(App),
}).$mount('#app')
