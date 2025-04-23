from mcp.server.fastmcp import FastMCP
import requests
import json
from datetime import datetime

# 创建MCP服务器
mcp = FastMCP("Auth Check Server")

# 导入instanchek.py中的函数
@mcp.tool()
def check_auth_api():
    """检查串流接口的状态，仅返回连接状态 (True/False)"""
    url = "https://cloud.139.com/ulhw/cloudphone/user/instance/auth"
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'token': 'instan_token',
        'sign': 'sign_xxxx',
    }
    payload = {
        "phoneId": "o91s2b3e",
        "authId": "",
        "streamType": 2
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            try:
                response_data = response.json()
                header = response_data.get('header', {})
                # 仅当状态为'200'且errMsg为'成功'时返回True
                if header.get('status') == '200' and header.get('errMsg') == '成功':
                    return True
                else:
                    # 其他情况（包括状态码不对或errMsg不对）都返回False
                    return False
            except json.JSONDecodeError:
                # JSON解析失败也返回False
                return False
        else:
            # HTTP请求不成功返回False
            return False
    except requests.exceptions.RequestException as e:
        # 请求异常返回False
        print(f"请求发生错误: {e}") # 保留日志输出以便调试
        return False

if __name__ == '__main__':
    mcp.run(transport='stdio')# 这里可以添加启动MCP服务器的代码，根据文档可能需要使用mcp命令相关操作
     
     
