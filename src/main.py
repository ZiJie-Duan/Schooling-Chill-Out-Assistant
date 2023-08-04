from module.chrome_control import Unimelb_Lecture_Rec_CC
from module.config import Config
from module.subtitle import Subtitle_Driver
from agent.agent import AgentSystem, AgentBrick
import time

subtitle_g = ""
back_ground_g = ""

def write_to_notion_impotant(notice: str) -> None:
    with open(r"C:\Users\lucyc\Desktop\notion", "a", encoding="utf-8") as file:
        file.write("\n\nIMPOTANT INFO MATION\n")
        file.write(notice + "\n")

def write_to_notion_summarized(summarized_info: str, back_ground: str) -> None:
    global back_ground_g
    back_ground_g = back_ground
    with open(r"C:\Users\lucyc\Desktop\notion", "a", encoding="utf-8") as file:
        file.write(summarized_info + "\n")
    return {"summarized_info" : summarized_info}


summarize_info = AgentBrick("summarize_info", "总结字幕信息")
summarize_info.front_prompt = """
    如果字幕是关于知识点的，和课程相关的知识
    你可以调用summarize_info函数，来总结字幕信息并更新背景信息
    如果你不知道选择些什么，请调用summarize_info函数。
    请使用中文记录, 在总结中插入(time)来表示时间,time的格式为hh:mm，来自字幕时间
    例如：教授认为C语言是很重要的(23:45)
"""
summarize_info.parameters = {"summarized_info": {"type": "string", "description": "总结完成的信息"},
                             "back_ground": {"type": "string", "description": "背景信息"}}
summarize_info.easy_set_up("do env", call_back=write_to_notion_summarized)


important_notice = AgentBrick("record_important_notice", "记录重要的信息")
important_notice.front_prompt = """
    如果字幕中包含有重要的信息（时间，地点，人物，事件）等，
    尤其是关于考试的信息，作业的信息，需要学生做出行动的信息
    请调用<record_important_notice>函数，将信息记录下来。
    尽可能保留细节
    请使用中文记录。
"""
important_notice.parameters = {"notice": {"type": "string", "description": "重要信息"}}
important_notice.easy_set_up("do env", call_back=write_to_notion_impotant)


root_b = AgentBrick("decision_maker", "root_brick")
root_b.back_prompt = """
    你是一个学生，你将得到一节大学课程中的部分字幕信息，以及背景信息。
    你的目标是根据字幕信息和背景信息，做出行动。
    以下是背景信息：\n <<<{back_ground}>>>
    以下是字幕信息：\n <<<{subtitle}>>> \n 你需要做出决定：
"""
root_b.parameters = {"subtitle": {"type": "string", "description": "字幕信息"},
                     "back_ground": {"type": "string", "description": "背景信息"}}
root_b.easy_set_up("think multi", brick_list=[summarize_info, important_notice])


def main():
    sys = AgentSystem(root_b,api_key="")
    sys.register({"subtitle":"","back_ground":"", "all_subtitle":""})

    subt = Subtitle_Driver()
    melb_cc = Unimelb_Lecture_Rec_CC("127.0.0.1:9222", r"C:\Users\lucyc\AppData\Local\Google\Chrome\User Data", "Default")
    
    url = input("Enter URL: ")
    melb_cc.lock_page(url)
    melb_cc.lock_element()

    while True:
        time.sleep(0.5)
        subtitle = melb_cc.get_subtitle()
        
        if subtitle[1] == "<No-text-found>":
            continue
        else:
            subtitle_time = subtitle[0].split("/")[0]
            if subt.add_subtitle((subtitle_time, subtitle[1])):
                print((subtitle_time, subtitle[1]))
        
        if subt.lenth > 60:
            melb_cc.play_or_stop()
            subtitle_g = subt.get_subtitle_str()
            sys.memo.update(back_ground=back_ground_g,
                            subtitle=subtitle_g)
            args = sys.get_parameter(root_b)
            sys.run(args)
            melb_cc.play_or_stop()


if __name__ == "__main__":
    main()