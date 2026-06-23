import Vue from 'vue';
import VueI18n from 'vue-i18n';
import zhCN from './zh_CN';
import zhTW from './zh_TW';
import en from './en';
import de from './de';
import vi from './vi';
import ptBR from './pt_BR';

Vue.use(VueI18n);

// Lấy cài đặt ngôn ngữ từ bộ nhớ cục bộ, nếu không tìm thấy thì dùng ngôn ngữ của trình duyệt hoặc mặc định
const getDefaultLanguage = () => {
  const savedLang = localStorage.getItem('userLanguage');
  if (savedLang) {
    return savedLang;
  }
  const browserLang = navigator.language || navigator.userLanguage;
  if (browserLang.indexOf('zh') === 0) {
    if (browserLang === 'zh-TW' || browserLang === 'zh-HK' || browserLang === 'zh-MO') {
      return 'zh_TW';
    }
    return 'zh_CN';
  }
  if (browserLang.indexOf('de') === 0) {
    return 'de';
  }
  if (browserLang.indexOf('vi') === 0) {
    return 'vi';
  }
  if (browserLang === 'pt-BR' || browserLang === 'pt') {
    return 'pt_BR';
  }
  return 'en';
};

const i18n = new VueI18n({
  locale: getDefaultLanguage(),
  fallbackLocale: 'zh_CN',
  messages: {
    'zh_CN': zhCN,
    'zh_TW': zhTW,
    'en': en,
    'de': de,
    'vi': vi,
    'pt_BR': ptBR
  }
});

export default i18n;

// Cung cấp một phương thức để chuyển đổi ngôn ngữ
export const changeLanguage = (lang) => {
  i18n.locale = lang;
  localStorage.setItem('userLanguage', lang);
  // Thông báo cho component rằng ngôn ngữ đã thay đổi
  Vue.prototype.$eventBus.$emit('languageChanged', lang);
};