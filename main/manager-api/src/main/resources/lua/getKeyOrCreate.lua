local value = redis.call('GET', KEYS[1])
-- value Nếu trống thì đặt giá trị
if not value then
    local result = redis.call('SET', KEYS[1], ARGV[1]) 
    -- Kiểm tra xem ARGV[2] có tồn tại và lớn hơn 0 hay không
    local expireTime = tonumber(ARGV[2])
    if expireTime and expireTime > 0 then
        redis.call('EXPIRE', KEYS[1], expireTime)
    end
end
return value