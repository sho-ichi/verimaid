import re

# "AAA[BBB]" -> "AAA", "CCC" -> "CCC"
def simplify(word):
    idx = word.find("[")
    if idx == -1:
        return word
    return word[:idx]


def main():
    # 全体の色を設定
    print("%%{\ninit: {\n    \'theme\': \'base\',\n    \'themeVariables\': {")
    print("        \'primaryColor\': \'#ECECFF\',")
    print("        \'primaryBorderColor\': \'#9B7BDD\',")
    print("        \'secondaryColor\': \'#F0F0C0\',")
    print("        \'tertiaryColor\': \'#ECECFF\',")
    print("        \'tertiaryBorderColor\': \'#AB92E5\'")
    print("    }\n  }\n}%%")

    # ファイルを開く
    with open('Top.v', 'r') as file:
        content = file.read()

    # re.DOTALL フラグを使って複数行にマッチさせる
    matches = re.findall(r"(\w+)\s+(\w+)\s*\((.*?)\);", content, re.DOTALL)
    moduleName = ""

    for match in matches:
        # 選択したファイルのモジュールにおける、入出力ポート
        if match[0] == 'module':
            moduleName = match[1]
            print("graph TD")        
            print("    input[\" \"]:::transparent ~~~ middle[\" \"]:::transparent ~~~ output[\" \"]:::transparent")

            io_matches = re.findall(r"(input|output)\s*(\[\d+:\d+\])?\s*(\w+);", content)
            for io in io_matches:
                port = io[2]
                s_port = simplify(io[2]) 
                if io[2][0] == "i":
                    print(f"        input ~~~ {moduleName}-{s_port}[\"{port}\"]:::input ~~~ middle")
                elif io[2][0] == "o":
                    print(f"        middle ~~~ {moduleName}-{s_port}[\"{port}\"]:::output ~~~ output")
                else:
                    print(f"        {moduleName}-{s_port}[\"{port}\"]")

            print("    subgraph ", match[1])
            print("        middle")
            for io in io_matches:
                port = io[2]
                s_port = simplify(io[2]) 
                print(f"        {moduleName}-{s_port}[\"{port}\"]")
            continue
        
        # 選択したファイルのモジュールにおける、サブモジュールと接続している信号
        print(f"\n        {match[0]}")
        port_matches = re.findall(r"\.(\w+)\s*\(([^)]+)\)", match[2].strip())
        for port, signal in port_matches:
            s_signal  = simplify(signal)
            print(f"        {moduleName}-{s_signal}[\"{signal}\"]:::signal")
    print("    end\n")

    for match in matches:
        if match[0] == 'module':
            continue
        # 選択したファイルのモジュールにおける、サブモジュール
        print(f"    subgraph {match[0]}")
        print(f"        {match[0]}-middle[\" \"]:::transparent")
        port_matches = re.findall(r"\.(\w+)\s*\(([^)]+)\)", match[2].strip())
        for port, signal in port_matches:
            s_port, s_signal = simplify(port), simplify(signal)
            if port[0] == "i" or signal[0] == "i" or signal[0] == "r":
                print(f"        {moduleName}-{s_signal} --> {match[0]}-{s_port}[\"{port}\"]:::input ~~~ {match[0]}-middle")
            elif port[0] == "o" or signal[0] == "o":
                print(f"        {match[0]}-middle ~~~ {match[0]}-{s_port}[\"{port}\"]:::output --> {moduleName}-{s_signal}")
            else:
                print(f"        {match[0]}-{s_port}[\"{port}\"]:::signal --- {moduleName}-{s_signal}")
        print("    end\n")

    # クラス定義による色を設定
    print("classDef transparent fill:transparent, stroke: transparent")
    print("classDef signal fill: #F0F0C0, stroke:#ECECFF")
    print("classDef input fill: #FF6666, stroke:#ECECFF")
    print("classDef output fill: #6666FF, stroke:#ECECFF")

if __name__ == "__main__":
    main()
