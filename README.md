# RAGLaw

linux开发

## 开始
创建环境
```
conda create -n RAGLaw python=3.10
conda activate RAGLaw
```
有gpu需要设置环境变量
```
# 有gpu
set CMAKE_ARGS=-DLLAMA_CUBLAS=on
set FORCE_CMAKE=1
pip install llama-cpp-python --force-reinstall --upgrade --no-cache-dir
```


安装依赖

```
git clone https://github.com/20km-shimakaze/RAGLaw.git
pip install -r requirements.txt
cd RAGLaw
```

安装编译llama.cpp
```
git clone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp
make
pip install -r requirements.txt
cd ..
```




## 设计
- 框架 LangChain
- 数据库 milvus
- 语言 python 
- 模型 
  - embedding模型
  - llama3 8b（暂定）

## 运行逻辑
### 使用
1. 用户输入提问
2. embedding模型转化为向量
   1. 数据库查询
      1. 法条
      2. 判例
   2. 网页搜索答案
3. 结合查询数据，组成prompt
4. 模型输出结果

## 代码架构
- db 数据库处理
- law_data 法律数据
- models 模型

## 数据库架构
### law_vec
> 储存法律信息的数据库
- id 数据id
- law_type 信息的类型
  - law_book 法律法规
  - xxx 法律判例
- vector 向量
- info 对应的文字