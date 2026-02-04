import os
# 这一行是调用刚才安装的神器
from pyncm import GetCurrentSession
from pyncm.utils.helper import UserHelper


def unlock_my_music():
    # 👇 把这里改成你的 NCM 音乐文件的名字
    # 记得加 .ncm 后缀
    file_name = "你的音乐文件名字.ncm"

    # 自动获取当前文件夹路径
    current_folder = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_folder, file_name)

    print(f"🎧 正在准备解锁：{file_name}")

    if not os.path.exists(file_path):
        print(f"❌ 找不到文件！请确认 {file_name} 就在 {current_folder} 文件夹里！")
        return

    # 这是一个魔法命令，模拟命令行调用 pyncm
    # 这样你就不用去为了“黑框框”报错发愁了
    command = f'pyncm "{file_path}"'

    print("🚀 开始转换...")
    # 让 Python 帮你去执行转换命令
    result = os.system(command)

    if result == 0:
        print("✅ 成功！MP3 文件应该已经出现在同级目录了。")
    else:
        print("⚠️ 转换可能出了一点小问题，请检查文件名是否正确。")


if __name__ == "__main__":
    unlock_my_music()