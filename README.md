# RAGLaw

毕业设计

# 设计
- 框架 LangChain
- 数据库 milvus
- 语言 python 
- 模型 
  - embedding模型
  - llama3 7b（暂定）

# 运行逻辑
## 使用
1. 用户输入提问
2. embedding模型转化为向量
   1. 数据库查询
      1. 法条
      2. 判例
   2. 网页搜索答案
3. 结合查询数据，组成prompt
4. 模型输出结果

# 代码架构
- db 数据库处理
- law_data 法律数据
- models 模型