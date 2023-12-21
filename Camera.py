import cv2

# 打开默认摄像头（通常是内置摄像头）
cap = cv2.VideoCapture(1)

# 检查摄像头是否成功打开
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

while True:
    # print('loading')
    # 读取帧
    ret, frame = cap.read()

    # 如果帧读取失败，退出循环
    if not ret:
        print("Error: Failed to capture frame.")
        break

    # 在窗口中显示帧
    cv2.imshow('Camera', frame)

    # 检查是否按下了 'q' 键，如果是则退出循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放摄像头资源
cap.release()

# 关闭所有窗口
cv2.destroyAllWindows()
