/**
 * Công cụ xem bộ đệm - Được sử dụng để kiểm tra xem tài nguyên CDN đã được Service Worker lưu vào bộ đệm hay chưa
 */

/**
 * Lấy tên của tất cả các bộ đệm của Service Worker
 * @returns {Promise<string[]>} Danh sách tên bộ đệm
 */
export const getCacheNames = async () => {
  if (!('caches' in window)) {
    return [];
  }
  
  try {
    return await caches.keys();
  } catch (error) {
    console.error('Không lấy được tên bộ nhớ đệm:', error);
    return [];
  }
};

/**
 * Nhận tất cả các mục trong bộ đệm được chỉ địnhURL
 * @param {string} cacheName tên bộ đệm
 * @returns {Promise<string[]>} danh sách URL được lưu trong bộ nhớ cache
 */
export const getCacheUrls = async (cacheName) => {
  if (!('caches' in window)) {
    return [];
  }
  
  try {
    const cache = await caches.open(cacheName);
    const requests = await cache.keys();
    return requests.map(request => request.url);
  } catch (error) {
    console.error(`Nhận bộ đệm ${cacheName} URL không thành công:`, error);
    return [];
  }
};

/**
 * Kiểm tra xem một URL cụ thể đã được lưu vào bộ nhớ đệm chưa
 * @param {string} url Để được kiểm traURL
 * @returns {Promise<boolean>} Nó có được lưu vào bộ nhớ đệm không?
 */
export const isUrlCached = async (url) => {
  if (!('caches' in window)) {
    return false;
  }
  
  try {
    const cacheNames = await getCacheNames();
    for (const cacheName of cacheNames) {
      const cache = await caches.open(cacheName);
      const match = await cache.match(url);
      if (match) {
        return true;
      }
    }
    return false;
  } catch (error) {
    console.error(`nghiên cứuURL ${url} Bộ nhớ đệm có bị lỗi hay không:`, error);
    return false;
  }
};

/**
 * Nhận trạng thái bộ đệm của tất cả tài nguyên CDN trên trang hiện tại
 * @returns {Promise<Object>} đối tượng trạng thái bộ đệm
 */
export const checkCdnCacheStatus = async () => {
  // Tìm tài nguyên từ bộ đệm CDN
  const cdnCaches = ['cdn-stylesheets', 'cdn-scripts'];
  const results = {
    css: [],
    js: [],
    totalCached: 0,
    totalNotCached: 0
  };
  
  for (const cacheName of cdnCaches) {
    try {
      const urls = await getCacheUrls(cacheName);
      
      // Phân biệt tài nguyên CSS và JS
      for (const url of urls) {
        if (url.endsWith('.css')) {
          results.css.push({ url, cached: true });
        } else if (url.endsWith('.js')) {
          results.js.push({ url, cached: true });
        }
        results.totalCached++;
      }
    } catch (error) {
      console.error(`lấy ${cacheName} Thông tin bộ nhớ đệm không thành công:`, error);
    }
  }
  
  return results;
};

/**
 * Xóa tất cả bộ nhớ đệm của service worker
 * @returns {Promise<boolean>} Xóa có thành công không?
 */
export const clearAllCaches = async () => {
  if (!('caches' in window)) {
    return false;
  }
  
  try {
    const cacheNames = await getCacheNames();
    for (const cacheName of cacheNames) {
      await caches.delete(cacheName);
    }
    return true;
  } catch (error) {
    console.error('Xóa tất cả bộ nhớ đệm không thành công:', error);
    return false;
  }
};

/**
 * Xuất trạng thái bộ đệm ra bàn điều khiển
 */
export const logCacheStatus = async () => {
  console.group('Service Worker trạng thái bộ đệm');
  
  const cacheNames = await getCacheNames();
  console.log('Đã phát hiện bộ đệm:', cacheNames);
  
  for (const cacheName of cacheNames) {
    const urls = await getCacheUrls(cacheName);
    console.group(`bộ nhớ đệm: ${cacheName} (${urls.length} mục)`);
    urls.forEach(url => console.log(url));
    console.groupEnd();
  }
  
  console.groupEnd();
  return cacheNames.length > 0;
}; 