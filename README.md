# hfx-dashboard

基于Dash+Greenplum的数据看板

## 项目结构

```
hfx-dashboard
│  run.py
│  README.md
│  requirements.txt
├─apis                                    # 接口路由定义
│      api_routers.py                     
├─apps                                    # dash应用
│  │  __init__.py
│  │  menu.py
│  │  sales_bymonth.py
│  ├─assets                               # 通用样式
│  │      content.css
│  │      siderbar.css
│  └─components                           # 通用组件
│          __init__.py
│          filter_channels.py
│          filter_city_level.py
│          filter_date_range.py
│          filter_store_age.py
│          filter_store_area.py
│          filter_store_star.py
├─conf                                    # 配置
│  └─config.py
├─conts                                   # 通用常量定义
│  │  __init__.py
│  └─router_conts.py
├─core
│  │  __init__.py
│  └─ flask_app.py                       # flask 实例配置       
├─db                                      # 数据库连接工具
│  │  __init__.py
│  └─Db.py
│          
├─service                                 # 数据处理
│      sales_service.py
├─utils                                   # 通用工具类
│  └─ToolUtil.py
└─run.py

```

## 项目配置

