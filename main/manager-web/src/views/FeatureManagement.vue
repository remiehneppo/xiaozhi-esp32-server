<template>
  <div class="welcome">
    <HeaderBar />

    <div class="operation-bar">
          <h2 class="page-title">{{ $t('header.featureManagement') }}</h2>
        </div>

    <div class="main-wrapper">
      <div class="content-panel">
        <div class="content-area">
          <el-card class="feature-card" shadow="never">
            <div class="config-header">
              <div class="header-icon">
                <img loading="lazy" src="@/assets/home/equipment.png" alt="" />
              </div>
              <div class="header-actions">
                <el-button @click="!isSaving && toggleSelectAll()" class="btn-select-all" :disabled="isSaving">
                  {{ isAllSelected ? $t('featureManagement.deselectAll') : $t('featureManagement.selectAll') }}
                </el-button>
                <el-button type="primary" class="save-btn" @click="handleSave" :disabled="isSaving">
                  {{ isSaving ? $t('featureManagement.saving') : $t('featureManagement.save') }}
                </el-button>
                <el-button class="reset-btn" @click="handleReset" :disabled="isSaving">
                  {{ $t('featureManagement.reset') }}
                </el-button>
              </div>
            </div>
            <div class="divider"></div>
            
            <!-- Vùng chứa nhóm chức năng - bố cục bên trái và bên phải -->
            <div class="feature-groups-container">
              <!-- Nhóm quản lý chức năng -->
              <div v-if="featureManagementFeatures.length > 0" class="feature-group">
                <h3 class="group-title">{{ $t('featureManagement.group.featureManagement') }}</h3>
                <div class="features-grid">
                  <div
                    v-for="feature in featureManagementFeatures"
                    :key="feature.id"
                    class="feature-card-item"
                    :class="{ 'feature-enabled': feature.enabled, 'feature-disabled': isSaving }"
                    @click="!isSaving && toggleFeature(feature)"
                  >
                    <div class="feature-header">
                      <h3 class="feature-name">{{ $t(`feature.${feature.id}.name`) }}</h3>
                      <el-checkbox
                        v-model="feature.enabled"
                        @change="!isSaving && toggleFeature(feature)"
                        class="feature-checkbox"
                        :disabled="isSaving"
                      />
                    </div>
                    <p class="feature-description">{{ $t(`feature.${feature.id}.description`) }}</p>
                  </div>
                </div>
              </div>
              
              <!-- Nhóm quản lý giọng nói -->
              <div v-if="voiceManagementFeatures.length > 0" class="feature-group">
                <h3 class="group-title">{{ $t('featureManagement.group.voiceManagement') }}</h3>
                <div class="features-grid">
                  <div
                    v-for="feature in voiceManagementFeatures"
                    :key="feature.id"
                    class="feature-card-item"
                    :class="{ 'feature-enabled': feature.enabled, 'feature-disabled': isSaving }"
                    @click="!isSaving && toggleFeature(feature)"
                  >
                    <div class="feature-header">
                      <h3 class="feature-name">{{ $t(`feature.${feature.id}.name`) }}</h3>
                      <el-checkbox
                        v-model="feature.enabled"
                        @change="!isSaving && toggleFeature(feature)"
                        class="feature-checkbox"
                        :disabled="isSaving"
                      />
                    </div>
                    <p class="feature-description">{{ $t(`feature.${feature.id}.description`) }}</p>
                  </div>
                </div>
              </div>
            </div>
            
            <div v-if="filteredFeatures.length === 0" class="empty-state">
              <el-empty :description="$t('featureManagement.noFeatures')">
                <p class="empty-tip">{{ $t('featureManagement.contactAdmin') }}</p>
              </el-empty>
            </div>
          </el-card>
        </div>
      </div>
    </div>

    <el-footer>
      <VersionFooter />
    </el-footer>
  </div>
</template>

<script>
import HeaderBar from "@/components/HeaderBar.vue";
import VersionFooter from "@/components/VersionFooter.vue";
import featureManager from "@/utils/featureManager.js";

export default {
  name: "FeatureManagement",
  components: {
    HeaderBar,
    VersionFooter
  },
  data() {
    return {
      pendingChanges: false,
      featureManagementFeatures: [],
      voiceManagementFeatures: [],
      isSaving: false // Thêm khóa trạng thái lưu
    }
  },
  computed: {
    // Tất cả danh sách tính năng
    filteredFeatures() {
      return [...this.featureManagementFeatures, ...this.voiceManagementFeatures]
    },
    
    // Xác định xem tất cả các tính năng có được chọn hay không
    isAllSelected() {
      const allFeatures = [...this.featureManagementFeatures, ...this.voiceManagementFeatures]
      return allFeatures.length > 0 && allFeatures.every(feature => feature.enabled)
    }
  },
  async created() {
    // Đợi quá trình khởi tạo Trình quản lý cấu hình chức năng hoàn tất
    try {
      await featureManager.waitForInitialization()
      await this.loadFeatures()
      this.setupConfigChangeListener()
    } catch (error) {
      console.error('Chờ khởi tạo trình quản lý cấu hình chức năng không thành công:', error)
      await this.loadFeatures()
      this.setupConfigChangeListener()
    }
  },
  
  beforeDestroy() {
    this.removeConfigChangeListener()
  },
  
  methods: {
    // Nhận chức năng dựa trên danh sách ID
    async getFeaturesByIds(featureIds) {
      try {
        const featureConfig = await featureManager.getAllFeatures()
        const result = featureIds.map(id => {
          const feature = featureConfig[id]
          return {
            id: id,
            name: this.$t(`feature.${id}.name`),
            description: this.$t(`feature.${id}.description`),
            enabled: feature?.enabled || false
          }
        })
        
        return result
      } catch (error) {
        console.error('Không thể lấy được cấu hình chức năng:', error)
        // Nếu việc thu thập không thành công, hãy quay lại cấu hình mặc định
        return featureIds.map(id => ({
          id: id,
          name: this.$t(`feature.${id}.name`),
          description: this.$t(`feature.${id}.description`),
          enabled: false
        }))
      }
    },
    
    // Cấu hình chức năng tải
    async loadFeatures() {
      // Lưu trạng thái lựa chọn của người dùng hiện tại
      const currentFeatureStates = {}
      const allCurrentFeatures = [...this.featureManagementFeatures, ...this.voiceManagementFeatures]
      allCurrentFeatures.forEach(feature => {
        currentFeatureStates[feature.id] = feature.enabled
      })
      
      // Tải lại cấu hình
      this.featureManagementFeatures = await this.getFeaturesByIds(['voiceprintRecognition', 'voiceClone', 'knowledgeBase', 'mcpAccessPoint', 'addressBook'])
      this.voiceManagementFeatures = await this.getFeaturesByIds(['vad', 'asr'])
      
      // Khôi phục trạng thái lựa chọn của người dùng (nếu có)）
      const allFeatures = [...this.featureManagementFeatures, ...this.voiceManagementFeatures]
      allFeatures.forEach(feature => {
        if (currentFeatureStates.hasOwnProperty(feature.id)) {
          feature.enabled = currentFeatureStates[feature.id]
        }
      })
    },
    // Chuyển đổi trạng thái chức năng
    async toggleFeature(feature) {
      // Nếu đang lưu, hãy chặn thao tác
      if (this.isSaving) {
        return
      }
      
      feature.enabled = !feature.enabled
      this.pendingChanges = true
      
      // Không còn cập nhật ngay lên trình quản lý cấu hình, chỉ các bản cập nhật được thống nhất khi lưu
    },
    // Lưu cấu hình
    async handleSave() {
      if (!this.pendingChanges) {
        this.$message.info({
          message: this.$t('featureManagement.noChanges'),
          showClose: true
        })
        return
      }
      
      // Đặt trạng thái lưu và khóa giao diện
      this.isSaving = true
      
      try {
        // Nhận trạng thái hiện tại của tất cả các chức năng và lưu nó
        const featureUpdates = {}
        const allFeatures = [...this.featureManagementFeatures, ...this.voiceManagementFeatures]
        allFeatures.forEach(feature => {
          featureUpdates[feature.id] = feature.enabled
        })
        await featureManager.updateFeatures(featureUpdates)
        
        this.pendingChanges = false
        this.$message.success({
          message: this.$t('featureManagement.saveSuccess'),
          showClose: true
        })

        setTimeout(() => {
          this.loadFeatures()
        }, 1000)
      } catch (error) {
        console.error('Không lưu được cấu hình:', error)
        this.$message.error({
          message: this.$t('featureManagement.saveError'),
          showClose: true
        })
      } finally {
        // Bất kể thành công hay thất bại, hãy mở khóa trạng thái lưu
        this.isSaving = false
      }
    },
    // Đặt trình nghe thay đổi cấu hình
    setupConfigChangeListener() {
      this.configChangeHandler = () => {
        this.loadFeatures()
      }
      window.addEventListener('featureConfigReloaded', this.configChangeHandler)
    },
    
    // Xóa trình nghe thay đổi cấu hình
    removeConfigChangeListener() {
      if (this.configChangeHandler) {
        window.removeEventListener('featureConfigReloaded', this.configChangeHandler)
      }
    },
    
    // Đặt lại cấu hình
    async handleReset() {
      try {
        await this.$confirm(
          this.$t('featureManagement.resetConfirm'),
          this.$t('featureManagement.reset'),
          {
            confirmButtonText: this.$t('featureManagement.confirm'),
            cancelButtonText: this.$t('featureManagement.cancel'),
            type: 'warning'
          }
        )
        
        featureManager.resetToDefault()
        this.loadFeatures()
        this.pendingChanges = false
        
        this.$message.success({
          message: this.$t('featureManagement.resetSuccess'),
          showClose: true
        })
        
        setTimeout(() => {
          this.loadFeatures()
          this.$router.go(0)
        }, 1000)
      } catch (error) {
        // Người dùng hủy thao tác
      }
    },
    // Chức năng tìm kiếm (giao diện dành riêng）
    handleSearch() {
      // Chức năng tìm kiếm sẽ được thực hiện
    },
    // Chọn tất cả/Bỏ chọn tất cả
    toggleSelectAll() {
      // Nếu đang lưu, hãy chặn thao tác
      if (this.isSaving) {
        return
      }
      
      const allFeatures = [...this.featureManagementFeatures, ...this.voiceManagementFeatures]
      const newStatus = !this.isAllSelected
      
      allFeatures.forEach(feature => {
        feature.enabled = newStatus
      })
      
      this.pendingChanges = true
    }
  }
}
</script>

<style scoped>
.welcome {
  min-width: 900px;
  min-height: 506px;
  height: 100vh;
  display: flex;
  position: relative;
  flex-direction: column;
  background-size: cover;
  background: linear-gradient(to bottom right, #dce8ff, #e4eeff, #e6cbfd) center;
  -webkit-background-size: cover;
  -o-background-size: cover;
  overflow: hidden;
}

.operation-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
}

.page-title {
  font-size: 24px;
  margin: 0;
}

.config-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 0 16px 0;
}

.header-icon {
  width: 40px;
  height: 40px;
  background: #5778ff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 12px;
}

.header-icon img {
  width: 20px;
  height: 20px;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-left: auto;
}

.divider {
  height: 1px;
  background: #e0e0e0;
  margin-bottom: 20px;
}

.btn-select-all {
  background: #e6ebff;
  color: #5778ff;
  border: 1px solid #adbdff;
  border-radius: 18px;
  padding: 8px 16px;
  height: 32px;
  font-size: 14px;
}

.btn-select-all:hover {
  background: #d0d8ff;
}

.save-btn {
  background: #5778ff;
  color: white;
  border: none;
  border-radius: 18px;
  padding: 8px 16px;
  height: 32px;
  font-size: 14px;
}

.save-btn:hover {
  background: #4a6ae8;
}

.reset-btn {
  background: #e6ebff;
  color: #5778ff;
  border: 1px solid #adbdff;
  border-radius: 18px;
  padding: 8px 16px;
  height: 32px;
}

.reset-btn:hover {
  background: #d0d8ff;
}

.main-wrapper {
  height: calc(100vh - 63px - 35px - 58px);
  margin: 0 22px;
  border-radius: 15px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  position: relative;
  background: rgba(237, 242, 255, 0.5);
  display: flex;
  flex-direction: column;
}

.content-panel {
  flex: 1;
  display: flex;
  overflow: hidden;
  height: 100%;
  border-radius: 15px;
  background: transparent;
  border: 1px solid #fff;
}

.content-area {
  flex: 1;
  height: 100%;
  min-width: 600px;
  overflow: auto;
  background-color: white;
  display: flex;
  flex-direction: column;
}

.feature-card {
  background: white;
  flex: 1;
  display: flex;
  flex-direction: column;
  border: none;
  box-shadow: none;
  overflow: hidden;
}

.feature-card ::v-deep .el-card__body {
  padding: 24px;
  display: flex;
  flex-direction: column;
  flex: 1;
  overflow: hidden;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}

.feature-card-item {
  display: flex;
  flex-direction: column;
  padding: 20px;
  border-radius: 12px;
  border: 2px solid #e0e0e0;
  background-color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  user-select: none;
  position: relative;
}

.feature-card-item:hover {
  border-color: #869bf0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.feature-card-item.feature-enabled {
  border-color:#5778ff;
  box-shadow: 0 4px 16px rgba(95, 112, 243, 0.2);
  transform: translateY(-2px);
}

.feature-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.feature-checkbox ::v-deep .el-checkbox__input {
  transform: scale(1.2);
}

.feature-checkbox ::v-deep .el-checkbox__input.is-checked .el-checkbox__inner {
  background-color: #5778ff;
  border-color: #5778ff;
}

.feature-checkbox ::v-deep .el-checkbox__input.is-checked + .el-checkbox__label {
  color: #5778ff;
}


.feature-name {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin: 0;
  transition: color 0.3s ease;
}


.feature-description {
  font-size: 14px;
  line-height: 1.6;
  color: #666;
  margin: 0 0 12px 0;
  transition: color 0.3s ease;
  text-align: left;
}


/* Vùng chứa nhóm chức năng - bố cục bên trái và bên phải */
.feature-groups-container {
  display: flex;
  gap: 32px;
  align-items: flex-start;
  position: relative;
}

/* Dấu phân cách giữa các nhóm */
.feature-groups-container::before {
  content: '';
  position: absolute;
  left: 50%;
  top: 0;
  bottom: 0;
  width: 1px;
  height: 550px;
  background: #e0e0e0;
  opacity: 0.5;
  transform: translateX(-50%);
}

/* Kiểu nhóm */
.feature-group {
  flex: 1;
  min-width: 0;
  margin-bottom: 32px;
}

.group-title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 12px;
  padding-left: 12px;
  border-left: 4px solid #5f70f3;
  text-align: left;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}
</style>