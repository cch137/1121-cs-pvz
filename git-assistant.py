import os
import json

cache_filepath = 'dev-assistant.json'

branch_name: str = ''

def show_branch_name():
    global branch_name
    print()
    print('Your branch:', branch_name)

def switch_c_branch():
    global branch_name
    print()
    status = os.system(f'git switch -c {branch_name}')
    if status != 0:
        print()
        print('創建失敗！')
        return False
    return True

def switch_branch():
    global branch_name
    print()
    status = os.system(f'git switch {branch_name}')
    if status != 0:
        print()
        print('切換失敗！')
        return False
    return True

def input_branch():
    print()
    global branch_name
    is_new_branch = input('你是否要創建一個新的 branch？(Y/N) ').strip().upper() == 'Y'
    branch_name = input('請輸入你的 branch 名稱：')
    if is_new_branch:
        if not switch_c_branch():
            return False
    elif not switch_branch():
        return False
    with open(cache_filepath, 'w') as f:
        f.write(json.dumps({ "branch": branch_name }))
    return True

def get_choose(input_prompt = ''):
    try: return int(input(input_prompt))
    except: return -1

def git_add():
    print()
    os.system('git add .')

def git_commit():
    print()
    message = input('Commit message: ')
    git_add()
    os.system(f'git commit -m "{message}"')

def git_push():
    print()
    os.system(f'git push')

def git_pull_origin_main():
    print()
    os.system('git fetch')
    os.system('git pull origin main')
    os.system('git push')

def git_reset():
    print()
    print('請選擇：')
    print('1 - 還原到最近一次的提交狀態 (commit)')
    print('2 - 還原到最近一次暫存 (add)')
    action = get_choose()
    if input('你確定？(Y/N) ').strip().upper() == 'Y':
        print()
        match action:
            case 1:
                os.system('git reset --hard HEAD')
            case 2:
                os.system('git reset --hard')
    else: print('操作已取消。')

def take_action():
    print()
    print('請選擇操作（輸入數字）：')
    print('1 - 將 branch 同步到最新版本')
    print('2 - 暫存（add）')
    print('3 - 提交 (commit)')
    print('4 - 推送 (push)')
    print('5 - 提交 & 推送 (commit & push)')
    print('9 - 放棄當前更改')
    action = get_choose()
    match action:
        case 1:
            git_pull_origin_main()
        case 2:
            git_add()
        case 3:
            git_commit()
        case 4:
            git_push()
        case 5:
            git_commit()
            git_push()
        case 9:
            git_reset()
        case _:
            print()
            print(':)')

def main():
    global branch_name
    if not os.path.exists(cache_filepath):
        if not input_branch():
            return
    else:
        branch_name = json.loads(open(cache_filepath, 'r').read()).get('branch')
        if not branch_name:
            if not input_branch():
                return
    
    show_branch_name()

    take_action()

if __name__ == '__main__':
    main()