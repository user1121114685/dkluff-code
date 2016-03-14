Bash脚本15分钟进阶教程
2014/04/22 | 分类： 开发 | 1 条评论 | 标签： BASH
分享到：
原文出处： robertmuth   译文出处： 外刊IT评论。欢迎加入技术翻译小组。

这里的技术技巧最初是来自谷歌的“Testing on the Toilet” (TOTT)。这里是一个修订和扩增版本。

脚本安全

我的所有bash脚本都以下面几句为开场白：

1
2
3
#!/bin/bash
set -o nounset
set -o errexit
这样做会避免两种常见的问题：

引用未定义的变量(缺省值为“”)
执行失败的命令被忽略
需要注意的是，有些Linux命令的某些参数可以强制忽略发生的错误，例如“mkdir -p” 和 “rm -f”。

还要注意的是，在“errexit”模式下，虽然能有效的捕捉错误，但并不能捕捉全部失败的命令，在某些情况下，一些失败的命令是无法检测到的。(更多细节请参考这个帖子。)

脚本函数

在bash里你可以定义函数，它们就跟其它命令一样，可以随意的使用；它们能让你的脚本更具可读性：

1
2
3
4
5
6
7
ExtractBashComments() {
    egrep "^#"
} 
 
cat myscript.sh | ExtractBashComments | wc
 
comments=$(ExtractBashComments < myscript.sh)
还有一些例子：

1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
SumLines() {  # iterating over stdin - similar to awk      
    local sum=0
    local line=””
    while read line ; do
        sum=$((${sum} + ${line}))
    done
    echo ${sum}
} 
 
SumLines < data_one_number_per_line.txt 
 
log() {  # classic logger
   local prefix="[$(date +%Y/%m/%d\ %H:%M:%S)]: "
   echo "${prefix} $@" >&2
} 
 
log "INFO" "a message"
尽可能的把你的bash代码移入到函数里，仅把全局变量、常量和对“main”调用的语句放在最外层。

变量注解

Bash里可以对变量进行有限的注解。最重要的两个注解是：

local(函数内部变量)
readonly(只读变量)
1
2
3
4
5
6
7
8
9
# a useful idiom: DEFAULT_VAL can be overwritten
#       with an environment variable of the same name
readonly DEFAULT_VAL=${DEFAULT_VAL:-7} 
 
myfunc() {
   # initialize a local variable with the global default
   local some_var=${DEFAULT_VAL}
   ...
}
这样，你可以将一个以前不是只读变量的变量声明成只读变量：

1
2
3
4
x=5
x=6
readonly x
x=7   # failure
尽量对你bash脚本里的所有变量使用local或readonly进行注解。

用$()代替反单引号(`)

反单引号很难看，在有些字体里跟正单引号很相似。$()能够内嵌使用，而且避免了转义符的麻烦。

1
2
3
# both commands below print out: A-B-C-D
echo "A-`echo B-\`echo C-\\\`echo D\\\`\``"
echo "A-$(echo B-$(echo C-$(echo D)))"
用[[]](双层中括号)替代[]

使用[[]]能避免像异常的文件扩展名之类的问题，而且能带来很多语法上的改进，而且还增加了很多新功能：

操作符  功能说明
||      逻辑or(仅双中括号里使用)
&&      逻辑and(仅双中括号里使用)
<       字符串比较(双中括号里不需要转移)
-lt     数字比较
=       字符串相等
==      以Globbing方式进行字符串比较(仅双中括号里使用，参考下文)
=~      用正则表达式进行字符串比较(仅双中括号里使用，参考下文)
-n      非空字符串
-z      空字符串
-eq     数字相等
-ne     数字不等
单中括号：

1
[ "${name}" \> "a" -o ${name} \< "m" ]
双中括号

1
[[ "${name}" > "a" && "${name}" < "m"  ]]
正则表达式/Globbing

使用双中括号带来的好处用下面几个例子最能表现：

1
2
3
4
5
t="abc123"
[[ "$t" == abc* ]]         # true (globbing比较)
[[ "$t" == "abc*" ]]       # false (字面比较)
[[ "$t" =~ [abc]+[123]+ ]] # true (正则表达式比较)
[[ "$t" =~ "abc*" ]]       # false (字面比较)
注意，从bash 3.2版开始，正则表达式和globbing表达式都不能用引号包裹。如果你的表达式里有空格，你可以把它存储到一个变量里：

1
2
r="a b+"
[[ "a bbb" =~ $r ]]        # true
按Globbing方式的字符串比较也可以用到case语句中：

1
2
3
case $t in
abc*)  <action> ;;
esac
字符串操作

Bash里有各种各样操作字符串的方式，很多都是不可取的。

基本用户

1
2
3
4
5
6
7
8
9
10
11
f="path1/path2/file.ext" 
 
len="${#f}" # = 20 (字符串长度) 
 
# 切片操作: ${<var>:<start>} or ${<var>:<start>:<length>}
slice1="${f:6}" # = "path2/file.ext"
slice2="${f:6:5}" # = "path2"
slice3="${f: -8}" # = "file.ext"(注意："-"前有空格)
pos=6
len=5
slice4="${f:${pos}:${len}}" # = "path2"
替换操作(使用globbing)

1
2
3
4
5
6
7
8
9
f="path1/path2/file.ext" 
 
single_subst="${f/path?/x}"   # = "x/path2/file.ext"
global_subst="${f//path?/x}"  # = "x/x/file.ext" 
 
# 字符串拆分
readonly DIR_SEP="/"
array=(${f//${DIR_SEP}/ })
second_dir="${arrray[1]}"     # = path2
删除头部或尾部(使用globbing)

1
2
3
4
5
6
7
8
9
10
11
12
13
f="path1/path2/file.ext"
 
# 删除字符串头部
extension="${f#*.}"  # = "ext"
 
# 以贪婪匹配方式删除字符串头部
filename="${f##*/}"  # = "file.ext"
 
# 删除字符串尾部
dirname="${f%/*}"    # = "path1/path2" 
 
# 以贪婪匹配方式删除字符串尾部
root="${f%%/*}"      # = "path1"
避免使用临时文件

有些命令需要以文件名为参数，这样一来就不能使用管道。这个时候?<()?就显出用处了，它可以接受一个命令，并把它转换成可以当成文件名之类的什么东西：

1
2
# 下载并比较两个网页
diff <(wget -O - url1) <(wget -O - url2)
还有一个非常有用处的是”here documents”，它能让你在标准输入上输入多行字符串。下面的’MARKER’可以替换成任何字词。

1
2
3
4
5
6
7
# 任何字词都可以当作分界符
command  << MARKER
...
${var}
$(cmd)
...
MARKER
如果文本里没有内嵌变量替换操作，你可以把第一个MARKER用单引号包起来：

1
2
3
4
5
6
command << 'MARKER'
...
no substitution is happening here.
$ (dollar sign) is passed through verbatim.
...
MARKER
内置变量

变量    说明
$0      脚本名称
$n      传给脚本/函数的第n个参数
$$      脚本的PID
$!      上一个被执行的命令的PID(后台运行的进程)
$?      上一个命令的退出状态(管道命令使用${PIPESTATUS})
$#      传递给脚本/函数的参数个数
$@      传递给脚本/函数的所有参数(识别每个参数)
$*      传递给脚本/函数的所有参数(把所有参数当成一个字符串)
提示
使用$*很少是正确的选择。
$@能够处理空格参数，而且参数间的空格也能正确的处理。
使用$@时应该用双引号括起来，像”$@”这样。
调试

对脚本进行语法检查：

1
bash -n myscript.sh
跟踪脚本里每个命令的执行：

1
bash -v myscripts.sh
跟踪脚本里每个命令的执行并附加扩充信息：

1
bash -x myscript.sh
你可以在脚本头部使用set -o verbose和set -o xtrace来永久指定-v和-o。当在远程机器上执行脚本时，这样做非常有用，用它来输出远程信息。

什么时候不应该使用bash脚本

你的脚本太长，多达几百行
你需要比数组更复杂的数据结构
出现了复杂的转义问题
有太多的字符串操作
不太需要调用其它程序和跟其它程序管道交互
担心性能
这个时候，你应该考虑一种脚本语言，比如Python或Ruby。

参考

Advanced Bash-Scripting Guide:?http://tldp.org/LDP/abs/html/
Bash Reference Manual



UPDATE: November 25, 2013

检查远程端口是否对bash开放：

echo >/dev/tcp/8.8.8.8/53 && echo "open"
让进程转入后台：

Ctrl + z
将进程转到前台：

fg
产生随机的十六进制数，其中n是字符数：

openssl rand -hex n
在当前shell里执行一个文件里的命令：

source /home/user/file.name
截取前5个字符：

${variable:0:5}
SSH debug 模式:

ssh -vvv user@ip_address
SSH with pem key:

ssh user@ip_address -i key.pem
用wget抓取完整的网站目录结构，存放到本地目录中：

wget -r --no-parent --reject "index.html*" http://hostname/ -P /home/user/dirs
一次创建多个目录：

mkdir -p /home/user/{test,test1,test2}
列出包括子进程的进程树：

ps axwef
创建 war 文件:

jar -cvf name.war file
测试硬盘写入速度：

dd if=/dev/zero of=/tmp/output.img bs=8k count=256k; rm -rf /tmp/output.img
测试硬盘读取速度：

hdparm -Tt /dev/sda
获取文本的md5 hash：

echo -n "text" | md5sum
检查xml格式：

xmllint --noout file.xml
将tar.gz提取到新目录里：

tar zxvf package.tar.gz -C new_dir
使用curl获取HTTP头信息：

curl -I http://www.example.com
修改文件或目录的时间戳(YYMMDDhhmm):

touch -t 0712250000 file
用wget命令执行ftp下载：

wget -m ftp://username:password@hostname
生成随机密码(例子里是16个字符长):

LANG=c < /dev/urandom tr -dc _A-Z-a-z-0-9 | head -c${1:-16};echo;
快速备份一个文件：

cp some_file_name{,.bkp}
访问Windows共享目录：

smbclient -U "DOMAIN\user" //dc.domain.com/share/test/dir
执行历史记录里的命令(这里是第100行):

!100
解压:

unzip package_name.zip -d dir_name
输入多行文字(CTRL + d 退出):

cat > test.txt
创建空文件或清空一个现有文件：

> test.txt
与Ubuntu NTP server同步时间：

ntpdate ntp.ubuntu.com
用netstat显示所有tcp4监听端口：

netstat -lnt4 | awk '{print $4}' | cut -f2 -d: | grep -o '[0-9]*'
qcow2镜像文件转换：

qemu-img convert -f qcow2 -O raw precise-server-cloudimg-amd64-disk1.img \
                                   precise-server-cloudimg-amd64-disk1.raw
重复运行文件，显示其输出（缺省是2秒一次）：

watch ps -ef
所有用户列表：

getent passwd
Mount root in read/write mode:

mount -o remount,rw /
挂载一个目录（这是不能使用链接的情况）:

mount --bind /source /destination
动态更新DNS server:

nsupdate < <EOF
update add $HOST 86400 A $IP
send
EOF
递归grep所有目录：

grep -r "some_text" /path/to/dir
列出前10个最大的文件：

lsof / | awk '{ if($7 > 1048576) print $7/1048576 "MB "$9 }' | sort -n -u | tail
显示剩余内存(MB):

free -m | grep cache | awk '/[0-9]/{ print $4" MB" }'
打开Vim并跳到文件末：

vim + some_file_name
Git 克隆指定分支(master):

git clone git@github.com:name/app.git -b master
Git 切换到其它分支(develop):

git checkout develop
Git 删除分支(myfeature):

git branch -d myfeature
Git 删除远程分支

git push origin :branchName
Git 将新分支推送到远程服务器：

git push -u origin mynewfeature
打印历史记录中最后一次cat命令：

!cat:p
运行历史记录里最后一次cat命令：

!cat
找出/home/user下所有空子目录:

find /home/user -maxdepth 1 -type d -empty
获取test.txt文件中第50-60行内容：

< test.txt sed -n '50,60p'
运行最后一个命令(如果最后一个命令是mkdir /root/test, 下面将会运行: sudo mkdir /root/test)：

sudo !!
创建临时RAM文件系统 – ramdisk (先创建/tmpram目录):

mount -t tmpfs tmpfs /tmpram -o size=512m
Grep whole words:

grep -w "name" test.txt
在需要提升权限的情况下往一个文件里追加文本：

echo "some text" | sudo tee -a /path/file
列出所有kill signal参数:

kill -l
在bash历史记录里禁止记录最后一次会话：

kill -9 $$
扫描网络寻找开放的端口：

nmap -p 8081 172.20.0.0/16
设置git email:

git config --global user.email "me@example.com"
To sync with master if you have unpublished commits:

git pull --rebase origin master
将所有文件名中含有”txt”的文件移入/home/user目录:

find -iname "*txt*" -exec mv -v {} /home/user \;
将文件按行并列显示：

paste test.txt test1.txt
shell里的进度条:

pv data.log
使用netcat将数据发送到Graphite server:

echo "hosts.sampleHost 10 `date +%s`" | nc 192.168.200.2 3000
将tabs转换成空格：

expand test.txt > test1.txt
Skip bash history:

< space >cmd
去之前的工作目录：

cd -
拆分大体积的tar.gz文件(每个100MB)，然后合并回去：

split –b 100m /path/to/large/archive /path/to/output/files
cat files* > archive
使用curl获取HTTP status code:

curl -sL -w "%{http_code}\\n" www.example.com -o /dev/null
设置root密码，强化MySQL安全安装:

/usr/bin/mysql_secure_installation
当Ctrl + c不好使时:

Ctrl + \
  获取文件owner:

stat -c %U file.txt
block设备列表：

lsblk -f
找出文件名结尾有空格的文件：

find . -type f -exec egrep -l " +$" {} \;
找出文件名有tab缩进符的文件

find . -type f -exec egrep -l $'\t' {} \;
用”=”打印出横线:

printf '%100s\n' | tr ' ' =
