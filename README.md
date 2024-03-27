# Auto-Download-And-Update-Github-Repo-And-Releases
自动下载和更新Github存储库源码和Releases

脚本说明：
对于在Github上面非常多的优质资源，开发者可能会删库的现象（开发者可能心情不好或者有其他的苦衷）  
这种现象会导致普通用户，或者众多技术员无法再下载到好用的软件、插件等  
可以稍作修改并定时执行这个脚本，开发者只要更新，执行脚本就会自动下载最新的Releases内容和源码  

脚本更新说明：
由于本人编程能力较差，脚本代码是询问GPT和在其他人的帮助下写出来的，可能有些不完善的情况。
如果您有新的需求，请在Issues中提出，我看情况是否能够添加功能。  
如果您自己就会编程，那更好了，您可以自己添加功能需求代码，如果可以，我也非常欢迎您提交修改，完善代码。  

脚本执行环境说明：  
环境需求：[Python](https://www.python.org/)、[GitHub CLI](https://cli.github.com/)、Windows系统  
“由于gh命令（GitHub CLI）执行时，其中的--json代码只能在Windows上运行（尚未测试MacOS），所以需要Windows系统来执行脚本”  

使用说明：  
1、安装GitHub CLI，并执行`gh auth login`登录你的账号。
（如果不会用可以看其他人写的这篇文章[https://blog.csdn.net/qq_34438779/article/details/128606768](https://blog.csdn.net/qq_34438779/article/details/128606768)）  
2、修改脚本，将前几行中相对应的信息填写进去
3、执行脚本，测试一下是否能正常执行
3、添加定时任务，设置每天几点定时执行
