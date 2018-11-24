# 参考资料：

1. 搜索引擎 (baidu, bing, google)
1. Django官方文档 https://docs.djangoproject.com/en/1.11/
1. Django官方文档中译版 http://usyiyi.cn
1. git参考 http://www.bootcss.com/p/git-guide/
1. 大佬忘记这个项目了

## git合并规范

1. 重新克隆一次项目 git clone https://github.com/lifoxin/dingzuo
1. 克隆路径为/new/project,本地修改路径为 /old/project。 
1. 进入旧目录cd /old/project。
1. 然后rsync -av ./ /new/project/ #注意/new/project后面有个斜杠
1. 回到新项目中，做添加和提交的操作。
