


## 项目构建
```shell
./gradlew --stop
./gradlew clean
./gradlew -x test ':{{cookiecutter.artifact_id}}:build' --nodaemon
```