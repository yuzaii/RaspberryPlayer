import subprocess
from Foundation import NSAppleScript


def mac_set_volume(volume):
    """
    设置音量

    Parameters:
        volume (int): 0到100之间的整数，表示音量百分比
    """
    try:
        # 构建AppleScript命令
        script = f"set volume output volume {volume}"

        # 使用subprocess运行osascript命令
        subprocess.run(["osascript", "-e", script])
        print(f"音量设置为：{volume}%")
    except Exception as e:
        print(f"发生错误：{e}")


def get_system_volume():
    script_str = 'output volume of (get volume settings)'
    script = NSAppleScript.alloc().initWithSource_(script_str)
    result, error_info = script.executeAndReturnError_(None)

    if result:
        return result.stringValue()
    else:
        print(f"Error: {error_info}")
        return None


if __name__ == '__main__':
    # 设置音量为50%
    mac_set_volume(90)
    # for i in range(100):
    #     mac_set_volume(i)
    #     time.sleep(1)
    # 获取系统音量
    # current_volume = get_system_volume()
    #
    # if current_volume is not None:
    #     print(f"当前系统音量：{current_volume}")
