import os

app_dir="cli-app/src/main/kotlin/{{cookiecutter.group_id}}".replace(".", os.sep)

os.makedirs(app_dir, exist_ok=True)

os.rename("common","{{cookiecutter.common_module}}")

os.system("mv cli-app/src/main/kotlin/com/example/cli/* "+app_dir)
os.system("rm -rf cli-app/src/main/kotlin/com/example/cli/")
os.system("mv cli-app {{cookiecutter.artifact_id}}")
