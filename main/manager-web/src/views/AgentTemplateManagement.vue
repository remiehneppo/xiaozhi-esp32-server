<template>
  <div class="welcome">
    <HeaderBar />

    <div class="operation-bar">
      <h2 class="page-title">{{ $t("agentTemplateManagement.title") }}</h2>
      <div class="right-operations">
        <el-input
          :placeholder="$t('agentTemplateManagement.searchPlaceholder')"
          v-model="search"
          class="search-input"
          clearable
          @keyup.enter.native="handleSearch"
          style="width: 240px"
        />
        <el-button class="btn-search" @click="handleSearch">
          {{ $t("agentTemplateManagement.search") }}
        </el-button>
      </div>
    </div>

    <!-- Nội dung chính -->
    <div class="main-wrapper">
      <div class="content-panel">
        <div class="content-area">
          <el-card class="template-card" shadow="never">
            <el-table
              ref="templateTable"
              :data="templateList"
              style="width: 100%"
              v-loading="templateLoading"
              :element-loading-text="$t('agentTemplateManagement.loading')"
              element-loading-spinner="el-icon-loading"
              element-loading-background="rgba(255, 255, 255, 0.7)"
              class="transparent-table"
              :header-cell-style="{ padding: '10px 20px' }"
              :cell-style="{ padding: '10px 20px' }"
            >
              <!-- Di dời@row-click="handleRowClick" -->
              <!-- Tùy chỉnh cột lựa chọn và nhận ra tiêu đề là"chọn"Văn bản, dòng dữ liệu là những ô nhỏ -->
              <el-table-column
                :label="$t('agentTemplateManagement.select')"
                align="center"
                min-width="100"
              >
                <template slot-scope="scope">
                  <el-checkbox
                    v-model="scope.row.selected"
                    @change="handleRowSelectionChange(scope.row)"
                    @click.stop
                  ></el-checkbox>
                </template>
              </el-table-column>
              <!-- Tên mẫu -->
              <el-table-column
                :label="$t('agentTemplateManagement.templateName')"
                prop="agentName"
                min-width="250"
                show-overflow-tooltip
              >
                <template slot-scope="scope">
                  <span>{{ scope.row.agentName }}</span>
                </template>
              </el-table-column>
              <!-- Sửa đổi thành cột số sê-ri và di chuyển vào đây -->
              <el-table-column
                :label="$t('agentTemplateManagement.serialNumber')"
                min-width="120"
                align="center"
              >
                <template slot-scope="scope">
                  <span>{{ (currentPage - 1) * pageSize + scope.$index + 1 }}</span>
                </template>
              </el-table-column>
              <!-- Cột thao tác -->
              <el-table-column
                :label="$t('agentTemplateManagement.action')"
                min-width="250"
                align="center"
              >
                <template slot-scope="scope">
                  <div style="display: flex; justify-content: center; gap: 15px">
                    <el-button type="text" @click="editTemplate(scope.row)">{{
                      $t("agentTemplateManagement.editTemplate")
                    }}</el-button>
                    <el-button type="text" @click="deleteTemplate(scope.row)">{{
                      $t("agentTemplateManagement.deleteTemplate")
                    }}</el-button>
                  </div>
                </template>
              </el-table-column>
            </el-table>

            <!-- Thanh tác vụ ở cuối bảng -->
            <div class="table_bottom">
              <div class="ctrl_btn">
                <el-button
                  type="primary"
                  @click="handleSelectAll"
                  size="mini"
                  class="select-all-btn"
                >
                  {{
                    isAllSelected
                      ? $t("agentTemplateManagement.deselectAll")
                      : $t("agentTemplateManagement.selectAll")
                  }}
                </el-button>
                <el-button type="success" @click="showAddTemplateDialog" size="mini">
                  {{ $t("agentTemplateManagement.createTemplate") }}
                </el-button>
                <el-button
                  type="danger"
                  @click="batchDeleteTemplate"
                  :disabled="!hasSelected"
                  size="mini"
                >
                  {{ $t("agentTemplateManagement.batchDelete") }}
                </el-button>
              </div>

              <!-- Phân trang -->
              <div class="custom-pagination">
                <el-pagination
                  v-model:current-page="currentPage"
                  v-model:page-size="pageSize"
                  :page-sizes="pageSizeOptions"
                  layout="total, sizes, prev, pager, next, jumper"
                  :total="total"
                  @size-change="handlePageSizeChange"
                  @current-change="handlePageChange"
                />
              </div>
            </div>
          </el-card>
        </div>
      </div>
    </div>
    <el-footer>
      <version-footer />
    </el-footer>
  </div>
</template>

<script>
import HeaderBar from "@/components/HeaderBar";
import agentApi from "@/apis/module/agent";
import VersionFooter from "@/components/VersionFooter.vue";

export default {
  name: "AgentTemplateManagement",
  components: {
    HeaderBar,
    VersionFooter
  },

  data() {
    return {
      // Mẫu liên quan
      templateList: [],
      templateLoading: false,
      selectedTemplates: [],
      isAllSelected: false, // Thêm trạng thái chọn tất cả

      search: "",
      // Dữ liệu liên quan đến phân trang
      pageSizeOptions: [10, 20, 50, 100],
      currentPage: 1,
      pageSize: 10,
      total: 0,
    };
  },
  created() {
    this.loadTemplateList();
  },
  // Thêm thuộc tính hasSelected vào phần tính toán
  computed: {
    pageCount() {
      return Math.ceil(this.total / this.pageSize);
    },
    visiblePages() {
      return this.getVisiblePages();
    },
    hasSelected() {
      return this.selectedTemplates.length > 0;
    },
  },
  methods: {
    // Tải danh sách mẫu
// Cải thiện logic xử lý lỗi của phương thức LoadTemplateList
    loadTemplateList() {
      this.templateLoading = true;
      const params = {
        page: this.currentPage,
        limit: this.pageSize,
      };
      if (this.search) {
        params.agentName = this.search;
      }

      try {
        agentApi.getAgentTemplatesPage(
          params,
          (res) => {
            // Logic xử lý phản hồi mạnh mẽ hơn
            if (res && typeof res === "object") {
              if (res.data && res.data.code === 0) {
                const responseData = res.data.data || {};
                // Thêm thuộc tính đã chọn vào mỗi mẫu
                this.templateList = Array.isArray(responseData.list)
                  ? responseData.list.map((item) => ({ ...item, selected: false }))
                  : [];
                this.total =
                  typeof responseData.total === "number" ? responseData.total : 0;
              } else {
                this.templateList = [];
                this.total = 0;
                this.$message.error(
                  res?.data?.msg || this.$t("agentTemplateManagement.fetchTemplateFailed")
                );
              }
            } else {
              this.templateList = [];
              this.total = 0;
              this.$message.error(
                this.$t("agentTemplateManagement.fetchTemplateBackendError")
              );
            }
            this.templateLoading = false;
          },
          (error) => {
            this.templateList = [];
            this.total = 0;
            this.templateLoading = false;
            this.$message.error(this.$t("common.networkError"));
          }
        );
      } catch (error) {
        this.templateList = [];
        this.total = 0;
        this.templateLoading = false;
        this.$message.error(this.$t("agentTemplateManagement.fetchTemplateBackendError"));
      }
    },

    // Tìm kiếm mẫu
    handleSearch() {
      if (this.search) {
        const searchValue = this.search.toLowerCase();
        const filteredList = this.templateList.filter((template) =>
          template.agentName.toLowerCase().includes(searchValue)
        );
        this.templateList = filteredList;
        this.total = filteredList.length;
      } else {
        this.loadTemplateList();
      }
    },

    // Sửa đổi phương thức showAddTemplateDialog để chuyển đến cùng trang với trang chỉnh sửa
// Hiển thị cửa sổ bật lên mẫu mới
    showAddTemplateDialog() {
      // Chuyển đến trang cấu hình nhanh mẫu, không chuyển tham số templateId để biểu thị phần bổ sung mới
      this.$router.push({
        path: "/template-quick-config",
      });
    },

    // Chỉnh sửa mẫu
    editTemplate(row) {
      // Chuyển đến trang cấu hình nhanh mẫu và chuyển tham số ID mẫu
      this.$router.push({
        path: "/template-quick-config",
        query: { templateId: row.id },
      });
    },

    // Xóa mẫu
    deleteTemplate(row) {
      this.$confirm(
        this.$t("agentTemplateManagement.confirmSingleDelete"),
        this.$t("common.warning"),
        {
          confirmButtonText: this.$t("common.confirm"),
          cancelButtonText: this.$t("common.cancel"),
          type: "warning",
        }
      )
        .then(() => {
          agentApi.deleteAgentTemplate(row.id, (res) => {
            if (res && typeof res === "object") {
              // Kiểm tra xem res.data có tồn tại và chứacode=0
              if (res.data && res.data.code === 0) {
                this.$message.success(this.$t("agentTemplateManagement.deleteSuccess"));
                this.loadTemplateList();
              } else {
                this.$message.error(
                  res?.data?.msg || this.$t("agentTemplateManagement.deleteFailed")
                );
              }
            } else {
              this.$message.error(this.$t("agentTemplateManagement.deleteBackendError"));
            }
          });
        })
        .catch(() => {
          this.$message.info(this.$t("common.deleteCancelled"));
        });
    },

    // Xóa mẫu theo đợt
    batchDeleteTemplate() {
      if (this.selectedTemplates.length === 0) {
        this.$message.warning(this.$t("agentTemplateManagement.selectTemplate"));
        return;
      }

      this.$confirm(
        this.$t("agentTemplateManagement.confirmBatchDelete", {
          count: this.selectedTemplates.length,
        }),
        this.$t("common.warning"),
        {
          confirmButtonText: this.$t("common.confirm"),
          cancelButtonText: this.$t("common.cancel"),
          type: "warning",
        }
      )
        .then(() => {
          // Đảm bảo các tham số có định dạng chính xác - sử dụng mảng id làm nội dung yêu cầu
          const ids = this.selectedTemplates.map((template) => template.id);

          agentApi.batchDeleteAgentTemplate(ids, (res) => {
            if (res && typeof res === "object") {
              if (res.data && res.data.code === 0) {
                this.$message.success(
                  this.$t("agentTemplateManagement.batchDeleteSuccess")
                );
                // Tải lại danh sách mẫu
                this.loadTemplateList();
                // Xóa lựa chọn
                this.selectedTemplates = [];
                this.isAllSelected = false;
              } else {
                this.$message.error(
                  res?.data?.msg || this.$t("agentTemplateManagement.batchDeleteFailed")
                );
              }
            } else {
              this.$message.error(this.$t("agentTemplateManagement.deleteBackendError"));
            }
          });
        })
        .catch(() => {
          this.$message.info(this.$t("common.deleteCancelled"));
        });
    },

    // Cải thiện các phương pháp liên quan đến phân trang
    handlePageChange(page) {
      this.currentPage = page;
      this.loadTemplateList();
    },

    handlePageSizeChange(size) {
      this.pageSize = size;
      this.currentPage = 1;
      this.loadTemplateList();
    },

    goFirst() {
      this.currentPage = 1;
    },
    goPrev() {
      this.currentPage--;
    },
    goNext() {
      this.currentPage++;
    },
    goToPage(page) {
      this.currentPage = page;
    },
    getVisiblePages() {
      const pages = [];
      const totalPages = this.pageCount;
      const currentPage = this.currentPage;

      if (totalPages <= 7) {
        for (let i = 1; i <= totalPages; i++) {
          pages.push(i);
        }
      } else {
        if (currentPage <= 4) {
          for (let i = 1; i <= 5; i++) {
            pages.push(i);
          }
          pages.push("...");
          pages.push(totalPages);
        } else if (currentPage >= totalPages - 3) {
          pages.push(1);
          pages.push("...");
          for (let i = totalPages - 4; i <= totalPages; i++) {
            pages.push(i);
          }
        } else {
          pages.push(1);
          pages.push("...");
          for (let i = currentPage - 1; i <= currentPage + 1; i++) {
            pages.push(i);
          }
          pages.push("...");
          pages.push(totalPages);
        }
      }

      return pages;
    },

    // Sửa đổi phương thức handSelectAll
    handleSelectAll() {
      this.isAllSelected = !this.isAllSelected;
      this.templateList.forEach((row) => {
        row.selected = this.isAllSelected;
      });
      // Cập nhật danh sách mẫu đã chọn
      this.selectedTemplates = this.isAllSelected ? [...this.templateList] : [];
    },

    // Xử lý các thay đổi lựa chọn hàng
    handleRowSelectionChange(row) {
      // Tìm mẫu đã chọn
      this.selectedTemplates = this.templateList.filter((template) => template.selected);
      // Cập nhật trạng thái đã chọn
      this.isAllSelected =
        this.templateList.length > 0 &&
        this.selectedTemplates.length === this.templateList.length;
    },
  },
};
</script>

<style scoped lang="scss">
/* Cài đặt nền và bố cục cơ bản */
.welcome {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  position: relative;
  background: linear-gradient(to bottom right, #dce8ff, #e4eeff, #e6cbfd) center;
  background-size: cover;
  overflow: hidden;
  width: 100%;
}

/* Phong cách thanh hành động */
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

.right-operations {
  display: flex;
  align-items: center;
  gap: 10px;
}

.search-input {
  width: 200px;
}

.btn-search {
  background: linear-gradient(135deg, #6b8cff, #a966ff);
  border: none;
  color: white;
}

/* Kiểu thùng chứa chính */
.main-wrapper {
  // Truy vấn 35px dưới cùng 63px trên cùng72px
  height: calc(100vh - 63px - 35px - 72px);
  margin: 0 22px;
  border-radius: 15px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  position: relative;
  background: rgba(237, 242, 255, 0.5);
  display: flex;
  flex-direction: column;
}

.content-panel {
  width: 100%;
  flex: 1;
  display: flex;
  overflow: hidden;
  border-radius: 15px;
  background: transparent;
  border: 1px solid #fff;
}

.content-area {
  flex: 1;
  min-width: 600px;
  overflow-x: auto;
  background-color: white;
  display: flex;
  flex-direction: column;
  position: relative;
}

/* Phong cách thẻ mẫu */
.template-card {
  border: none;
  box-shadow: none;
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;

  :deep(.el-card__body) {
    padding: 15px;
    display: flex;
    flex-direction: column;
    flex: 1;
    overflow: hidden;
  }
}

/* Kiểu bảng - phiên bản tích hợp tối ưu */
.transparent-table {
  width: 100%;
  flex: 1;
  min-height: 0;
}

:deep(.el-table) {
  height: 100%;
  display: flex;
  flex-direction: column;
  --table-max-height: calc(100vh - 42vh);
  max-height: var(--table-max-height);

  /* Kiểu tiêu đề bảng */
  .el-table__header th {
    padding: 8px 0 !important;
    height: 40px !important;
  }

  .el-table__header th .cell {
    color: #303133 !important;
    font-weight: 600;
  }

  /* Kiểu dáng thân bàn */
  .el-table__body {
    .el-table__row td {
      padding: 12px 0 !important;
      border-bottom: 1px solid #ebeef5;
    }
    .el-table__row:hover {
      background-color: #f5f7fa;
    }
  }

  /* Kiểu nút bảng */
  .el-button--text {
    color: #7079aa;
  }

  .el-button--text:hover {
    color: #5a64b5;
  }

  /* Kiểu văn bản ô */
  .cell {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
}

/* Thanh tác vụ ở cuối bảng */
.table_bottom {
  display: flex;
  justify-content: space-between !important;
  align-items: center;
  margin-top: auto;
  padding: 0 20px !important;
  width: 100% !important;
  box-sizing: border-box !important;
}

/* Kiểu nút điều khiển */
.ctrl_btn {
  display: flex;
  gap: 8px;
  padding-left: 0 !important;
  margin-left: 0 !important;

  .el-button {
    min-width: 72px;
    height: 32px;
    padding: 7px 12px 7px 10px;
    font-size: 12px;
    border-radius: 4px;
    line-height: 1;
    font-weight: 500;
    border: none;
    transition: all 0.3s ease;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);

    &:hover {
      transform: translateY(-1px);
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    }
  }

  .el-button--primary {
    background: #5f70f3;
    color: white;
  }
  .el-button--success {
    background: #5bc98c;
    color: white;
  }
  .el-button--danger {
    background: #fd5b63;
    color: white;
  }
}
</style>
