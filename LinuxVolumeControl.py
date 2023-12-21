import subprocess


def set_volume(volume):
    """
    设置音量

    Parameters:
        volume (int): 0到100之间的整数，表示音量百分比
    """
    try:
        # 构建amixer命令
        command = f"amixer set Master {volume}%"

        # 使用subprocess运行amixer命令
        subprocess.run(command, shell=True)
        print(f"音量设置为：{volume}%")
    except Exception as e:
        print(f"发生错误：{e}")


# 设置音量为50%
set_volume(50)
