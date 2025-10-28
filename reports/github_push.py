# reports/github_push.py
import argparse, os, subprocess, sys
from pathlib import Path
from datetime import datetime

def run(cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, check=True, text=True,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-dir", default="/app/gitrepo") # 컨테이너 내 임시 clone
    ap.add_argument("--remote", default=os.getenv("GITHUB_REPO",""))
    ap.add_argument("--src", required=True)  # reports/YYYY-MM-DD 폴더
    ap.add_argument("--dst", default="reports")  # 리포의 저장 경로
    args = ap.parse_args()

    if not args.remote:
        print("GITHUB_REPO not set"); sys.exit(1)

    repo_dir = Path(args.repo_dir)
    if repo_dir.exists():
        run(["rm","-rf",str(repo_dir)])
    run(["git","clone",args.remote,str(repo_dir)])
    # 복사
    src = Path(args.src)
    dst = repo_dir/args.dst/src.name
    dst.parent.mkdir(parents=True, exist_ok=True)
    run(["mkdir","-p",str(dst)])
    run(["cp","-r",str(src)+"/.","",str(dst)], cwd=None)  # busybox/gnu 차이에 주의 → 대안 아래
    # 안전한 복사(파이썬)
    # from distutils.dir_util import copy_tree; copy_tree(str(src), str(dst))

    # git 설정
    author = os.getenv("GIT_AUTHOR_NAME","autobot")
    email  = os.getenv("GIT_AUTHOR_EMAIL","autobot@example.com")
    run(["git","config","user.name", author], cwd=repo_dir)
    run(["git","config","user.email", email], cwd=repo_dir)

    # 커밋 & 푸시
    run(["git","add","-A"], cwd=repo_dir)
    ts = datetime.utcnow().isoformat()
    run(["git","commit","-m",f"chore: add reports {src.name} ({ts})"], cwd=repo_dir)
    run(["git","push"], cwd=repo_dir)
    print("[git] pushed to remote.")

if __name__=="__main__":
    main()
