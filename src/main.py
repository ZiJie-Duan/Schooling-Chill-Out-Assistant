from module.chrome_control import Unimelb_Lecture_Rec_CC
from module.config import Config
from agent.agent import AgentSystem, AgentBrick


def print_imporant_notice(notice):
    print("重要信息：", notice)
    return {"info":notice}

def print_ignore_info(info):
    print("无用信息：", info)

def print_next(info):
    print("下一个操作：", info)


rt = AgentBrick("return_node")
rt.easy_set_up("do popr nf")


pn = AgentBrick("print_next")
pn.easy_set_up("do single", call_back=print_next, brick_list=[rt])
pn.parameters = {"info": {"type": "string", "description": "下一个操作"}}


important_notice = AgentBrick("record_important_notice", "记录重要的信息")
important_notice.front_prompt = """
    如果字幕中包含有重要的信息（时间，地点，人物，事件）等，尤其是和课程相关的内容
    请选择<record_important_notice>，将信息记录下来。
"""
important_notice.parameters = {"notice": {"type": "string", "description": "重要信息"}}
important_notice.easy_set_up("do single", call_back=print_imporant_notice, brick_list=[pn])



ignore_info = AgentBrick("ignore_info", "忽略无用的信息")
ignore_info.front_prompt = """
    如果字幕中包含有无用的信息，无意义的口头禅，或者和课程无关的内容
    请选择<ignore_info>，将信息忽略。
"""
ignore_info.parameters = {"info": {"type": "string", "description": "无用信息"}}
ignore_info.easy_set_up("do env", call_back=print_ignore_info)



root_b = AgentBrick("decision_maker", "root_brick")
root_b.back_prompt = """
    你是一个学生，你将得到一节大学课程中的部分字幕信息，以及背景信息。
    你的目标是根据字幕信息和背景信息，做出正确的决定。
    背景信息仅用作参考，你的决定仅和字幕信息有关。
    \n 以下是字幕信息：\n {subtitle} \n 你需要做出决定：
"""
root_b.parameters = {"subtitle": {"type": "string", "description": "字幕信息"}}
root_b.easy_set_up("think multi", brick_list=[important_notice, ignore_info])


sys = AgentSystem(root_b,api_key="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")
sys.register({"info":"??"})
sys.run({"subtitle" : "hi 大家好，现在上课了哈，你们昨天作业做的怎么样了？那个你们记得明天晚上9点前提交哈，不然就算迟交了，那个，就会扣分了哈，那个，你们有什么问题吗？"})