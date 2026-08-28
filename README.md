# spring boot 项目模板

基于 [copier](https://copier.readthedocs.io/) 的 Spring Boot 项目模板，生成 Gradle 多模块 CLI 工程，支持 Java 或 Java+Kotlin 混合开发。

## 创建项目

```shell
copier copy <本仓库路径或 git 地址> my-project
```

按提示输入以下变量：

| 变量 | 说明 | 默认值 |
|---|---|---|
| `project_name` | 项目名 | Spring Boot Kotlin Gradle Project |
| `language` | 项目语言：`java+kotlin`（混合）或 `java`（纯 Java） | java+kotlin |
| `group_id` | 包名 / Maven groupId | com.example |
| `artifact_id` | 应用模块名 / Maven artifactId | cli-app |
| `version` | 项目版本 | 1.0.0 |

## language 选项

- **java+kotlin**（默认）：生成 Kotlin 示例源码，构建脚本带完整 Kotlin 工具链（kotlin、kapt、jackson-module-kotlin 等），可自由混写 Java/Kotlin
- **java**：生成纯 Java 示例源码（配置属性为 setter 风格），构建脚本零 Kotlin 痕迹——无 Kotlin 插件、无 kotlin-stdlib 依赖

## 可选依赖

创建时按需选择，默认全部关闭；仅引入依赖，不改动配置与示例代码。版本已按 Boot 2.7.18 / Java 8 适配：

| 分组 | 选项 | 引入内容 |
|---|---|---|
| 数据层 | `use_druid` / `use_pagehelper` / `use_mybatis_plus` | Druid 连接池 / PageHelper 分页（1.4.7）/ MyBatis-Plus（3.5.1） |
| 中间件与云服务 | `use_redisson` / `use_tencent_cos` / `use_aws_s3` | Redisson（3.19.0，已适配 Boot 2.7）/ 腾讯云 COS+STS / AWS S3+STS（1.12.261） |
| 应用功能 | `use_easyexcel` / `use_validation` / `use_web` | EasyExcel / Bean Validation / Web MVC（spring-boot-starter-web + WebMvcConfig JSON 定制 + knife4j 接口文档） |
| 工具库 | `use_guava` / `use_commons_io` / `use_fastjson` | Guava（31.1-jre）/ commons-io / fastjson |

`use_web` 生成 `WebMvcConfig`（统一 JSON 序列化：`LocalDateTime → yyyy-MM-dd HH:mm:ss`、`LocalDate → yyyy-MM-dd`、忽略未知字段等），并连带引入 knife4j 接口文档；Boot 2.7 下启动文档需配 `spring.mvc.pathmatch.matching-strategy=ant_path_matcher`，属使用时自行配置。

## 模板演进（copier update）

生成的项目里会保留 `.copier-answers.yml`（**必须提交入库**）。本模板更新后，在生成的项目里执行：

```shell
copier update --trust
```

模板侧的改动会三方合并进项目，冲突按 git 提示手工解决。模板版本由 `copier.yml` 的 `_version` 标记。

## 生成后的项目结构

```
<project>/
├── cli-app/          # Spring Boot CLI 应用模块（bootJar，单模块工程）
│   └── src/main/
│       ├── java/     # language=java 时保留
│       └── kotlin/   # language=java+kotlin 时保留
├── build.gradle      # 根构建脚本，依赖版本集中在 dependencyManagement
├── settings.gradle
├── Makefile          # 构建快捷命令
└── .copier-answers.yml
```

## 构建命令

在生成的项目根目录执行（需 JDK 11）：

```shell
./gradlew --stop
./gradlew clean
./gradlew -x test ':cli-app:build'
```

## 技术栈

- Spring Boot 2.7.18 / Kotlin 1.9.25 / 目标 JDK 1.8 / Gradle 7.6.6
- MyBatis（mybatis-spring-boot-starter）、MySQL、retrofit-spring-boot-starter
- hutool-crypto + BouncyCastle（SM2 国密加密）
- Maven 依赖走阿里云镜像，Gradle Wrapper 走腾讯镜像
