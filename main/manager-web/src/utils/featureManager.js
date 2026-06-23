//Công cụ cấu hình chức năng
import Api from "@/apis/api";
import store from "@/store";

class FeatureManager {
    constructor() {
        this.defaultFeatures = {
            voiceprintRecognition: {
                name: 'feature.voiceprintRecognition.name',
                enabled: false,
                description: 'feature.voiceprintRecognition.description'
            },
            voiceClone: {
                name: 'feature.voiceClone.name',
                enabled: false,
                description: 'feature.voiceClone.description'
            },
            knowledgeBase: {
                name: 'feature.knowledgeBase.name',
                enabled: false,
                description: 'feature.knowledgeBase.description'
            },
            mcpAccessPoint: {
                name: 'feature.mcpAccessPoint.name',
                enabled: false,
                description: 'feature.mcpAccessPoint.description'
            },
            vad: {
                name: 'feature.vad.name',
                enabled: false,
                description: 'feature.vad.description'
            },
            asr: {
                name: 'feature.asr.name',
                enabled: false,
                description: 'feature.asr.description'
            },
            addressBook: {
                name: 'feature.addressBook.name',
                enabled: false,
                description: 'feature.addressBook.description'
            }
        };
        this.currentFeatures = { ...this.defaultFeatures }; // Cấu hình hiện có trong bộ nhớ
        this.initialized = false;
        this.initPromise = null;
    }

    /**
     * Đợi quá trình khởi tạo hoàn tất
     */
    async waitForInitialization() {
        if (!this.initPromise) {
            this.initPromise = this.init();
        }
        await this.initPromise;
        return this.initialized;
    }

    /**
     * Khởi tạo cấu hình chức năng
     */
    async init() {
        try {
            // Nhận cấu hình từ giao diện pub-config
            const config = await this.getConfigFromPubConfig();
            if (config) {
                this.currentFeatures = { ...config }; // Lưu vào bộ nhớ
                this.initialized = true;
                return;
            }
        } catch (error) {
            console.warn('Không lấy được cấu hình từ giao diện pub-config:', error);
        }

        // pub-configGiao diện không thành công, sử dụng cấu hình mặc định
        this.currentFeatures = { ...this.defaultFeatures }; // Lưu cấu hình mặc định vào bộ nhớ
        this.initialized = true;
    }

    /**
     * Cập nhật bộ đệm cấu hình
     */
    updateConfigCache(config) {
        store.commit('setPubConfig', config);
        localStorage.setItem('pubConfig', JSON.stringify(config));
    }

    /**
     * Nhận cấu hình từ giao diện pub-config
     */
    async getConfigFromPubConfig() {
        return new Promise((resolve) => {
            // Gọi trực tiếp giao diện pub-config để lấy cấu hình
            Api.user.getPubConfig((result) => {
                // Kiểm tra cấu trúc kết quả trả về
                if (result && result.status === 200) {
                    // Kiểm tra xem có trường dữ liệu không
                    if (result.data) {
                        const configCache = result.data.data || {};
                        // Kiểm tra xem có trường mã nào không, nếu có thì phán đoán theo mã đó
                        if (result.data.code !== undefined) {
                            if (result.data.code === 0 && result.data.data && result.data.data.systemWebMenu) {
                                try {
                                    let config;
                                    if (typeof result.data.data.systemWebMenu === 'string') {
                                        // Nếu là một chuỗi thì nó cần được phân tích (parse)JSON
                                        config = JSON.parse(result.data.data.systemWebMenu);
                                    } else {
                                        // Nếu nó đã là một đối tượng, hãy sử dụng nó trực tiếp
                                        config = result.data.data.systemWebMenu;
                                    }

                                    // Kiểm tra xem cấu hình có chứa các đối tượng tính năng hay không
                                    if (config && config.features) {
                                        // Đảm bảo hàm KnowledgeBase tồn tại và được cấu hình đúng
                                        if (!config.features.knowledgeBase) {
                                            console.warn('Hàm KnowledgeBase bị thiếu trong cấu hình và cấu hình mặc định đã được hợp nhất.');
                                            config.features = { ...this.defaultFeatures, ...config.features };
                                        }
                                        resolve(config.features);
                                    } else {
                                        console.warn('Đối tượng tính năng bị thiếu trong cấu hình, hãy sử dụng cấu hình mặc định');
                                        resolve(this.defaultFeatures);
                                    }
                                    configCache.systemWebMenu = config;
                                } catch (error) {
                                    console.warn('Không thể xử lý cấu hình systemWebMenu:', error);
                                    resolve(null);
                                }
                            } else {
                                console.warn('Nếu mã trả về giao diện không phải là 0 hoặc thiếu dữ liệu cần thiết, hãy sử dụng cấu hình mặc định.');
                                resolve(null);
                            }
                        } else {
                            // Nếu không có trường mã kiểm tra trực tiếpsystemWebMenu
                            if (result.data && result.data.systemWebMenu) {
                                try {
                                    let config;
                                    if (typeof result.data.systemWebMenu === 'string') {
                                        // Nếu là một chuỗi thì nó cần được phân tích (parse)JSON
                                        config = JSON.parse(result.data.systemWebMenu);
                                    } else {
                                        // Nếu nó đã là một đối tượng, hãy sử dụng nó trực tiếp
                                        config = result.data.systemWebMenu;
                                    }

                                    // Kiểm tra xem cấu hình có chứa các đối tượng tính năng hay không
                                    if (config && config.features) {
                                        // Đảm bảo hàm KnowledgeBase tồn tại và được cấu hình đúng
                                        if (!config.features.knowledgeBase) {
                                            console.warn('Hàm KnowledgeBase bị thiếu trong cấu hình và cấu hình mặc định đã được hợp nhất.');
                                            config.features = { ...this.defaultFeatures, ...config.features };
                                        }
                                        resolve(config.features);
                                    } else {
                                        console.warn('Đối tượng tính năng bị thiếu trong cấu hình, hãy sử dụng cấu hình mặc định');
                                        resolve(this.defaultFeatures);
                                    }
                                    configCache.systemWebMenu = config;
                                } catch (error) {
                                    console.warn('Không thể xử lý cấu hình systemWebMenu:', error);
                                    resolve(null);
                                }
                            } else {
                                console.warn('Giao diện trả về dữ liệu systemWebMenu bị thiếu và sử dụng cấu hình mặc định.');
                                resolve(null);
                            }
                        }
                        this.updateConfigCache(configCache)
                    } else {
                        console.warn('Trường dữ liệu bị thiếu trong dữ liệu được giao diện trả về và cấu hình mặc định được sử dụng.');
                        resolve(null);
                    }
                } else {
                    console.warn('pub-configCuộc gọi giao diện không thành công và cấu hình mặc định đã được sử dụng.');
                    resolve(null);
                }
            });
        });
    }

    /**
     * Nhận cấu hình hiện tại
     */
    getCurrentConfig() {
        // Trả về cấu hình hiện tại trong bộ nhớ
        return this.currentFeatures;
    }

    /**
     * Lưu cấu hình vào backendAPI
     */
    async saveConfig(config) {
        try {
            // Cập nhật cấu hình trong bộ nhớ
            this.currentFeatures = { ...config };

            // Lưu không đồng bộ vào phụ trợAPI
            this.saveConfigToAPI(config).catch(error => {
                console.warn('Không lưu được cấu hình vào API:', error);
            }).finally(() => {
                this.init()
            });

            // Sự kiện thay đổi cấu hình kích hoạt
            window.dispatchEvent(new CustomEvent('featureConfigChanged', {
                detail: config
            }));
        } catch (error) {
            console.error('Không lưu được cấu hình chức năng:', error);
        }
    }

    /**
     * Lưu cấu hình vào backendAPI
     */
    async saveConfigToAPI(config) {
        return new Promise((resolve) => {
            // Cập nhật thông số trực tiếp bằng ID đã biết (600)
            Api.admin.updateParam(
                {
                    id: 600,
                    paramCode: 'system-web.menu',
                    paramValue: JSON.stringify({
                        features: config,
                        groups: {
                            featureManagement: ["voiceprintRecognition", "voiceClone", "knowledgeBase", "mcpAccessPoint", "addressBook"],
                            voiceManagement: ["vad", "asr"]
                        }
                    }),
                    valueType: 'json',
                    remark: 'Cấu hình menu chức năng hệ thống'
                },
                (updateResult) => {
                    if (updateResult.code === 0) {
                        resolve();
                    } else {
                        // Nếu cập nhật không thành công, có thể do tham số không tồn tại hoặc lỗi khác, nó sẽ được ghi lại nhưng không ngăn việc lưu vàolocalStorage
                        console.warn('Không cập nhật được thông số:', updateResult.msg);
                        resolve(); // Đừng ngăn cản việc lưu vàolocalStorage
                    }
                },
                (error) => {
                    console.warn('Không cập nhật được thông số:', error);
                    resolve(); // Đừng ngăn cản việc lưu vàolocalStorage
                }
            );
        });
    }



    /**
     * Nhận tất cả các cấu hình chức năng
     */
    getAllFeatures() {
        return this.getCurrentConfig();
    }

    /**
     * Nhận một đối tượng cấu hình đơn giản hóa (đối với thành phần trang chủ）
     */
    getConfig() {
        const features = this.getAllFeatures();
        return {
            voiceprintRecognition: features.voiceprintRecognition?.enabled || false,
            voiceClone: features.voiceClone?.enabled || false,
            knowledgeBase: features.knowledgeBase?.enabled || false,
            mcpAccessPoint: features.mcpAccessPoint?.enabled || false,
            vad: features.vad?.enabled || false,
            asr: features.asr?.enabled || false,
            addressBook: features.addressBook?.enabled || false
        };
    }

    /**
     * Nhận trạng thái của chức năng được chỉ định
     */
    getFeatureStatus(featureKey) {
        const features = this.getAllFeatures();
        return features[featureKey]?.enabled || false;
    }

    /**
     * Đặt trạng thái chức năng
     */
    setFeatureStatus(featureKey, enabled) {
        const features = this.getAllFeatures();
        if (features[featureKey]) {
            features[featureKey].enabled = enabled;
            this.saveConfig(features);
            return true;
        }
        return false;
    }

    /**
     * Kích hoạt tính năng
     */
    enableFeature(featureKey) {
        return this.setFeatureStatus(featureKey, true);
    }

    /**
     * Tắt chức năng
     */
    disableFeature(featureKey) {
        return this.setFeatureStatus(featureKey, false);
    }

    /**
     * Chuyển đổi trạng thái chức năng
     */
    toggleFeature(featureKey) {
        const currentStatus = this.getFeatureStatus(featureKey);
        return this.setFeatureStatus(featureKey, !currentStatus);
    }

    /**
     * Đặt lại tất cả các chức năng về mặc định
     */
    resetToDefault() {
        this.saveConfig(this.defaultFeatures);
    }

    /**
     * Trạng thái tính năng cập nhật hàng loạt
     */
    updateFeatures(featureUpdates) {
        const features = this.getAllFeatures();
        Object.keys(featureUpdates).forEach(featureKey => {
            if (features[featureKey]) {
                features[featureKey].enabled = featureUpdates[featureKey];
            } else if (this.defaultFeatures[featureKey]) {
                features[featureKey] = { ...this.defaultFeatures[featureKey] };
                features[featureKey].enabled = featureUpdates[featureKey];
            }
        });
        this.saveConfig(features);
    }

    /**
     * Nhận danh sách các tính năng được kích hoạt
     */
    getEnabledFeatures() {
        const features = this.getAllFeatures();
        return Object.keys(features).filter(key => features[key].enabled);
    }

    /**
     * Kiểm tra xem tính năng đã được bật chưa
     */
    isFeatureEnabled(featureKey) {
        return this.getFeatureStatus(featureKey);
    }
}

// Tạo một cá thể đơn lẻ
const featureManager = new FeatureManager();

export default featureManager;