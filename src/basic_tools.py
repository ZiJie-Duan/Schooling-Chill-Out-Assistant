import platform
import os

class FilePath:
    def __init__(self):
        self.system = platform.system() # 检测操作系统
        self.file_path = None
        self.file_name = None
        self.file_name_no_ext = None
        self.file_ext = None
        self.file_working_path = None
    
    def __call__(self):
        return self.file_path  # 返回文件路径
    
    def _path_check(self, file_path):  # 检查路径中是否包含文件名
        tmp_path = file_path.split("\\")
        if "." in tmp_path[-1]:
            return True
        else:
            return False

    def set_path(self, file_path):  # 设置文件路径并分离出文件名、文件扩展名等
        if self.system == "Windows":
            if self._path_check(file_path):
                self.file_path = file_path
                tmp = file_path.split("\\")
                self.file_name = tmp[-1]
                self.file_name_no_ext = self.file_name.split(".")[0]
                self.file_ext = self.file_name.split(".")[1]
                tmp = tmp[:-1]
                self.file_working_path = "\\".join(tmp)
                return True
            else:
                return False
        else:
            pass # 其他系统（例如MAC）

    def build_new_file(self, file_name=None, file_name_no_ext=None, ext=None):  # 构建新文件的路径
        if self.system == "Windows":
            # 下面的逻辑用于构建新的文件路径
            # 省略了一些详细代码
            pass
        else:
            pass # 其他系统（例如MAC）


class SystemCmd:

    def __init__(self):
        self.system = platform.system()  # 检测操作系统

    def __call__(self, cmd="NONE"):
        if cmd == "NONE":
            pass
        else:
            self.cmd(cmd)
    
    def cmd(self, cmd):  # 执行命令行命令
        if self.system == "Windows":
            os.system(cmd)
        else:
            pass # 其他系统（例如MAC）

    # def cmd_with_return(self, cmd): 
    #     有关执行命令并返回结果的函数
    #     pass # 省略了代码
    
    def open_file(self, file_path):  # 打开文件
        if self.system == "Windows":
            os.startfile(file_path)
        
        else:
            pass # 其他系统（例如MAC）

# 下面的 FILE_MANAGER 类已被注释掉
# 它看起来像是用于管理多个文件路径的工具

# test code

# 下面是一些测试代码和注释，已被注释掉

