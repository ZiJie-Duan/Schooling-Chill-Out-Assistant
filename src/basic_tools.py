import platform
import os
 
class FilePath:
    """
    一个文件路径管理类
    负责跨平台的处理和管理文件路径
    可以检测操作系统，拆分工作路径，文件名和 文件后缀
    可以根据工作路径快速构建 新的文件 灵活的指定后缀和名称
    """
    def __init__(self, file_path):
        self.system = platform.system() # 检测操作系统
        self.file_path = None           # 文件完整路径
        self.file_name = None           # 文件完成名称
        self.file_name_no_ext = None    # 文件名称 无后缀
        self.file_ext = None            # 文件后缀
        self.file_working_path = None   # 文件工作路径
        self.set_path(file_path)
    
    def __call__(self):
        """返回文件完整路径"""
        return self.file_path  
    
    def _path_check(self, file_path):  
        """检查传入的文件路径 是否合法"""
        tmp_path = file_path.split("\\")
        if "." in tmp_path[-1]:
            return True
        else:
            return False

    def set_path(self, file_path):  
        """设置文件路径并分离出文件名、文件扩展名等"""
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

    def nfile(self, name=None, full_name=None, ext=None):  
        """
        构建新的文件路径
            name: 新文件名称 不包含后缀
            full_name: 新文件名称 全名
            ext: 新文件后缀
        如果full_name不为None, 则忽略name和ext
        只有name将会改变文件名称, ext将会改变文件后缀
        """
        if self.system == "Windows":
            # Windows实现
            if full_name != None:
                return self.file_working_path + "\\" + full_name
            else:
                if name == None:
                    if ext == None:
                        return self.file_working_path + "\\" + self.file_name_no_ext + "_new." + self.file_ext
                    else:
                        return self.file_working_path + "\\" + self.file_name_no_ext + "." + ext
                else:
                    if ext == None:
                        return self.file_working_path + "\\" + name + "." + self.file_ext
                    else:
                        return self.file_working_path + "\\" + name + "." + ext
        else:
            pass # 其他系统（例如MAC）


class SystemCmd:
    """
    一个系统命令行管理类
    """

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


# fp = FilePath(r"C:\Users\lucyc\Desktop\kk.jpg")
# print(fp.file_path)
# print(fp.nfile(ext="go"))