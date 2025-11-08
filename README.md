# 改版

小组丐板项目

# 依赖

> 在安装neo4j之前你需要准备java21
> [Oracle JDK](https://www.oracle.com/java/technologies/downloads/)

```bash
#Neo4j linux
wget -O - https://debian.neo4j.com/neotechnology.gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/neotechnology.gpg
echo 'deb [signed-by=/etc/apt/keyrings/neotechnology.gpg] https://debian.neo4j.com stable latest' | sudo tee -a /etc/apt/sources.list.d/neo4j.list
sudo apt-get update

sudo apt-get install neo4j=1:5.25.1
#windows
#"自己去下载"
https://neo4j.ac.cn/deployment-center/
```

配置neo4j环境变量，见[教程](https://neo4j.ac.cn/docs/operations-manual/5/installation/windows/)

# 部署
```bash
python -m venv .venv
#linux
source .venv/bin/activate
#windows
\.venv\Scripts\activate.bat

pip install -r requirements.txt

cd web
npm install
vite
```
## 数据库数据

linux服务器有自己去copy,账号密码群里有

# todo

继续美化，数据页还要美化一下

# 启动
```bash
cd src
python3 main.py

cd ..
cd web
npx build
```
