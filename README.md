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
| `common_module` | 公共模块名 | common |
| `version` | 项目版本 | 1.0.0 |

## language 选项

- **java+kotlin**（默认）：生成 Kotlin 示例源码，构建脚本带完整 Kotlin 工具链（kotlin、kapt、jackson-module-kotlin 等），可自由混写 Java/Kotlin
- **java**：生成纯 Java 示例源码（配置属性为 setter 风格），构建脚本零 Kotlin 痕迹——无 Kotlin 插件、无 kotlin-stdlib 依赖

## 模板演进（copier update）

生成的项目里会保留 `.copier-answers.yml`（**必须提交入库**）。本模板更新后，在生成的项目里执行：

```shell
copier update --trust
```

模板侧的改动会三方合并进项目，冲突按 git 提示手工解决。模板版本由 `copier.yml` 的 `_version` 标记。

## 生成后的项目结构

```
<project>/
├── cli-app/          # Spring Boot CLI 应用模块（bootJar，依赖 common）
│   └── src/main/
│       ├── java/     # language=java 时保留
│       └── kotlin/   # language=java+kotlin 时保留
├── common/           # 公共模块
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
