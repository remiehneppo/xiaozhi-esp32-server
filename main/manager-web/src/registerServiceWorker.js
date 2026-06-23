/* eslint-disable no-console */

export const register = () => {
  if (process.env.NODE_ENV === 'production' && 'serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      const swUrl = `${process.env.BASE_URL}service-worker.js`;
      
      console.info(`[Dịch vụ Xiaozhi] Đang cố gắng đăng kýService Worker，URL: ${swUrl}`);
      
      // Trước tiên hãy kiểm tra xem Service Worker đã được đăng ký chưa
      navigator.serviceWorker.getRegistrations().then(registrations => {
        if (registrations.length > 0) {
          console.info('[Dịch vụ Xiaozhi] Người ta thấy rằng Service Worker đã được đăng ký và đang kiểm tra các bản cập nhật.');
        }
        
        // Tiếp tục đăng kýService Worker
        navigator.serviceWorker
          .register(swUrl)
          .then(registration => {
            console.info('[Dịch vụ Xiaozhi] Service WorkerĐăng ký thành công');
            
            // Xử lý cập nhật
            registration.onupdatefound = () => {
              const installingWorker = registration.installing;
              if (installingWorker == null) {
                return;
              }
              installingWorker.onstatechange = () => {
                if (installingWorker.state === 'installed') {
                  if (navigator.serviceWorker.controller) {
                    // Nội dung đã được lưu trữ và cập nhật. Thông báo cho người dùng để làm mới.
                    console.log('[Dịch vụ Xiaozhi] Có nội dung mới, vui lòng làm mới trang');
                    // Mẹo cập nhật có thể được hiển thị ở đây
                    const updateNotification = document.createElement('div');
                    updateNotification.style.cssText = `
                      position: fixed;
                      bottom: 20px;
                      right: 20px;
                      background: #409EFF;
                      color: white;
                      padding: 12px 20px;
                      border-radius: 4px;
                      box-shadow: 0 2px 12px 0 rgba(0,0,0,.1);
                      z-index: 9999;
                    `;
                    const savedLang = localStorage.getItem('userLanguage');
                    let text = 'Đã tìm thấy phiên bản mới, nhấp để làm mới ứng dụng';
                    let btnText = 'làm cho khỏe lại';
                    if (savedLang === 'en') {
                      text = 'New version found, click to refresh';
                      btnText = 'Refresh';
                    } else if (savedLang === 'vi') {
                      text = 'Đã có phiên bản mới, click để làm mới';
                      btnText = 'Làm mới';
                    } else if (savedLang === 'de') {
                      text = 'Neue Version gefunden, zum Aktualisieren klicken';
                      btnText = 'Aktualisieren';
                    } else if (savedLang === 'pt_BR') {
                      text = 'Nova versão encontrada, clique para atualizar';
                      btnText = 'Atualizar';
                    } else if (savedLang === 'zh_TW') {
                      text = 'Đã tìm thấy phiên bản mới, nhấp để làm mới ứng dụng';
                      btnText = 'làm cho khỏe lại';
                    }
                    updateNotification.innerHTML = `
                      <div style="display: flex; align-items: center;">
                        <span style="margin-right: 10px;">${text}</span>
                        <button style="background: white; color: #409EFF; border: none; padding: 5px 10px; border-radius: 3px; cursor: pointer;">${btnText}</button>
                      </div>
                    `;
                    document.body.appendChild(updateNotification);
                    updateNotification.querySelector('button').addEventListener('click', () => {
                      window.location.reload();
                    });
                  } else {
                    // Mọi thứ đều hoạt động tốt và Service Worker đã được cài đặt thành công
                    console.log('[Dịch vụ Xiaozhi] Nội dung được lưu vào bộ nhớ đệm để sử dụng ngoại tuyến');
                    
                    // Bạn có thể khởi tạo bộ đệm ở đây
                    setTimeout(() => {
                      // Khởi động bộ đệm CDN
                      const cdnUrls = [
                        'https://unpkg.com/element-ui@2.15.14/lib/theme-chalk/index.css',
                        'https://cdnjs.cloudflare.com/ajax/libs/normalize/8.0.1/normalize.min.css',
                        'https://unpkg.com/vue@2.6.14/dist/vue.min.js',
                        'https://unpkg.com/vue-router@3.6.5/dist/vue-router.min.js',
                        'https://unpkg.com/vuex@3.6.2/dist/vuex.min.js',
                        'https://unpkg.com/element-ui@2.15.14/lib/index.js',
                        'https://unpkg.com/axios@0.27.2/dist/axios.min.js',
                        'https://unpkg.com/opus-decoder@0.7.7/dist/opus-decoder.min.js'
                      ];
                      
                      // Bộ đệm ấm
                      cdnUrls.forEach(url => {
                        fetch(url, { mode: 'no-cors' }).catch(err => {
                          console.log(`Bộ đệm ấm ${url} thất bại`, err);
                        });
                      });
                    }, 2000);
                  }
                }
              };
            };
          })
          .catch(error => {
            console.error('Service Worker Đăng ký không thành công:', error);
            
            if (error.name === 'TypeError' && error.message.includes('Failed to register a ServiceWorker')) {
              console.warn('[Dịch vụ Xiaozhi] Đã xảy ra lỗi mạng khi đăng ký Service Worker và tài nguyên CDN có thể không được lưu vào bộ đệm.');
              if (process.env.NODE_ENV === 'production') {
                console.info(
                  'Các lý do có thể: 1. Máy chủ không được định cấu hình đúng loại MIME 2. Sự cố chứng chỉ SSL máy chủ 3. Máy chủ không trả về tệp service-worker.js'
                );
              }
            }
          });
      });
    });
  }
};

export const unregister = () => {
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.ready
      .then(registration => {
        registration.unregister();
      })
      .catch(error => {
        console.error(error.message);
      });
  }
}; 