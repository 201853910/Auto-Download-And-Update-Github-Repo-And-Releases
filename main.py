import os
import subprocess
import json
import time
import shlex

# 这一部分是需要修改的内容
# GitHub 项目信息
owner = ""  # GitHub 项目所有者用户名
repo = ""  # GitHub 项目仓库名称
# 设置网络连接代理，如不需要请将下面四行注释
proxy_host = "127.0.0.1" # 设置代理IP地址
proxy_port = "7890" # 设置代理端口
os.environ["HTTP_PROXY"] = f"http://{proxy_host}:{proxy_port}" # 设置HTTP代理环境变量
os.environ["HTTPS_PROXY"] = f"http://{proxy_host}:{proxy_port}" # 设置HTTPS代理环境变量
# 设置下载目录，以/结尾
directory = "E:/github/" # 这个是示例的路径，请修改为你自己的路径

# 下面是不需要更改的代码
# 获取最新的 release 标签名
def get_latest_tag(owner, repo):
    cmd = f"gh release list -R {owner}/{repo} -L 1 --json tagName"
    output = subprocess.check_output(cmd, shell=True).decode('utf-8')
    releases = json.loads(output)
    latest_tag = releases[0]['tagName'] if releases else None
    return latest_tag
# 读取本地存储的最新 release
def read_current_tag(repo, directory):
    if os.path.exists(f"{directory}{repo}_latest_tag.txt"):
        with open(f"{directory}{repo}_latest_tag.txt", "r") as f:
            current_tag = f.read().strip()
    else:
        current_tag = ""
    return current_tag
# 下载release文件
def download_release(owner, repo, latest_tag, directory, max_retries=3):
    retry_count = 0
    while retry_count < max_retries:
        try:
            # 下载 release 文件到指定目录
            cmd = f"gh release download -R {owner}/{repo} {latest_tag} --clobber -D {directory}Releases/{repo}/{shlex.quote(latest_tag)}"
            output = subprocess.check_output(cmd, shell=True).decode('utf-8')
            if output:
                err_msg = (f"【release文件下载错误】{owner}/{repo}存储库tag版本【{latest_tag}】发生了错误：{output}")
                with open(f"{directory}error_log.txt", "a") as errfile:
                    errfile.write(err_msg + "\n")
                return
            else:
                info_msg = (f"【release文件下载成功】{owner}/{repo}存储库tag版本【{latest_tag}】")
                with open(f"{directory}info_log.txt", "a") as infofile:
                    infofile.write(info_msg + "\n")
                break
        except Exception as e:
            retry_count += 1
            err_msg = (f"【单次下载错误】{owner}/{repo}存储库tag版本【{latest_tag}】文件下载时发生了错误，这是第{retry_count}/{max_retries}次下载")
            with open(f"{directory}error_log.txt", "a") as errfile:
                errfile.write(err_msg + "\n")
            if retry_count ==3:
                err_msg = (f"【release文件下载错误】{owner}/{repo}存储库tag版本【{latest_tag}】发生了错误：{e}")
                with open(f"{directory}error_log.txt", "a") as errfile:
                    errfile.write(err_msg + "\n")
                return
            time.sleep(2) # 等待2秒后重试
# 下载源码文件
def download_source(owner, repo, latest_tag, directory, max_retries=3):
    retry_count = 0
    while retry_count < max_retries:
        try:
            # 下载源码并保存为 zip 格式到指定目录
            cmd = f"gh release download -R {owner}/{repo} {latest_tag} --clobber -A zip -D {directory}Sources/{repo}/{shlex.quote(latest_tag)}"
            output = subprocess.check_output(cmd, shell=True).decode('utf-8')
            if output:
                err_msg = (f"【release源码下载错误】{owner}/{repo}存储库tag版本【{latest_tag}】发生了错误：{output}")
                with open(f"{directory}error_log.txt", "a") as errfile:
                    errfile.write(err_msg + "\n")
                return
            else:
                info_msg = (f"【release源码下载成功】{owner}/{repo}存储库tag版本【{latest_tag}】")
                with open(f"{directory}info_log.txt", "a") as infofile:
                    infofile.write(info_msg + "\n")
                break
        except Exception as e:
            retry_count += 1
            err_msg = (f"【单次下载错误】{owner}/{repo}存储库tag版本【{latest_tag}】源码下载时发生了错误，这是第{retry_count}/{max_retries}次下载。")
            with open(f"{directory}error_log.txt", "a") as errfile:
                errfile.write(err_msg + "\n")
            if retry_count ==3:
                err_msg = (f"【release源码下载错误】{owner}/{repo}存储库tag版本【{latest_tag}】发生了错误：{e}")
                with open(f"{directory}error_log.txt", "a") as errfile:
                    errfile.write(err_msg + "\n")
                return
            time.sleep(2) # 等待2秒后重试
# 更新本地存储的最新 release
def update_current_tag(repo, latest_tag, directory):
    with open(f"{directory}{repo}_latest_tag.txt", "w") as f:
        f.write(latest_tag)
# 执行的主函数
def main():
    latest_tag = get_latest_tag(owner, repo)
    current_tag = read_current_tag(repo, directory)
    # 如果有新 release，则下载 release 文件和源码
    if latest_tag != current_tag:
        download_release(owner, repo, latest_tag, directory, max_retries=3)
        download_source(owner, repo, latest_tag, directory, max_retries=3)
        update_current_tag(repo, latest_tag, directory)
# 执行函数
if __name__ == "__main__":
    main()
