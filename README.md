# BigBoss

> BigBoss is watching your android.

## 设计

![BigBossDesign](BigBoss.svg)

[2rd RMS4A](https://github.com/williamfzc/RMS4A)

### 设备管理

需要id、状态、机型信息等。

- slaver名下
    - json

- master
    - 收集各slaver的连接状态
    - 以数据库形式管理

### 通信

- server之间
    - restful
    - json

- server与device
    - `whenconnect`
    - `adb`

### 任务管理

两种基本思路。

- 关联Jenkins
    - 关联Jenkins上的构建任务
    - 通过前端界面，用户能够通过简单操作灵活配置参数
    - 将参数绑定到jenkins上的对应字段
    - 随后由jenkins接管这一过程

- 不依赖Jenkins
    - 每个任务对应一行命令行（多余逻辑放脚本内）
    - 通过命令行模板进行参数定制
        - 例如`python ${entry_script}`
    - 结合前端界面，用户能够通过简单操作灵活配置参数

公共部分：

- 设备状态更新（是否被占用）
- 任务状态更新（完成与否、执行情况）

## 路线

### 第一期 设备管理

- slaver server
    - [x] 能够正常识别设备插拔
    - [x] 维持最新的设备列表
    - [x] 设备同步接口

- server设备同步
    - [x] slaver ip记录

### 第二期 任务

- slaver server
    - [ ] 设备操作

- [ ] 任务发布

## 依赖

- [tornado](https://github.com/tornadoweb/tornado)
- [requests](https://github.com/requests/requests)
- [whenconnect](https://github.com/williamfzc/whenconnect)
    - 用于即时设备管理

## 协议

[MIT](LICENSE)
