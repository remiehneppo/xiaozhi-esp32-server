import 'element-ui/lib/theme-chalk/index.css';
import 'normalize.css/normalize.css'; // A modern alternative to CSS resets
import Vue from 'vue';
import ElementUI from 'element-ui';
import App from './App.vue';
import router from './router';
import store from './store';
import i18n from './i18n';
import './styles/global.scss';
import { register as registerServiceWorker } from './registerServiceWorker';
import featureManager from './utils/featureManager';

// Tạo một bus sự kiện để liên lạc giữa các thành phần
Vue.prototype.$eventBus = new Vue();

Vue.use(ElementUI);

Vue.config.productionTip = false

// đăng kýService Worker
registerServiceWorker();

// Tạo một phiên bản Vue
new Vue({
  router,
  store,
  i18n,
  render: function (h) { return h(App) }
}).$mount('#app')
