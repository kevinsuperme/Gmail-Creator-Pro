# -*- coding: utf-8 -*-
"""
Gmail Creator Pro - 带诊断日志的启动包装器
================================================

【设计背景】
原 auto_gmail_creator.exe（PyInstaller 打包）内嵌的 rich 库在 Windows 平台
存在硬编码缺陷：无论 stdout 是什么（tty/管道/文件），都强制走
legacy_windows_render（Win32 控制台 API，使用 GBK 编码），遇到 emoji（如 ✨
\u2728）必然触发 UnicodeEncodeError 崩溃。

经实测：
  - 直接运行（继承真实控制台 + UTF-8 代码页）→ rich 正常渲染，程序正常
  - subprocess 重定向到 PIPE / 文件        → 触发 legacy 路径，程序崩溃

这意味着「实时捕获 stdout 写日志」会破坏程序运行。本启动器采用三段式
务实架构：正常运行优先 + 崩溃时自动诊断捕获。

【工作模式】
  1. 启动前：记录环境元信息、配置文件校验结果到日志
  2. 运行时：直接继承真实控制台运行 exe（程序正常显示，不崩溃）
  3. 崩溃后：若退出码非零，自动用「重定向模式」再跑一次，
             虽然程序仍会崩，但崩溃的完整 traceback 会被捕获到日志，
             提供精确的文件名/行号/错误类型用于排查

【用法】
    python run_with_logging.py
    python run_with_logging.py --target .\auto_gmail_creator.exe
    python run_with_logging.py --no-diagnostic   # 崩溃时不自动诊断
"""

import argparse
import io
import os
import secrets
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

# 将本进程 stdout/stderr 切到 UTF-8，避免启动器自身在 GBK 控制台输出中文/emoji 崩溃
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, io.UnsupportedOperation):
        pass

ROOT_DIR = Path(__file__).resolve().parent
LOG_DIR = ROOT_DIR / "logs"
DEFAULT_TARGET = ROOT_DIR / "auto_gmail_creator.exe"


def generate_strong_password(length: int = 16) -> str:
    """生成强密码，包含大小写字母、数字、特殊字符各至少一个。"""
    uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lowercase = "abcdefghijklmnopqrstuvwxyz"
    digits = "0123456789"
    symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    all_chars = uppercase + lowercase + digits + symbols
    password = [
        secrets.choice(uppercase),
        secrets.choice(lowercase),
        secrets.choice(digits),
        secrets.choice(symbols),
    ] + [secrets.choice(all_chars) for _ in range(length - 4)]
    from random import shuffle
    shuffle(password)
    return "".join(password)


def write_runtime_password(log_path: Path) -> str:
    """生成随机强密码并写入 password.txt，返回密码值。"""
    password = generate_strong_password()
    password_path = ROOT_DIR / "config" / "password.txt"
    password_path.write_text(password, encoding="utf-8")
    log(log_path, f"已生成随机强密码并写入 config/password.txt")
    log(log_path, f"密码: {password}")
    return password


def generate_random_birthday() -> str:
    """生成 1980-2008 年之间的随机生日，格式为 "month day year"。"""
    import random
    year = random.randint(1980, 2008)
    month = random.randint(1, 12)
    if month in [4, 6, 9, 11]:
        max_day = 30
    elif month == 2:
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
            max_day = 29
        else:
            max_day = 28
    else:
        max_day = 31
    day = random.randint(1, max_day)
    return f"{month} {day} {year}"


def write_runtime_birthday(log_path: Path) -> str:
    """生成随机生日并写入 config.py，返回生日值。"""
    birthday = generate_random_birthday()
    config_path = ROOT_DIR / "config" / "config.py"
    content = config_path.read_text(encoding="utf-8")
    content = content.replace(
        'YOUR_BIRTHDAY = ""  # Leave empty for random (1980-2008)',
        f'YOUR_BIRTHDAY = "{birthday}"  # Random generated'
    )
    config_path.write_text(content, encoding="utf-8")
    log(log_path, f"已生成随机生日并写入 config/config.py")
    log(log_path, f"生日: {birthday}")
    return birthday

# 关键配置文件（启动前校验）
REQUIRED_FILES = [
    "config/config.py",
    "config/password.txt",
    "data/names.txt",
]
OPTIONAL_FILES = [
    "config/5sim_config.txt",
    "config/user_agents.txt",
]


def now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def timestamp_file() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def setup_log_file() -> Path:
    """创建带时间戳的日志文件并写入文件头。"""
    LOG_DIR.mkdir(exist_ok=True)
    log_path = LOG_DIR / f"run_{timestamp_file()}.log"
    header = [
        "=" * 70,
        "Gmail Creator Pro 运行日志",
        f"生成时间 : {now_str()}",
        f"工作目录 : {ROOT_DIR}",
        f"Python    : {sys.version.split()[0]}",
        f"平台      : {sys.platform}",
        "=" * 70,
        "",
    ]
    log_path.write_text("\n".join(header), encoding="utf-8")
    return log_path


def log(log_path: Path, *messages: str):
    """向日志文件追加若干行。"""
    with open(log_path, "a", encoding="utf-8") as f:
        for msg in messages:
            f.write(msg + "\n")


def validate_environment(log_path: Path) -> bool:
    """校验配置文件是否就绪，结果写入日志。返回是否全部必需文件存在。"""
    log(log_path, "---- 配置文件校验 ----")
    all_ok = True
    for rel in REQUIRED_FILES:
        ok = (ROOT_DIR / rel).exists()
        status = "OK  " if ok else "MISS"
        log(log_path, f"  [{status}] {rel}  ({'必需' if not ok else ''})")
        if not ok:
            all_ok = False
    for rel in OPTIONAL_FILES:
        ok = (ROOT_DIR / rel).exists()
        status = "OK  " if ok else "WARN"
        log(log_path, f"  [{status}] {rel}  (可选)")
    log(log_path, "")
    return all_ok


def run_direct(target: Path, log_path: Path) -> int:
    """
    直接运行模式：继承真实控制台，让 rich 正常渲染。
    程序正常运行（不触发 GBK 崩溃），代价是无法捕获实时输出。
    """
    log(log_path, "---- 主运行（直接继承控制台）----")
    log(log_path, f"启动时间 : {now_str()}")
    log(log_path, f"目标     : {target.name}")
    log(log_path, f"说明     : 程序输出直接显示在当前控制台，未做重定向以避免 rich GBK 崩溃")
    log(log_path, "")
    log(log_path, "（以下为程序在控制台的实际输出，未写入本日志；如需捕获请看屏幕）")
    log(log_path, "")

    start = time.time()
    print("-" * 70)
    print(f"[启动器] 正在运行 {target.name}（直接模式，输出显示在当前控制台）")
    print("[启动器] 如程序崩溃，启动器将自动进入诊断模式捕获详细错误")
    print("-" * 70)

    # stdin/stdout/stderr 全部继承真实控制台
    proc = subprocess.Popen([str(target)], cwd=str(ROOT_DIR))
    try:
        exit_code = proc.wait()
    except KeyboardInterrupt:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
        exit_code = -1
        log(log_path, "运行被用户中断 (Ctrl+C)")
    elapsed = time.time() - start

    log(log_path, f"结束时间 : {now_str()}")
    log(log_path, f"退出码   : {exit_code}")
    log(log_path, f"耗时     : {elapsed:.1f} 秒")
    log(log_path, "")
    return exit_code


def run_diagnostic(target: Path, log_path: Path, timeout: float = 8.0) -> bool:
    """
    诊断模式：重定向 stdout 到文件，故意触发 rich 崩溃以捕获完整 traceback。
    虽然程序会崩，但崩溃栈（文件名/行号/错误类型）会被完整记录，用于排查。
    :return: 是否成功捕获到诊断信息
    """
    log(log_path, "---- 崩溃诊断模式 ----")
    log(log_path, "说明：检测到程序异常退出，启动诊断模式捕获详细错误堆栈。")
    log(log_path, "      诊断模式下程序本身仍会因 rich 缺陷崩溃，但崩溃信息将被完整记录。")
    log(log_path, "")

    # 注入 UTF-8 环境，让崩溃前的部分输出尽量可读
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"

    diag_file = LOG_DIR / f"diagnostic_{timestamp_file()}.log"
    try:
        with open(diag_file, "w", encoding="utf-8") as out:
            proc = subprocess.Popen(
                [str(target)],
                cwd=str(ROOT_DIR),
                stdin=subprocess.DEVNULL,    # 诊断模式不交互
                stdout=out,
                stderr=subprocess.STDOUT,
                env=env,
            )
            try:
                proc.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                proc.terminate()
                try:
                    proc.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    proc.kill()
    except Exception as e:
        log(log_path, f"诊断模式执行失败: {type(e).__name__}: {e}")
        return False

    # 读取诊断输出，提取关键错误信息
    try:
        content = diag_file.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return False

    log(log_path, f"诊断输出文件 : {diag_file}")
    log(log_path, "诊断捕获内容（原始）：")
    log(log_path, "-" * 70)
    # 逐行写入日志（去除纯乱码的空行）
    for line in content.splitlines():
        log(log_path, f"  {line}")
    log(log_path, "-" * 70)
    log(log_path, "")
    return bool(content.strip())


def write_summary(log_path: Path, exit_code: int, diag_done: bool,
                  crashed: bool, note: str = ""):
    """写入运行总结。"""
    sep = "=" * 70
    summary = [
        "",
        sep,
        "运行总结 / RUN SUMMARY",
        sep,
        f"结束时间       : {now_str()}",
        f"最终退出码     : {exit_code}",
        f"是否崩溃       : {'是' if crashed else '否'}",
        f"是否执行诊断   : {'是' if diag_done else '否'}",
    ]
    if note:
        summary.append(f"备注           : {note}")
    summary.append(sep)

    with open(log_path, "a", encoding="utf-8") as f:
        f.write("\n".join(summary) + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="带诊断日志的 Gmail Creator Pro 启动器"
    )
    parser.add_argument(
        "--target", default=str(DEFAULT_TARGET),
        help="目标可执行文件路径（默认 auto_gmail_creator.exe）"
    )
    parser.add_argument(
        "--no-diagnostic", action="store_true",
        help="崩溃时不自动进入诊断模式"
    )
    parser.add_argument(
        "--count", type=int, default=1,
        help="创建账户数量（默认 1，每个账户独立密码和生日）"
    )
    args = parser.parse_args()

    target = Path(args.target)
    if not target.exists():
        print(f"[启动器] 错误：找不到目标文件 {target}", file=sys.stderr)
        sys.exit(2)

    log_path = setup_log_file()

    print(f"[启动器] 日志文件 : {log_path}")
    print(f"[启动器] 目标程序 : {target.name}")
    print(f"[启动器] 创建数量 : {args.count} 个（每个独立密码和生日）")
    print(f"[启动器] 说明     : 直接运行模式，程序输出显示在控制台")
    print(f"[启动器] 已知限制 : 原 exe 的 rich 库在 Windows 下重定向输出会触发 GBK 崩溃，")
    print(f"                   故本启动器不做实时 stdout 捕获，改为「正常运行 + 崩溃诊断」机制")
    print("=" * 70)

    # 环境校验
    env_ok = validate_environment(log_path)
    if not env_ok:
        print("[启动器] 警告：部分必需配置文件缺失，程序可能无法正常运行")
        print("[启动器] 请参阅 docs/02-环境配置与安装.md 完成配置")
        log(log_path, "警告：配置文件校验未通过，继续运行但可能失败。")
        log(log_path, "")

    # 批量创建模式：每个账户生成独立密码和生日
    exit_code = 0
    for i in range(args.count):
        print(f"\n{'=' * 70}")
        print(f"[启动器] 第 {i + 1}/{args.count} 个账户")
        print(f"{'=' * 70}")

        # 生成随机生日（1980-2008）
        print("[启动器] 正在生成随机生日...")
        birthday = write_runtime_birthday(log_path)
        print(f"[启动器] 生日已生成: {birthday}")

        # 生成随机强密码
        print("[启动器] 正在生成随机强密码...")
        password = write_runtime_password(log_path)
        print(f"[启动器] 密码已生成（长度: {len(password)} 字符）")

        # 运行 exe
        print("[启动器] 正在启动程序...")
        batch_exit = run_direct(target, log_path)
        
        if batch_exit != 0:
            exit_code = batch_exit
            if not args.no_diagnostic:
                print("-" * 70)
                print(f"[启动器] 检测到程序异常退出（退出码 {batch_exit}），启动诊断模式...")
                run_diagnostic(target, log_path)
            else:
                print(f"[启动器] 程序异常退出，退出码: {batch_exit}")

        # 非最后一个账户，提示等待
        if i < args.count - 1:
            print(f"[启动器] 第 {i + 1} 个账户完成，等待 5 秒后继续...")
            time.sleep(5)

    # 崩溃处理
    crashed = exit_code != 0
    diag_done = False
    note = ""
    if crashed and not args.no_diagnostic:
        print("-" * 70)
        print(f"[启动器] 检测到程序异常退出（退出码 {exit_code}），启动诊断模式捕获错误...")
        diag_done = run_diagnostic(target, log_path)
        if diag_done:
            print(f"[启动器] 诊断信息已写入日志：{log_path}")
            note = "已通过诊断模式捕获崩溃堆栈，详见日志「崩溃诊断模式」段落"
        else:
            note = "诊断模式未能捕获额外信息"
    elif crashed:
        note = "已禁用诊断模式（--no-diagnostic）"

    # 总结
    write_summary(log_path, exit_code, diag_done, crashed, note)

    print("=" * 70)
    print(f"[启动器] 运行结束，退出码: {exit_code}")
    print(f"[启动器] 完整日志: {log_path}")
    if crashed and diag_done:
        print(f"[启动器] 崩溃堆栈已捕获，请查阅日志中的「崩溃诊断模式」段落定位问题")
    elif crashed:
        print(f"[启动器] 程序异常退出，如需捕获错误详情请去掉 --no-diagnostic 重新运行")
    else:
        print(f"[启动器] 程序正常退出。")

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
