-- Thay đổi mô hình tài liệu FunASRServer thành SenseVoiceSmall
UPDATE `ai_model_config` SET 
`doc_link` = 'https://github.com/modelscope/FunASR/blob/main/runtime/docs/SDK_advanced_guide_online_zh.md',
`remark` = 'Triển khai độc lậpFunASR，sử dụngFunASRcủaAPIdịch vụ，Chỉ cần năm câu
câu đầu tiên：mkdir -p ./funasr-runtime-resources/models
câu thứ hai：sudo docker run -d -p 10096:10095 --privileged=true -v $PWD/funasr-runtime-resources/models:/workspace/models registry.cn-hangzhou.aliyuncs.com/funasr_repo/funasr:funasr-runtime-sdk-online-cpu-0.1.12
Sau khi câu trước được thực thi sẽ vào container，Tiếp tục đến câu thứ ba：cd FunASR/runtime
Không thoát khỏi container，Tiếp tục thực hiện câu thứ 4 trong container：nohup bash run_server_2pass.sh --download-model-dir /workspace/models --vad-dir damo/speech_fsmn_vad_zh-cn-16k-common-onnx --model-dir iic/SenseVoiceSmall-onnx  --online-model-dir damo/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-online-onnx  --punc-dir damo/punc_ct-transformer_zh-cn-common-vad_realtime-vocab272727-onnx --lm-dir damo/speech_ngram_lm_zh-cn-ai-wesp-fst --itn-dir thuduj12/fst_itn_zh --hotword /workspace/models/hotwords.txt > log.txt 2>&1 &
Sau khi câu trước được thực thi sẽ vào container，Tiếp tục đến câu thứ năm：tail -f log.txt
Sau khi câu thứ năm được thi hành，Bạn sẽ thấy nhật ký tải xuống mô hình，Sau khi tải về bạn có thể kết nối và sử dụng
Ở trên được sử dụngCPUlý luận，nếu cóGPU，Tham khảo chi tiết：https://github.com/modelscope/FunASR/blob/main/runtime/docs/SDK_advanced_guide_online_zh.md' WHERE `id` = 'ASR_FunASRServer';