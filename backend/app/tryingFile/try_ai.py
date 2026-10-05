# import requests
# import json

# response  = requests.post("http://127.0.0.1:11434/api/chat",
#                           json={"model":"phi4-mini",
#                                 "messages" :[{"role":"user",
#                                             "content":"what is compouter explain in deep?"}],"stream":True},stream=True)
                        


# for line in response.iter_lines():
#     if line:
#         data = json.loads(line)
#         print(data['message']['content'],end="",flush=True)
