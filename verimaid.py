import re

# modules = { 'module1': { 'in':['iCLK', 'iValue'],
#                     'out':['iValue'],
#                     'instances':{   'module2':'m2',
#                                     'module3':'m3'}
#             }
#             'module2': { 'in':[],
#                     'out':[]},
#             'module3': { 'in':[],
#                     'out':[]}
#             }

pattern = r"(\w+)\s+(\w+)\s*\((.*?)\);"

# ファイルを開く
with open('Top.v', 'r') as file:
    content = file.read()



# re.DOTALL フラグを使って複数行にマッチさせる
matches = re.findall(pattern, content, re.DOTALL)

for match in matches:
    if match[0] == 'module':
        print("graph TD")
        print("    subgraph", match[1])
        print("        middle[\" \"]:::transparent")
        io_matches = re.findall(r"(input|output)\s*(\[\d+:\d+\])?\s*(\w+);", content)
        for io in io_matches:
            if io[2][0] == "i":
                print("        s_" + io[2] + ":::signal ~~~~~ middle")  # io[1]:[1:0]
            elif io[2][0] == "o":
                print("        middle ~~~~~ s_" + io[2] + ":::signal")  # io[1]:[1:0]
            else:
                print("        s_" + io[2])  # io[1]:[1:0]
        continue
    
    print(f"\n        {match[0]}")
    port_matches = re.findall(r"\.(\w+)\s*\(([^)]+)\)", match[2].strip())
    for port, signal in port_matches:
        print(f"        s_{signal}:::signal")
print("    end\n")

for match in matches:
    if match[0] == 'module':
        continue
    print("    subgraph", match[0])
    print(f"        middle_{match[0]}[\" \"]:::transparent")
    # print("Instance Name:", match[1])
    # print("Connections:", match[2].strip())
    port_matches = re.findall(r"\.(\w+)\s*\(([^)]+)\)", match[2].strip())
    for port, signal in port_matches:
        if port[0] == "i":
            print(f"        s_{signal}:::signal --> {port}:::signal ~~~~~ middle_{match[0]}")
        elif port[0] == "o":
            print(f"        middle_{match[0]} ~~~~~ {port}:::signal --> s_{signal}:::signal")
        else:
            print(f"        {port}:::signal --- s_{signal}:::signal")


    print("    end\n")
