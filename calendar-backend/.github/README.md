# GitHub Actions 工作流

此目录包含项目的GitHub Actions工作流配置文件。

## 后端每周任务 (backend-weekly.yml)

这个工作流每周一凌晨2点(UTC时间)自动运行，执行以下后端维护任务：

1. 为下周生成默认的可用时间槽
2. 清理两周前的过期数据

### 环境变量

工作流使用以下GitHub Secrets：

- `DATABASE_URL`: MongoDB数据库连接字符串

### 手动触发

除了定时执行外，还可以通过GitHub UI手动触发工作流。

## 配置管理

若需修改工作流配置：

1. 编辑 `.github/workflows/backend-weekly.yml` 文件
2. 在GitHub仓库的Settings -> Secrets and variables -> Actions中管理环境变量 