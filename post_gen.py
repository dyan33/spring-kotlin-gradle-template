"""生成后处理（由 copier.yml 的 _tasks 调用，cwd 为生成的项目目录）。

必须保持幂等：copier update 会重跑本脚本，任何 mv/rm 都要有存在性守卫。
用法：post_gen.py <language> <artifact_id> <group_id>
"""
import os
import shutil
import sys

language, artifact_id, group_id = sys.argv[1:4]


def merge_move(src: str, dst: str) -> None:
    """src 搬到 dst；dst 已是目录时递归合并内容（update 重跑必须幂等）。"""
    if os.path.isdir(src) and os.path.isdir(dst):
        for name in os.listdir(src):
            merge_move(os.path.join(src, name), os.path.join(dst, name))
        os.rmdir(src)
    else:
        shutil.move(src, dst)


# 两棵源码树并行维护，生成时必须只保留一棵，否则同名类冲突
trees = {
    'java': ('cli-app/src/main/java', 'cli-app/src/main/kotlin'),
    'java+kotlin': ('cli-app/src/main/kotlin', 'cli-app/src/main/java'),
}
keep_dir, drop_dir = trees[language]
if os.path.exists(drop_dir):
    shutil.rmtree(drop_dir)

# 包路径搬迁：模板内固定 com/example/cli → group_id 对应路径
src_pkg = os.path.join(keep_dir, 'com', 'example', 'cli')
if os.path.exists(src_pkg):
    app_dir = os.path.join(keep_dir, *group_id.split('.'))
    os.makedirs(app_dir, exist_ok=True)
    for name in os.listdir(src_pkg):
        merge_move(os.path.join(src_pkg, name), os.path.join(app_dir, name))
    shutil.rmtree(src_pkg)
    # 清理搬迁后残留的空目录链（如 com/example）
    try:
        os.removedirs(os.path.dirname(src_pkg))
    except OSError:
        pass

# 模块改名（空答案直接跳过，避免 rename 到空路径崩溃）
if artifact_id and artifact_id != 'cli-app' and not os.path.exists(artifact_id):
    os.rename('cli-app', artifact_id)
