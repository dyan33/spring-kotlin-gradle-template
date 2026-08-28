# AGENTS.md

本仓库是 **copier 项目模板**（生成 Spring Boot CLI 项目，创建时可选择 `java` 或 `java+kotlin`），本身不是可运行的应用。

## 目录结构

- `copier.yml` — 模板配置：问题定义（`project_name` / `language` / `group_id` / `artifact_id` / `version`，`language` 为 choice：`java+kotlin` 默认，`java` 纯 Java 零 Kotlin）、12 个可选依赖布尔问题（`use_druid` / `use_pagehelper` / `use_mybatis_plus` / `use_redisson` / `use_tencent_cos` / `use_aws_s3` / `use_easyexcel` / `use_validation` / `use_knife4j` / `use_guava` / `use_commons_io` / `use_fastjson`，默认全 false）、`_subdirectory: template`、`_version`（模板版本锚点）、`_tasks`
- `post_gen.py` — 生成后处理脚本（由 `_tasks` 调用，cwd 为生成的项目目录）：按 `language` 保留一棵源码树，把源码从 `com/example/cli` 搬到 `group_id` 包路径，重命名 `cli-app` → `artifact_id`。**必须保持幂等**——copier update 会重跑它
- `template/` — 模板工程本体（`_subdirectory` 指向），单应用模块 Gradle 工程：
  - `cli-app/` — Spring Boot CLI 应用模块（bootJar），源码为 `src/main/java` 与 `src/main/kotlin` **并行两棵树**（内容一一对应，靠 post_gen.py 二选一）；`use_knife4j` 选项通过 jinja 条件目录段（`[[% if use_knife4j %]]config[[% endif %]]`）控制 SwaggerConfig 是否生成
  - 带 `.jinja` 后缀的文件参与渲染，其余文件原样复制

## 模板约定（copier）

- 定界符：变量 `[[ x ]]`，语句块 `[[% if ... %]]` / `[[% endif %]]`；引用问题名**没有** `cookiecutter.` 前缀
- 占位符只允许出现在 `.jinja` 文件中；新增含占位符的文件必须加 `.jinja` 后缀，否则 copier 原样复制、不渲染
- `language` 条件统一写 `[[% if language == 'java+kotlin' %]]`；选 `java` 的生成物必须零 Kotlin 痕迹（无 Kotlin 插件、kapt、kotlin-stdlib、jackson-module-kotlin）
- 可选依赖默认关闭、仅加依赖不改配置：新增一项需同时改三处——copier.yml 布尔问题、根 build.gradle.jinja 的 dependencyManagement 版本条目（Boot BOM 管版本的除外）、cli-app/build.gradle.jinja 的 implementation 条件块；版本以 Boot 2.7.18 / Java 8 兼容为准，不照搬参考项目

## 模板修改规则（重要）

- 模板演进必须提交 git 并升级 `copier.yml` 的 `_version`（建议打同名 tag），已生成项目才能通过 `copier update` 感知到变化
- `template/.copier-answers.yml.jinja` 是 answers 文件的来源，**不可删除**——copier 9.x 的 copy 不会自动生成 answers 文件，没有它 `copier update` 无法工作
- `_tasks` 字符串与模板文件共用 `_envops` 定界符（`[[ ]]`）；模板仓库自身路径用 `[[ _copier_conf.src_path ]]`（9.x 没有 `_template_src`）
- `post_gen.py` 中的 mv/rm 必须带存在性守卫且目录搬运用 `merge_move` 递归合并（`shutil.move` 遇已存在目录会把源塞进去，update 重跑即产生嵌套目录）
- `copier update` 要求生成项目工作区干净（含未跟踪文件），有未跟踪产物时先 `git clean -fd`
- 示例逻辑在 `src/main/java`（setter 风格、Java 8 无 record）和 `src/main/kotlin` 两棵树各有一份，**改动示例必须两棵树同步修改**并保持行为一致
- 生成项目里的 `.copier-answers.yml` 必须提交入库，`copier update` 依赖它做三方合并
- 不能在 `template/` 里直接构建：须先 `copier copy` 渲染到临时目录再操作

## 构建命令

在渲染后的项目内执行：

```shell
./gradlew --stop
./gradlew clean
./gradlew -x test ':cli-app:build'
```

构建须用 JDK 11（本机 `setjdk11` 别名；非交互 shell 直接 `export JAVA_HOME='/Users/dengcg/Library/Java/JavaVirtualMachines/temurin-11.0.24/Contents/Home'`）。JDK 17+ 会导致 Kotlin 编译器内部错误（`javaslang.λ` ClassNotFound），Gradle 7.6.6 本身也不支持 Java 20+。

## 技术栈与约束

- Spring Boot 2.7.18、Kotlin 1.9.25、目标 JVM 1.8（`jvmTarget = JVM_1_8`），不能使用 Java 8 之后的 API
- Gradle 7.6.6，**Groovy DSL**（`build.gradle`），不是 Kotlin DSL
- 依赖版本统一在根 `build.gradle` 的 `dependencyManagement` 中声明，子模块依赖不写版本号
- Maven 仓库走阿里云镜像（central/public/spring），Gradle Wrapper 下载走腾讯镜像；新增仓库时保持国内镜像优先
- 主要依赖：MyBatis（mybatis-spring-boot-starter）、MySQL、retrofit-spring-boot-starter、hutool-crypto + bouncycastle（SM2 国密加密）、kapt
- `application.yaml` 配置属性用 kebab-case（如 `public_key`），映射到 camelCase 字段（Kotlin 版构造器绑定，Java 版 setter 绑定）

## 文档

- `README.md` — copier 用法与 update 工作流
