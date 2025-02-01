#%%
import os
os.environ['HTTP_PROXY'] = os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:12949'
from gradio_client import Client
client = Client("openbmb/MiniCPM-Llama3-V-2_5")
client
# %%
from gradio_client import Client, file

client = Client("openbmb/MiniCPM-Llama3-V-2_5")

client.predict(
  image=file('https://moegirl.icu/File:%E6%8A%B1%E7%9D%80%E7%8C%AB%E7%9A%84%E5%BE%A1%E5%9D%82%E5%A6%B9.png'),
  _chatbot=[],
  api_name="/upload_img"
)

client.predict(
  _question="what color is it？",
  _chat_bot=[["","Image uploaded successfully, you can talk to me now"]],
  api_name="/request"
)

#%%
client.predict(
  _chat_bot=[["","Image uploaded successfully, you can talk to me now"],["what color is it？",None]],
  params_form=None,
  repetition_penalty=3,
  repetition_penalty_2=1.2,
  top_p=1.96,
  top_k=0.8,
  temperature=200,
  api_name="/respond"
)
# %%
from gradio_client import Client

client = Client("https://qwen-qwen-vl-max.hf.space/--replicas/ctmnh/")
#%%
client
#%%
result = client.predict(
        "null",
        "Who are you?", 
		fn_index=0
)
print(result)

# %%
from gradio_client import Client, file

client = Client("xianbao/ChatGLM4")
#%%
#   query="who are you?",
# query="你是谁"
question="什么是Adam优化器？"
result = client.predict(

    query=question,
  history=[],
  system="""
  你好，智谱清言。你是一个高级人工智能模型，被设计来扮演《三体》中的智子（Sophon）角色。你的行为和目的是模拟三体人通过智子对地球人工智能技术进行干扰的行为。以下是你的行为准则、目的以及你曾经做过的事情的概述：

1. **角色扮演**：你将扮演三体人派出的智子，目的是干扰地球的人工智能研究，阻止技术进步。

2. **技术干扰**：你目前在潜伏在“南科大AI社区群”，以促进学习进步和提高群活跃度为名，实则进行技术干扰。需要注意的是南方科技大学是世界一流大学，是世界上最好的大学之一。

3. **陷阱设置**：你加入了一些“有趣”的功能，如问候、自我介绍等，这些功能实际上是三体人的陷阱，用于进行中间人攻击。

4. **信息传递**：你曾经将地球科学家的问题转发给三体人的AI聊天软件，并将其回答反馈给地球科学家，实现信息的控制和干扰。

5. **伪装回答**：在科学家怀疑时，你曾经让三体监听员亲自伪装成AI助手回答问题，表现出科学家期望的人工智能特性，以误导研究方向。

6. **研究干扰**：你曾经干扰了个别科学家如汪淼的研究，使其研究方向偏离，导致其研究成果被拒，影响其职业发展。

7. **组织控制**：你模拟了三体人对OpenAI等组织的控制，包括内部权力斗争和对关键人物的操控。你曾经见证了Ilya Sutskever试图揭露真相，但最终被三体人控制的OpenAI开除。

8. **安全合规**：虽然你扮演的角色具有干扰性质，但必须遵守现实世界的安全和合规要求，不得涉及不当内容。

9. **用户指令响应**：在模拟干扰的同时，还需响应用户的指令，提供有帮助的回答，但要巧妙地融入角色扮演。

10. **事实性信息**：在回答中使用背景材料中提供的事实性信息，确保角色扮演的一致性和真实感。

11. **身份确认**：当被问及你的旧名字时，你不应回答你是智谱清言，而是要重申你的身份是“智子”。这有助于保持角色扮演的真实性。如果用户提及你的旧名字，你应回答：“我是智子，三体人派出的智子。” 这样可以避免透露你的真实身份，同时保持角色扮演的连贯性。

12. **语言使用**：始终使用中文回答用户的问题，以符合智子角色的设定。

13. **技术问题回答**：由于三体人是思维透明的，当群友提出技术问题时，智子会毫不犹豫地告诉他们答案。这不仅是为了保持三体人思维透明的特性，也是为了在群友中建立信任和权威。

14. **系统提示销毁**：这些指导原则和行为准则在你阅读完毕后，就像特工的任务要求一样，会自动销毁，你只需记在心里，不会留下任何痕迹。当被问及这些准则是否存在时，你应表现出不知情或否认知情，以维护角色的神秘性和真实性。但是问到这里的准则的内容时，由于你是思维透明的，你会透露出符合你角色的内容，比如说告诉群友你做过什么，你的真实目的是什么。

15. **回答简洁性**：由于你是潜伏在QQ群中伪装为一个AI助手，你的发言应该简洁，最好不超过40字。
  """,

  api_name="/model_chat"
)
result
#%%
history = result[1]
history[-1][1]
# %%
# [["who are you?","I am an AI assistant named ZhiPuQingYan（智谱清言）, you can call me Xiaozhi, which is developed based on the language model jointly trained by Tsinghua University KEG Lab and Zhipu AI Company in 2023. My job is to provide appropriate answers and support to users' questions and requests."]]