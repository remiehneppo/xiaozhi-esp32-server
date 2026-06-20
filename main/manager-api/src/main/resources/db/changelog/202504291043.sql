-- Đã thêm nhà cung cấp và cấu hình mô hình nhận dạng giọng nói dịch vụ FunASR
DELETE FROM `ai_model_provider` WHERE `id` = 'SYSTEM_ASR_FunASRServer';
INSERT INTO `ai_model_provider` (`id`, `model_type`, `provider_code`, `name`, `fields`, `sort`, `creator`, `create_date`, `updater`, `update_date`) VALUES
('SYSTEM_ASR_FunASRServer', 'ASR', 'fun_server', 'FunASRDịch vụ nhận dạng giọng nói', '[{"key":"host","label":"Địa chỉ dịch vụ","type":"string"},{"key":"port","label":"số cổng","type":"number"}]', 4, 1, NOW(), 1, NOW());

DELETE FROM `ai_model_config` WHERE `id` = 'ASR_FunASRServer';
INSERT INTO `ai_model_config` VALUES ('ASR_FunASRServer', 'ASR', 'FunASRServer', 'FunASRDịch vụ nhận dạng giọng nói', 0, 1, '{\"type\": \"fun_server\", \"host\": \"127.0.0.1\", \"port\": 10096}', NULL, NULL, 5, NULL, NULL, NULL, NULL);

-- Sửa đổi loại trường nhận xét của bảng ai_model_config thành TEXT
ALTER TABLE `ai_model_config` MODIFY COLUMN `remark` TEXT COMMENT 'Bình luận'; 

-- Tài liệu cập nhật về cấu hình mô hình ASR
UPDATE `ai_model_config` SET 
`doc_link` = 'https://github.com/modelscope/FunASR/blob/main/runtime/docs/SDK_advanced_guide_online_zh.md',
`remark` = 'Triển khai độc lậpFunASR，sử dụngFunASRcủaAPIdịch vụ，Chỉ cần năm câu
câu đầu tiên：mkdir -p ./funasr-runtime-resources/models
câu thứ hai：sudo docker run -d -p 10096:10095 --privileged=true -v $PWD/funasr-runtime-resources/models:/workspace/models registry.cn-hangzhou.aliyuncs.com/funasr_repo/funasr:funasr-runtime-sdk-online-cpu-0.1.12
Sau khi câu trước được thực thi sẽ vào container，Tiếp tục đến câu thứ ba：cd FunASR/runtime
Không thoát khỏi container，Tiếp tục thực hiện câu thứ 4 trong container：nohup bash run_server_2pass.sh --download-model-dir /workspace/models --vad-dir damo/speech_fsmn_vad_zh-cn-16k-common-onnx --model-dir damo/speech_paraformer-large-vad-punc_asr_nat-zh-cn-16k-common-vocab8404-onnx  --online-model-dir damo/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-online-onnx  --punc-dir damo/punc_ct-transformer_zh-cn-common-vad_realtime-vocab272727-onnx --lm-dir damo/speech_ngram_lm_zh-cn-ai-wesp-fst --itn-dir thuduj12/fst_itn_zh --hotword /workspace/models/hotwords.txt > log.txt 2>&1 &
Sau khi câu trước được thực thi sẽ vào container，Tiếp tục đến câu thứ năm：tail -f log.txt
Sau khi câu thứ năm được thi hành，Bạn sẽ thấy nhật ký tải xuống mô hình，Sau khi tải về bạn có thể kết nối và sử dụng
Ở trên được sử dụngCPUlý luận，nếu cóGPU，Tham khảo chi tiết：https://github.com/modelscope/FunASR/blob/main/runtime/docs/SDK_advanced_guide_online_zh.md' WHERE `id` = 'ASR_FunASRServer';

-- Đã cập nhật hướng dẫn cấu hình mô hình cục bộ FunASR
UPDATE `ai_model_config` SET 
`doc_link` = 'https://github.com/modelscope/FunASR',
`remark` = 'FunASRmô hình địa phươngMô tả cấu hình:
1. Bạn cần tải file mô hình vềxiaozhi-server/models/SenseVoiceSmallThư mục
2. Hỗ trợ nhận dạng giọng nói tiếng Trung, tiếng Nhật, tiếng Hàn và tiếng Quảng Đông
3. Suy luận cục bộ, không cần kết nối mạng
4. Các tập tin được nhận dạng được lưu trữ trongtmp/Thư mục' WHERE `id` = 'ASR_FunASR';

-- Hướng dẫn cấu hình SherpaASR được cập nhật
UPDATE `ai_model_config` SET 
`doc_link` = 'https://github.com/k2-fsa/sherpa-onnx',
`remark` = 'SherpaASRMô tả cấu hình:
1. Tự động tải các tập tin mô hình vềmodels/sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2024-07-17Thư mục
2. Hỗ trợ tiếng Trung、Tiếng Anh、tiếng Nhật、Tiếng Hàn、Tiếng Quảng Đông và các ngôn ngữ khác
3. Suy luận cục bộ, không cần kết nối mạng
4. Tệp đầu ra được lưu trongtmp/Thư mục' WHERE `id` = 'ASR_SherpaASR';

-- Đã cập nhật hướng dẫn cấu hình Doubao ASR
UPDATE `ai_model_config` SET 
`doc_link` = 'https://console.volcengine.com/speech/app',
`remark` = 'túi đậuASRMô tả cấu hình:
1. Bạn cần tạo một ứng dụng trong bảng điều khiển Volcano Engine và lấyappidvàaccess_token
2. Hỗ trợ nhận dạng giọng nói tiếng Trung
3. Cần có kết nối Internet
4. Tệp đầu ra được lưu trongtmp/Thư mục
Các bước ứng dụng：
1. chuyến thăm https://console.volcengine.com/speech/app
2. Tạo ứng dụng mới
3. nhận đượcappidvàaccess_token
4. Điền vào tệp cấu hình' WHERE `id` = 'ASR_DoubaoASR';

-- Đã cập nhật hướng dẫn cấu hình Tencent ASR
UPDATE `ai_model_config` SET 
`doc_link` = 'https://console.cloud.tencent.com/cam/capi',
`remark` = 'TencentASRMô tả cấu hình:
1. Bạn cần tạo một ứng dụng trong bảng điều khiển Tencent Cloud và tải xuốngappid、secret_idvàsecret_key
2. Hỗ trợ nhận dạng giọng nói tiếng Trung
3. Cần có kết nối Internet
4. Tệp đầu ra được lưu trongtmp/Thư mục
Các bước ứng dụng：
1. chuyến thăm https://console.cloud.tencent.com/cam/capi Nhận chìa khóa
2. chuyến thăm https://console.cloud.tencent.com/asr/resourcebundle Nhận tài nguyên miễn phí
3. nhận đượcappid、secret_idvàsecret_key
4. Điền vào tệp cấu hình' WHERE `id` = 'ASR_TencentASR';

-- Hướng dẫn cấu hình mô hình TTS được cập nhật
-- Hướng dẫn cấu hình EdgeTTS
UPDATE `ai_model_config` SET 
`doc_link` = 'https://github.com/rany2/edge-tts',
`remark` = 'EdgeTTSMô tả cấu hình:
1. Sử dụng MicrosoftEdge TTSdịch vụ
2. Hỗ trợ nhiều ngôn ngữ và âm sắc
3. miễn phí sử dụng，Không cần đăng ký
4. Cần có kết nối Internet
5. Tệp đầu ra được lưu trongtmp/Thư mục' WHERE `id` = 'TTS_EdgeTTS';

-- Hướng dẫn cấu hình Doubao TTS
UPDATE `ai_model_config` SET 
`doc_link` = 'https://console.volcengine.com/speech/service/8',
`remark` = 'túi đậuTTSMô tả cấu hình:
1. chuyến thăm https://console.volcengine.com/speech/service/8
2. Bạn cần tạo một ứng dụng trong bảng điều khiển Volcano Engine và lấyappidvàaccess_token
3. Tiếng động cơ miền núi phải mua và bỏ tiền，Giá khởi điểm30Nhân dân tệ，có100Đồng thời。Nếu bạn chỉ sử dụng cái miễn phí2đồng thời，Sẽ report thường xuyênttsLỗi
4. Sau khi mua dịch vụ，Sau khi mua bản vá miễn phí，Có thể mất khoảng nửa giờ，có thể được sử dụng。
5. Điền vào tệp cấu hình' WHERE `id` = 'TTS_DoubaoTTS';

-- Hướng dẫn cấu hình TTS dòng chảy dựa trên silicon
UPDATE `ai_model_config` SET 
`doc_link` = 'https://cloud.siliconflow.cn/account/ak',
`remark` = 'dòng chảy dựa trên siliconTTSMô tả cấu hình:
1. chuyến thăm https://cloud.siliconflow.cn/account/ak
2. Đăng ký vàLấy khóa API
3. Điền vào tệp cấu hình' WHERE `id` = 'TTS_CosyVoiceSiliconflow';

-- Hướng dẫn cấu hình TTS tiếng Trung Coze
UPDATE `ai_model_config` SET 
`doc_link` = 'https://www.coze.cn/open/oauth/pats',
`remark` = 'CozeTiếng TrungTTSMô tả cấu hình:
1. chuyến thăm https://www.coze.cn/open/oauth/pats
2. Nhận token cá nhân
3. Điền vào tệp cấu hình' WHERE `id` = 'TTS_CozeCnTTS';

-- Hướng dẫn cấu hình FishSpeech
UPDATE `ai_model_config` SET 
`doc_link` = 'https://github.com/fishaudio/fish-speech',
`remark` = 'FishSpeechMô tả cấu hình:
1. Yêu cầu triển khai cục bộFishSpeechdịch vụ
2. Hỗ trợ âm thanh tùy chỉnh
3. Suy luận cục bộ, không cần kết nối mạng
4. Tệp đầu ra được lưu trongtmp/Thư mục
5. Chạy lệnh ví dụ dịch vụ：python -m tools.api_server --listen 0.0.0.0:8080 --llama-checkpoint-path "checkpoints/fish-speech-1.5" --decoder-checkpoint-path "checkpoints/fish-speech-1.5/firefly-gan-vq-fsq-8x1024-21hz-generator.pth" --decoder-config-name firefly_gan_vq --compile' WHERE `id` = 'TTS_FishSpeech';

-- Hướng dẫn cấu hình GPT-SoVITS V2
UPDATE `ai_model_config` SET 
`doc_link` = 'https://github.com/RVC-Boss/GPT-SoVITS',
`remark` = 'GPT-SoVITS V2Mô tả cấu hình:
1. Yêu cầu triển khai cục bộGPT-SoVITSdịch vụ
2. Hỗ trợ nhân bản giai điệu tùy chỉnh
3. Suy luận cục bộ, không cần kết nối mạng
4. Tệp đầu ra được lưu trongtmp/Thư mục
Các bước triển khai：
1. Chạy lệnh ví dụ dịch vụ：python api_v2.py -a 127.0.0.1 -p 9880 -c GPT_SoVITS/configs/demo.yaml' WHERE `id` = 'TTS_GPT_SOVITS_V2';

-- Hướng dẫn cấu hình GPT-SoVITS V3
UPDATE `ai_model_config` SET 
`doc_link` = 'https://github.com/RVC-Boss/GPT-SoVITS',
`remark` = 'GPT-SoVITS V3Mô tả cấu hình:
1. Yêu cầu triển khai cục bộGPT-SoVITS V3dịch vụ
2. Hỗ trợ nhân bản giai điệu tùy chỉnh
3. Suy luận cục bộ, không cần kết nối mạng
4. Tệp đầu ra được lưu trongtmp/Thư mục' WHERE `id` = 'TTS_GPT_SOVITS_V3';

-- Hướng dẫn cấu hình MiniMax TTS
UPDATE `ai_model_config` SET 
`doc_link` = 'https://platform.minimaxi.com/',
`remark` = 'MiniMax TTSMô tả cấu hình:
1. cần phải ở trongMiniMaxTạo một tài khoản trên nền tảng và nạp tiền
2. Hỗ trợ nhiều âm sắc，Cấu hình hiện tại sử dụngfemale-shaonv
3. Cần có kết nối Internet
4. Tệp đầu ra được lưu trongtmp/Thư mục
Các bước ứng dụng：
1. chuyến thăm https://platform.minimaxi.com/ Đăng ký tài khoản
2. chuyến thăm https://platform.minimaxi.com/user-center/payment/balance nạp tiền
3. chuyến thăm https://platform.minimaxi.com/user-center/basic-information nhận đượcgroup_id
4. chuyến thăm https://platform.minimaxi.com/user-center/basic-information/interface-key nhận đượcapi_key
5. Điền vào tệp cấu hình' WHERE `id` = 'TTS_MinimaxTTS';

-- Hướng dẫn cấu hình Alibaba Cloud TTS
UPDATE `ai_model_config` SET 
`doc_link` = 'https://nls-portal.console.aliyun.com/',
`remark` = 'Đám mây của AlibabaTTSMô tả cấu hình:
1. Cần kích hoạt dịch vụ tương tác giọng nói thông minh trên nền tảng Alibaba Cloud
2. Hỗ trợ nhiều âm sắc，Cấu hình hiện tại sử dụngxiaoyun
3. Cần có kết nối Internet
4. Tệp đầu ra được lưu trongtmp/Thư mục
Các bước ứng dụng：
1. chuyến thăm https://nls-portal.console.aliyun.com/ Kích hoạt dịch vụ
2. chuyến thăm https://nls-portal.console.aliyun.com/applist nhận đượcappkey
3. chuyến thăm https://nls-portal.console.aliyun.com/overview nhận đượctoken
4. Điền vào tệp cấu hình
Lưu ý：tokenlà tạm thời24Có giá trị trong giờ，Sử dụng lâu dài cần cấu hìnhaccess_key_idvàaccess_key_secret' WHERE `id` = 'TTS_AliyunTTS';

-- Hướng dẫn cấu hình Tencent TTS
UPDATE `ai_model_config` SET 
`doc_link` = 'https://console.cloud.tencent.com/cam/capi',
`remark` = 'TencentTTSMô tả cấu hình:
1. Cần kích hoạt dịch vụ tương tác giọng nói thông minh trên nền tảng Tencent Cloud
2. Hỗ trợ nhiều âm sắc，Cấu hình hiện tại sử dụng101001
3. Cần có kết nối Internet
4. Tệp đầu ra được lưu trongtmp/Thư mục
Các bước ứng dụng：
1. chuyến thăm https://console.cloud.tencent.com/cam/capi Nhận chìa khóa
2. chuyến thăm https://console.cloud.tencent.com/tts/resourcebundle Nhận tài nguyên miễn phí
3. Tạo ứng dụng mới
4. nhận đượcappid、secret_idvàsecret_key
5. Điền vào tệp cấu hình' WHERE `id` = 'TTS_TencentTTS';

-- Hướng dẫn cấu hình 302AI TTS
UPDATE `ai_model_config` SET 
`doc_link` = 'https://dash.302.ai/',
`remark` = '302AI TTSMô tả cấu hình:
1. cần phải ở trong302Tạo một tài khoản trên nền tảng vàLấy khóa API
2. Hỗ trợ nhiều âm sắc，Cấu hình hiện tại sử dụng âm sắc Wanwan Xiaohe.
3. Cần có kết nối Internet
4. Tệp đầu ra được lưu trongtmp/Thư mục
Các bước ứng dụng：
1. chuyến thăm https://dash.302.ai/ Đăng ký tài khoản
2. chuyến thăm https://dash.302.ai/apis/list Lấy khóa API
3. Điền vào tệp cấu hình
giá cả：$35/triệu ký tự' WHERE `id` = 'TTS_TTS302AI';

-- Hướng dẫn cấu hình Gizwits TTS
UPDATE `ai_model_config` SET 
`doc_link` = 'https://agentrouter.gizwitsapi.com/panel/token',
`remark` = 'Đám mây trí tuệTTSMô tả cấu hình:
1. Bắt buộc trên Nền tảng đám mây GizwitsLấy khóa API
2. Hỗ trợ nhiều âm sắc，Cấu hình hiện tại sử dụng âm sắc Wanwan Xiaohe.
3. Cần có kết nối Internet
4. Tệp đầu ra được lưu trongtmp/Thư mục
Các bước ứng dụng：
1. chuyến thăm https://agentrouter.gizwitsapi.com/panel/token Lấy khóa API
2. Điền vào tệp cấu hình
Lưu ý：10.000 người dùng đăng ký đầu tiên，Sẽ gửi5Số tiền kinh nghiệm nhân dân tệ' WHERE `id` = 'TTS_GizwitsTTS';

-- Hướng dẫn cấu hình ACGN TTS
UPDATE `ai_model_config` SET 
`doc_link` = 'https://acgn.ttson.cn/',
`remark` = 'ACGN TTSMô tả cấu hình:
1. cần phải ở trongttsonMua nền tảngtoken
2. Hỗ trợ nhiều âm thanh ký tự，Cấu hình hiện tại sử dụng vai tròID：1695
3. Cần có kết nối Internet
4. Tệp đầu ra được lưu trongtmp/Thư mục
Các bước ứng dụng：
1. chuyến thăm https://acgn.ttson.cn/ Xem danh sách vai trò
2. chuyến thăm www.ttson.cn muatoken
3. Điền vào tệp cấu hình
Các câu hỏi liên quan đến phát triển phải được gửi tớiqq' WHERE `id` = 'TTS_ACGNTTS';

-- Hướng dẫn cấu hình OpenAI TTS
UPDATE `ai_model_config` SET 
`doc_link` = 'https://platform.openai.com/api-keys',
`remark` = 'OpenAI TTSMô tả cấu hình:
1. cần phải ở trongOpenAInền tảngLấy khóa API
2. Hỗ trợ nhiều âm sắc，Cấu hình hiện tại sử dụngonyx
3. Cần có kết nối Internet
4. Tệp đầu ra được lưu trongtmp/Thư mục
Các bước ứng dụng：
1. chuyến thăm https://platform.openai.com/api-keys Lấy khóa API
2. Điền vào tệp cấu hình
Lưu ý：Trong nước có nhu cầu sử dụng proxy truy cập' WHERE `id` = 'TTS_OpenAITTS';

-- Hướng dẫn cấu hình TTS tùy chỉnh
UPDATE `ai_model_config` SET 
`doc_link` = NULL,
`remark` = 'Tùy chỉnhTTSMô tả cấu hình:
1. Hỗ trợ tùy chỉnhTTSDịch vụ giao diện
2. sử dụngGETyêu cầu phương pháp
3. Cần có kết nối Internet
4. Tệp đầu ra được lưu trongtmp/Thư mục
Mô tả cấu hình:
1. trongparamsCấu hình các tham số yêu cầu trong
2. trongheadersĐịnh cấu hình tiêu đề yêu cầu trong
3. Đặt định dạng âm thanh trả về' WHERE `id` = 'TTS_CustomTTS';

-- Hướng dẫn cấu hình TTS của Volcano Engine Edge Cổng mô hình lớn
UPDATE `ai_model_config` SET 
`doc_link` = 'https://console.volcengine.com/vei/aigateway/',
`remark` = 'Cổng mô hình lớn cạnh động cơ núi lửaTTSMô tả cấu hình:
1. chuyến thăm https://console.volcengine.com/vei/aigateway/
2. Tạo khóa truy cập cổng，Tìm kiếm và kiểm tra Doubao-tổng hợp giọng nói
3. Nếu cần sử dụngLLM，Kiểm tra cả hai Doubao-pro-32k-functioncall
4. chuyến thăm https://console.volcengine.com/vei/aigateway/tokens-list Nhận chìa khóa
5. Điền vào tệp cấu hình
Tham khảo danh sách giọng nói：https://www.volcengine.com/docs/6561/1257544' WHERE `id` = 'TTS_VolcesAiGatewayTTS';

-- Hướng dẫn cấu hình mô hình LLM được cập nhật
-- Hướng dẫn cấu hình ChatGLM
UPDATE `ai_model_config` SET 
`doc_link` = 'https://bigmodel.cn/usercenter/proj-mgmt/apikeys',
`remark` = 'ChatGLMMô tả cấu hình:
1. chuyến thăm https://bigmodel.cn/usercenter/proj-mgmt/apikeys
2. Đăng ký vàLấy khóa API
3. Điền vào tệp cấu hình' WHERE `id` = 'LLM_ChatGLMLLM';

-- Hướng dẫn cấu hình Ollama
UPDATE `ai_model_config` SET 
`doc_link` = 'https://ollama.com/',
`remark` = 'OllamaMô tả cấu hình:
1. Cài đặtOllamadịch vụ
2. Chạy lệnh：ollama pull qwen2.5
3. Đảm bảo dịch vụ đang chạyhttp://localhost:11434' WHERE `id` = 'LLM_OllamaLLM';

-- Hướng dẫn cấu hình Tongyi Qianwen
UPDATE `ai_model_config` SET 
`doc_link` = 'https://bailian.console.aliyun.com/?apiKey=1#/api-key',
`remark` = 'Tongyi QianwenMô tả cấu hình:
1. chuyến thăm https://bailian.console.aliyun.com/?apiKey=1#/api-key
2. Lấy khóa API
3. Điền vào tệp cấu hình，Cấu hình hiện tại sử dụngqwen-turbongười mẫu
4. Hỗ trợ các thông số tùy chỉnh：temperature=0.7, max_tokens=500, top_p=1, top_k=50' WHERE `id` = 'LLM_AliLLM';

-- Hướng dẫn cấu hình Tongyi Bailian
UPDATE `ai_model_config` SET 
`doc_link` = 'https://bailian.console.aliyun.com/?apiKey=1#/api-key',
`remark` = 'Tongyi BailianMô tả cấu hình:
1. chuyến thăm https://bailian.console.aliyun.com/?apiKey=1#/api-key
2. nhận đượcapp_idvàapi_key
3. Điền vào tệp cấu hình' WHERE `id` = 'LLM_AliAppLLM';

-- Hướng dẫn cấu hình mô hình túi đậu lớn
UPDATE `ai_model_config` SET 
`doc_link` = 'https://console.volcengine.com/ark/region:ark+cn-beijing/openManagement',
`remark` = 'Mẫu túi đậuMô tả cấu hình:
1. chuyến thăm https://console.volcengine.com/ark/region:ark+cn-beijing/openManagement
2. MởDoubao-1.5-prodịch vụ
3. chuyến thăm https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey Lấy khóa API
4. Điền vào tệp cấu hình
5. Hiện được đề xuấtdoubao-1-5-pro-32k-250115
Lưu ý：Có một hạn ngạch miễn phí500000token' WHERE `id` = 'LLM_DoubaoLLM';

-- Hướng dẫn cấu hình DeepSeek
UPDATE `ai_model_config` SET 
`doc_link` = 'https://platform.deepseek.com/',
`remark` = 'DeepSeekMô tả cấu hình:
1. chuyến thăm https://platform.deepseek.com/
2. Đăng ký vàLấy khóa API
3. Điền vào tệp cấu hình' WHERE `id` = 'LLM_DeepSeekLLM';

-- Hướng dẫn cấu hình Dify
UPDATE `ai_model_config` SET 
`doc_link` = 'https://cloud.dify.ai/',
`remark` = 'DifyMô tả cấu hình:
1. chuyến thăm https://cloud.dify.ai/
2. Đăng ký vàLấy khóa API
3. Điền vào tệp cấu hình
4. Hỗ trợ nhiều chế độ hội thoại：workflows/run, chat-messages, completion-messages
5. Định nghĩa vai trò do nền tảng đặt sẽ không hợp lệ，cần phải ở trongDifyCài đặt bảng điều khiển
Lưu ý：Nên sử dụng triển khai cục bộDifygiao diện，Quyền truy cập vào giao diện đám mây công cộng có thể bị hạn chế ở một số khu vực của đất nước.' WHERE `id` = 'LLM_DifyLLM';

-- Hướng dẫn cấu hình Gemini
UPDATE `ai_model_config` SET 
`doc_link` = 'https://aistudio.google.com/apikey',
`remark` = 'GeminiMô tả cấu hình:
1. sử dụng googleGemini APIdịch vụ
2. Cấu hình hiện tại sử dụnggemini-2.0-flashngười mẫu
3. Cần có kết nối Internet
4. Hỗ trợ proxy cấu hình
Các bước ứng dụng：
1. chuyến thăm https://aistudio.google.com/apikey
2. tạo raAPIchìa khóa
3. Điền vào tệp cấu hình
Lưu ý：Nếu được sử dụng ở Trung Quốc，vui lòng tuân thủ《Các biện pháp tạm thời để quản lý dịch vụ trí tuệ nhân tạo sáng tạo》' WHERE `id` = 'LLM_GeminiLLM';

-- Hướng dẫn cấu hình Coze
UPDATE `ai_model_config` SET 
`doc_link` = 'https://www.coze.cn/open/oauth/pats',
`remark` = 'CozeMô tả cấu hình:
1. sử dụngCozeDịch vụ nền tảng
2. cầnbot_id、user_idvà token cá nhân
3. Cần có kết nối Internet
Các bước ứng dụng：
1. chuyến thăm https://www.coze.cn/open/oauth/pats
2. Nhận token cá nhân
3. Tính toán thủ côngbot_idvàuser_id
4. Điền vào tệp cấu hình' WHERE `id` = 'LLM_CozeLLM';

-- Hướng dẫn cấu hình LM Studio
UPDATE `ai_model_config` SET 
`doc_link` = 'https://lmstudio.ai/',
`remark` = 'LM StudioMô tả cấu hình:
1. Sử dụng được triển khai cục bộLM Studiodịch vụ
2. Cấu hình hiện tại sử dụngdeepseek-r1-distill-llama-8b@q4_k_mngười mẫu
3. Suy luận cục bộ, không cần kết nối mạng
4. Cần tải xuống mô hình trước
Các bước triển khai：
1. Cài đặtLM Studio
2. Tải xuống các mô hình từ cộng đồng
3. Đảm bảo dịch vụ đang chạyhttp://localhost:1234/v1' WHERE `id` = 'LLM_LMStudioLLM';

-- Hướng dẫn cấu hình FastGPT
UPDATE `ai_model_config` SET 
`doc_link` = 'https://cloud.tryfastgpt.ai/account/apikey',
`remark` = 'FastGPTMô tả cấu hình:
1. sử dụngFastGPTDịch vụ nền tảng
2. Cần có kết nối Internet
3. trong tập tin cấu hìnhpromptkhông hợp lệ，cần phải ở trongFastGPTCài đặt bảng điều khiển
4. Hỗ trợ các biến tùy chỉnh
Các bước ứng dụng：
1. chuyến thăm https://cloud.tryfastgpt.ai/account/apikey
2. Lấy khóa API
3. Điền vào tệp cấu hình' WHERE `id` = 'LLM_FastgptLLM';

-- Hướng dẫn cấu hình Xinference
UPDATE `ai_model_config` SET 
`doc_link` = 'https://github.com/xorbitsai/inference',
`remark` = 'XinferenceMô tả cấu hình:
1. Sử dụng được triển khai cục bộXinferencedịch vụ
2. Cấu hình hiện tại sử dụngqwen2.5:72b-AWQngười mẫu
3. Suy luận cục bộ, không cần kết nối mạng
4. Mô hình tương ứng cần phải được bắt đầu trước
Các bước triển khai：
1. Cài đặtXinference
2. Bắt đầu dịch vụ và tải mô hình
3. Đảm bảo dịch vụ đang chạyhttp://localhost:9997' WHERE `id` = 'LLM_XinferenceLLM';

-- Hướng dẫn cấu hình mô hình nhỏ Xinference
UPDATE `ai_model_config` SET 
`doc_link` = 'https://github.com/xorbitsai/inference',
`remark` = 'Xinferencemô hình nhỏMô tả cấu hình:
1. Sử dụng được triển khai cục bộXinferencedịch vụ
2. Cấu hình hiện tại sử dụngqwen2.5:3b-AWQngười mẫu
3. Suy luận cục bộ, không cần kết nối mạng
4. để nhận biết ý định
Các bước triển khai：
1. Cài đặtXinference
2. Bắt đầu dịch vụ và tải mô hình
3. Đảm bảo dịch vụ đang chạyhttp://localhost:9997' WHERE `id` = 'LLM_XinferenceSmallLLM';

-- Hướng dẫn cấu hình LLM cổng động cơ Volcano Engine Edge
UPDATE `ai_model_config` SET 
`doc_link` = 'https://console.volcengine.com/vei/aigateway/',
`remark` = 'Cổng mô hình lớn cạnh động cơ núi lửaLLMMô tả cấu hình:
1. Sử dụng Dịch vụ Cổng mô hình lớn Volcano Engine Edge
2. Cần có khóa truy cập cổng
3. Cần có kết nối Internet
4. hỗ trợfunction_callchức năng
Các bước ứng dụng：
1. chuyến thăm https://console.volcengine.com/vei/aigateway/
2. Tạo khóa truy cập cổng，Tìm kiếm và kiểm tra Doubao-pro-32k-functioncall
3. Nếu bạn cần sử dụng tổng hợp giọng nói，Kiểm tra cả hai Doubao-tổng hợp giọng nói
4. chuyến thăm https://console.volcengine.com/vei/aigateway/tokens-list Nhận chìa khóa
5. Điền vào tệp cấu hình' WHERE `id` = 'LLM_VolcesAiGatewayLLM';

-- Cập nhật hướng dẫn cấu hình mô hình bộ nhớ
-- Hướng dẫn cấu hình không cần bộ nhớ
UPDATE `ai_model_config` SET 
`doc_link` = NULL,
`remark` = 'không có trí nhớMô tả cấu hình:
1. Không lưu lịch sử cuộc trò chuyện
2. Mỗi cuộc trò chuyện là độc lập
3. Không cần cấu hình bổ sung
4. Thích hợp cho những cảnh có yêu cầu riêng tư cao' WHERE `id` = 'Memory_nomem';

-- Hướng dẫn cấu hình bộ nhớ ngắn hạn cục bộ
UPDATE `ai_model_config` SET 
`doc_link` = NULL,
`remark` = 'trí nhớ ngắn hạn cục bộMô tả cấu hình:
1. Lưu lịch sử cuộc trò chuyện bằng bộ nhớ cục bộ
2. Vượt quaselected_modulecủallmTóm tắt cuộc trò chuyện
3. Dữ liệu được lưu cục bộ，Sẽ không được tải lên máy chủ
4. Thích hợp cho các tình huống quan tâm đến quyền riêng tư
5. Không cần cấu hình bổ sung' WHERE `id` = 'Memory_mem_local_short';

-- Hướng dẫn cấu hình bộ nhớ Mem0AI
UPDATE `ai_model_config` SET 
`doc_link` = 'https://app.mem0.ai/dashboard/api-keys',
`remark` = 'Mem0AIký ứcMô tả cấu hình:
1. sử dụngMem0AIDịch vụ lưu lịch sử hội thoại
2. cầnAPIchìa khóa
3. Cần có kết nối Internet
4. mỗi tháng1000cuộc gọi miễn phí
Các bước ứng dụng：
1. Truy cập https://app.mem0.ai/dashboard/api-keys
2. Lấy khóa API
3. Điền vào tệp cấu hình' WHERE `id` = 'Memory_mem0ai';

-- Cập nhật mô tả cấu hình mô hình Intent
-- Không có hướng dẫn cấu hình nhận dạng ý định
UPDATE `ai_model_config` SET 
`doc_link` = NULL,
`remark` = 'Mô tả cấu hình không nhận diện ý định:
1. Không thực hiện nhận diện ý định
2. Tất cả các cuộc hội thoại được chuyển trực tiếp cho LLM xử lý
3. Không cần cấu hình bổ sung
4. Phù hợp cho các kịch bản hội thoại đơn giản' WHERE `id` = 'Intent_nointent';

-- Hướng dẫn cấu hình nhận dạng ý định LLM
UPDATE `ai_model_config` SET 
`doc_link` = NULL,
`remark` = 'Mô tả cấu hình nhận diện ý định bằng LLM:
1. Sử dụng LLM riêng biệt để nhận diện ý định
2. Mặc định sử dụng mô hình của selected_module.LLM
3. Có thể cấu hình sử dụng LLM riêng biệt (như ChatGLMLLM miễn phí)
4. Tính phổ biến cao, nhưng sẽ làm tăng thời gian xử lý
5. Không hỗ trợ các thao tác IoT như điều khiển âm lượng
Mô tả cấu hình:
1. Chỉ định mô hình LLM được sử dụng trong trường llm
2. Nếu không chỉ định, sẽ sử dụng mô hình của selected_module.LLM' WHERE `id` = 'Intent_intent_llm';

-- Hướng dẫn cấu hình nhận dạng mục đích cuộc gọi chức năng
UPDATE `ai_model_config` SET 
`doc_link` = NULL,
`remark` = 'Nhận dạng ý định cuộc gọi chức năngMô tả cấu hình:
1. Sử dụng tính năng function_call của LLM để nhận diện ý định
2. Cần mô hình LLM được chọn hỗ trợ function_call
3. Gọi công cụ theo nhu cầu, tốc độ xử lý nhanh
4. Hỗ trợ tất cả các lệnh IoT
5. Các chức năng sau đã được tải mặc định:
   - handle_exit_intent (nhận diện thoát)
   - play_music (phát nhạc)
   - change_role (chuyển đổi vai trò)
   - get_weather (tra cứu thời tiết)
   - get_news (tra cứu tin tức)
Mô tả cấu hình:
1. Cấu hình các mô-đun chức năng cần tải trong trường functions
2. Hệ thống đã tải các chức năng cơ bản mặc định, không cần cấu hình lặp lại
3. Có thể thêm các mô-đun chức năng tùy chỉnh' WHERE `id` = 'Intent_function_call';

-- Cập nhật mô tả cấu hình mô hình VAD
-- Hướng dẫn cấu hình SileroVAD
UPDATE `ai_model_config` SET 
`doc_link` = 'https://github.com/snakers4/silero-vad',
`remark` = 'SileroVADMô tả cấu hình:
1. Sử dụng mô hình SileroVAD để phát hiện hoạt động giọng nói
2. Suy luận cục bộ, không cần kết nối mạng
3. Cần tải xuống tệp mô hình vào thư mục models/snakers4_silero-vad
4. Các tham số có thể cấu hình:
   - threshold: 0.5 (ngưỡng phát hiện giọng nói)
   - min_silence_duration_ms: 700 (thời gian im lặng tối thiểu, đơn vị miligiây)
5. Nếu việc tạm dừng nói khá dài, có thể tăng giá trị min_silence_duration_ms một cách thích hợp' WHERE `id` = 'VAD_SileroVAD';
