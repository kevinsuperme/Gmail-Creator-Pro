# -*- coding: utf-8 -*-
"""
配置生成器 - 为 Gmail Creator Pro 生成动态配置

功能：
  1. 生成 1980-2008 年之间的随机生日
  2. 为每个账户生成独立的强密码
  3. 扩充 names.txt 到 500 条不重复姓名

使用方式：
    python generate_config.py       # 生成所有配置
    python generate_config.py --names-only  # 仅生成姓名库
    python generate_config.py --password-only  # 仅生成单个随机密码
"""

import argparse
import random
import secrets
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
DATA_DIR = ROOT_DIR / "data"
CONFIG_DIR = ROOT_DIR / "config"


# ===== 姓名生成模块 =====
MALE_FIRST_NAMES = [
    "Ahmed", "Mohamed", "Omar", "Ibrahim", "Mahmoud", "Hassan", "Hussein",
    "Khaled", "Mostafa", "Youssef", "Karim", "Amr", "Ayman", "Hossam",
    "Sherif", "Tarek", "Waleed", "Sameh", "Ramy", "Nour", "Sayed", "Ismail",
    "Abdallah", "Khalil", "Soliman", "Kamel", "Samir", "Othman", "Fouad",
    "Zaki", "Gamal", "Farid", "Mansour", "Adel", "Salem", "John", "Michael",
    "David", "James", "Robert", "William", "Richard", "Joseph", "Thomas",
    "Charles", "Daniel", "Matthew", "Anthony", "Mark", "Donald", "Steven",
    "Paul", "Andrew", "Joshua", "Kenneth", "Kevin", "Brian", "George",
    "Timothy", "Ronald", "Edward", "Jason", "Jeffrey", "Ryan", "Jacob",
    "Gary", "Nicholas", "Eric", "Stephen", "Jonathan", "Larry", "Justin",
    "Scott", "Brandon", "Benjamin", "Samuel", "Gregory", "Frank", "Alexander",
    "Raymond", "Patrick", "Jack", "Dennis", "Jerry", "Tyler", "Aaron",
    "Jose", "Adam", "Henry", "Douglas", "Nathan", "Peter", "Zachary",
    "Walter", "Kyle", "Harold", "Carl", "Jeremy", "Keith", "Roger",
    "Gerald", "Ethan", "Arthur", "Lawrence", "Terry", "Sean", "Christian",
    "Austin", "Noah", "Dylan", "Jesse", "Jordan", "Bryan", "Billy",
    "Joe", "Bruce", "Willie", "Gabriel", "Logan", "Alan", "Juan",
    "Wayne", "Roy", "Ralph", "Randy", "Eugene", "Vincent", "Russell",
    "Bobby", "Philip", "Louis", "Johnny", "Elijah", "Isaac", "Isaiah",
    "Liam", "Mason", "Ethan", "Lucas", "Oliver", "Elijah", "William",
    "James", "Benjamin", "Jacob", "Michael", "Ethan", "Alexander",
]

FEMALE_FIRST_NAMES = [
    "Fatma", "Aisha", "Mariam", "Sara", "Nada", "Heba", "Rana", "Mona",
    "Amira", "Dina", "Yasmin", "Reem", "Layla", "Manal", "Hala", "Noura",
    "Ghada", "Samar", "Dalia", "Safa", "Nabilah", "Faten", "Zainab",
    "Nouran", "Raneem", "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth",
    "Barbara", "Susan", "Jessica", "Sarah", "Margaret", "Lisa", "Nancy",
    "Karen", "Betty", "Helen", "Sandra", "Donna", "Carol", "Ruth", "Sharon",
    "Michelle", "Laura", "Sarah", "Kimberly", "Deborah", "Jessica", "Shirley",
    "Cynthia", "Angela", "Melissa", "Brenda", "Amy", "Anna", "Rebecca",
    "Virginia", "Kathleen", "Pamela", "Martha", "Debra", "Amanda", "Stephanie",
    "Carolyn", "Christine", "Marie", "Janet", "Catherine", "Frances",
    "Ann", "Joyce", "Diane", "Alice", "Julie", "Heather", "Teresa",
    "Doris", "Gloria", "Evelyn", "Jean", "Cheryl", "Mildred", "Katherine",
    "Joan", "Ashley", "Judith", "Rose", "Janice", "Kim", "Theresa",
    "Lisa", "Nicole", "Grace", "Denise", "Wanda", "Beverly", "Diana",
    "Stacy", "Emma", "Olivia", "Ava", "Isabella", "Sophia", "Charlotte",
    "Amelia", "Mia", "Harper", "Evelyn", "Abigail", "Emily", "Elizabeth",
    "Mila", "Ella", "Avery", "Sofia", "Camila", "Aria", "Scarlett",
    "Victoria", "Madison", "Luna", "Grace", "Chloe", "Penelope", "Layla",
]

LAST_NAMES = [
    "Mohamed", "Ali", "Ibrahim", "Mahmoud", "Hassan", "Hussein", "Khaled",
    "Mostafa", "Youssef", "Karim", "Amr", "Ayman", "Hossam", "Sherif",
    "Tarek", "Waleed", "Sameh", "Ramy", "Nour", "Sayed", "Ismail",
    "Abdallah", "Khalil", "Soliman", "Kamel", "Samir", "Othman", "Fouad",
    "Zaki", "Gamal", "Farid", "Mansour", "Adel", "Salem", "Smith", "Johnson",
    "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez",
    "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
    "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez",
    "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis",
    "Robinson", "Walker", "Young", "Allen", "King", "Wright", "Scott",
    "Torres", "Nguyen", "Hill", "Flores", "Green", "Adams", "Nelson",
    "Baker", "Hall", "Rivera", "Campbell", "Mitchell", "Carter", "Roberts",
    "Gomez", "Phillips", "Evans", "Turner", "Diaz", "Parker", "Cruz",
    "Edwards", "Collins", "Reyes", "Stewart", "Morris", "Morales", "Murphy",
    "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan", "Cooper", "Peterson",
    "Bailey", "Reed", "Kelly", "Howard", "Ramos", "Kim", "Cox", "Ward",
    "Richardson", "Watson", "Brooks", "Chavez", "Wood", "James", "Bennett",
    "Gray", "Mendoza", "Ruiz", "Hughes", "Price", "Alvarez", "Castillo",
    "Sanders", "Patel", "Myers", "Long", "Ross", "Foster", "Jimenez",
]


def generate_names(count: int = 500) -> list[str]:
    """生成指定数量的不重复姓名。"""
    names = set()
    while len(names) < count:
        gender = random.choice(["male", "female"])
        if gender == "male":
            first = random.choice(MALE_FIRST_NAMES)
        else:
            first = random.choice(FEMALE_FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        names.add(f"{first} {last}")
    return sorted(list(names))


def save_names(names: list[str], file_path: Path):
    """将姓名列表写入文件。"""
    file_path.write_text("\n".join(names), encoding="utf-8")


# ===== 密码生成模块 =====
def generate_strong_password(length: int = 16) -> str:
    """生成强密码，包含大小写字母、数字、特殊字符。"""
    uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lowercase = "abcdefghijklmnopqrstuvwxyz"
    digits = "0123456789"
    symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    all_chars = uppercase + lowercase + digits + symbols
    
    # 确保包含每种类型至少一个字符
    password = [
        secrets.choice(uppercase),
        secrets.choice(lowercase),
        secrets.choice(digits),
        secrets.choice(symbols),
    ]
    
    # 填充剩余长度
    password += [secrets.choice(all_chars) for _ in range(length - 4)]
    
    # 打乱顺序
    random.shuffle(password)
    
    return "".join(password)


def generate_password_list(count: int = 500) -> list[str]:
    """生成指定数量的不重复强密码。"""
    passwords = set()
    while len(passwords) < count:
        passwords.add(generate_strong_password())
    return list(passwords)


def save_password(password: str, file_path: Path):
    """将密码写入文件。"""
    file_path.write_text(password, encoding="utf-8")


# ===== 生日生成模块 =====
def generate_random_birthday() -> str:
    """生成 1980-2008 年之间的随机生日，格式为 "month day year"。"""
    year = random.randint(1980, 2008)
    month = random.randint(1, 12)
    
    # 根据月份确定天数
    if month in [4, 6, 9, 11]:
        max_day = 30
    elif month == 2:
        # 处理闰年
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
            max_day = 29
        else:
            max_day = 28
    else:
        max_day = 31
    
    day = random.randint(1, max_day)
    
    return f"{month} {day} {year}"


# ===== 配置文件修改模块 =====
def update_config_file(config_path: Path):
    """更新 config.py，设置动态生成标记（空值表示运行时生成）。"""
    content = config_path.read_text(encoding="utf-8")
    
    # 统一设置为空值标记，由运行时脚本生成具体值
    content = content.replace(
        'YOUR_BIRTHDAY = "2 4 1950"  # Format: "month day year"',
        'YOUR_BIRTHDAY = ""  # Leave empty for random (1980-2008)'
    )
    content = content.replace(
        'YOUR_BIRTHDAY = ""  # Leave empty for random (1980-2008)',
        'YOUR_BIRTHDAY = ""  # Leave empty for random (1980-2008)'
    )
    content = content.replace(
        'YOUR_BIRTHDAY = "',
        'YOUR_BIRTHDAY = ""  # Leave empty for random (1980-2008)'
    )
    
    # 将固定密码改为空（让程序运行时动态生成）
    content = content.replace(
        'YOUR_PASSWORD = ""  # Leave empty to read from password.txt',
        'YOUR_PASSWORD = ""  # Leave empty for random strong password'
    )
    content = content.replace(
        'YOUR_PASSWORD = ""  # Leave empty for random strong password',
        'YOUR_PASSWORD = ""  # Leave empty for random strong password'
    )
    
    config_path.write_text(content, encoding="utf-8")


# ===== 主函数 =====
def main():
    parser = argparse.ArgumentParser(description="配置生成器")
    parser.add_argument(
        "--names-only", action="store_true",
        help="仅生成姓名库"
    )
    parser.add_argument(
        "--password-only", action="store_true",
        help="仅生成一个随机密码"
    )
    parser.add_argument(
        "--count", type=int, default=500,
        help="生成数量（默认 500）"
    )
    args = parser.parse_args()

    if args.password_only:
        # 仅生成单个密码
        password = generate_strong_password()
        print(f"随机强密码: {password}")
        return

    print("=" * 70)
    print("Gmail Creator Pro 配置生成器")
    print("=" * 70)

    if not args.names_only:
        # 更新 config.py
        print("1. 更新 config.py 配置...")
        update_config_file(CONFIG_DIR / "config.py")
        print("   ✓ 已将生日改为动态生成（1980-2008）")
        print("   ✓ 已将密码改为动态生成（独立强密码）")

    # 生成姓名库
    print("2. 生成姓名库...")
    names = generate_names(args.count)
    save_names(names, DATA_DIR / "names.txt")
    print(f"   ✓ 已生成 {len(names)} 条不重复姓名")
    print(f"   ✓ 文件: {DATA_DIR / 'names.txt'}")

    print("=" * 70)
    print("配置生成完成！")
    print("=" * 70)


if __name__ == "__main__":
    main()
