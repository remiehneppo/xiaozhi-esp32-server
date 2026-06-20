-- Thêm nhà cung cấp và cấu hình mô hình RAG
-- -------------------------------------------------------

-- Thêm nhà cung cấp mô hình RAG
delete from `ai_model_provider` where id = 'SYSTEM_RAG_ragflow';
INSERT INTO `ai_model_provider` (`id`, `model_type`, `provider_code`, `name`, `fields`, `sort`, `creator`, `create_date`, `updater`, `update_date`) VALUES
('SYSTEM_RAG_ragflow', 'RAG', 'ragflow', 'RAGFlow', '[{"key": "base_url", "type": "string", "label": "Địa chỉ dịch vụ"}, {"key": "api_key", "type": "string", "label": "APIchìa khóa"}]', 1, 1, NOW(), 1, NOW());

-- Thêm cấu hình mô hình RAG
delete from `ai_model_config` where id = 'RAG_RAGFlow';
INSERT INTO `ai_model_config` VALUES ('RAG_RAGFlow', 'RAG', 'ragflow', 'RAGFlow', 1, 1, '{"type": "ragflow", "base_url": "http://localhost", "api_key": "của bạnRAGchìa khóa"}', 'https://github.com/infiniflow/ragflow/blob/main/README_zh.md', 'RAGFlowHướng dẫn cấu hình：
một、Hướng dẫn triển khai nhanh（dockertriển khai）
1.$ sysctl vm.max_map_count
2.$ sysctl -w vm.max_map_count=262144
3.$ git clone https://github.com/infiniflow/ragflow.git
4.docker compose -f docker-compose.yml up -d
5.$ docker logs -f docker-ragflow-cpu-1
6.Sau khi đăng ký và đăng nhập，Bấm vào avatar ở góc trên bên phải，nhận đượcRAGFlowcủaAPI KEYvàAPIĐịa chỉ máy chủ。sử dụngRAGFlowXin vui lòng đến trướcModel ProviderThêm mô hình và đặt mô hình mặc định trong。
hai、Nếu bạn muốn tắt chức năng đăng ký
1.Dừng dịch vụ   docker compose down
2. sed -i ''s/REGISTER_ENABLED=1/REGISTER_ENABLED=0/g'' .env   
3.cat .env | grep -i register
4.xemREGISTER_ENABLED=0 Chỉ cần khởi động lại dịch vụ。',  1, NULL, NULL, NULL, NULL);

