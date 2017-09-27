import re, json
import os
import time
reg = '[0-9a-f]{40}'

OPENSSL_PATH = '/Users/fangdongliang/Desktop/openssl/'
DIFF_PATH = '/Users/fangdongliang/Desktop/difference/'


def a_temp_test():
    with open('res.json', 'r') as infile:
        m_commit = json.load(infile)
        the_list = m_commit['c-d']
        for item in the_list:
            extra_file(dirname='c-d', commit_id=item)

def format_resolve():
    m_set = {}
    with open('commit_id.txt', 'r') as infile:
        idx = ""
        line = "11111"
        while len(line) > 0:
            line = infile.readline()
            length = len(line)
            if length >= 40:
                m_set[idx] += re.findall(reg, line)
            if length == 4:
                if idx != "":
                    m_set[idx] = list(set(m_set[idx]))
                idx = line[0:3]
                m_set[idx] = []
    with open('res.json', 'w') as outfile:
        outfile.write(json.dumps(m_set, indent=1))

def extra_file(dirname, commit_id):
    """
    this function aims to extra two files (origin and changed!)
    according to current commit_id and 'git diff'
    utilizing current commit id and the commit id before
    """
    regex = 'commit ([0-9a-f]{40})\nAuthor'
    LOG_HEAD = 20
    S_COUNT = 1
    os.chdir(OPENSSL_PATH)
    reset_version = "git reset --hard " + commit_id + " > /dev/null"
    os.system(reset_version)
    git_log = "git log| head -n " + str(LOG_HEAD)
    logs = os.popen(git_log).read()
    commit_ids = re.findall(regex, logs, re.S|re.M)
    while len(commit_ids) < 2:
        S_COUNT *= 2
        LOG_HEAD *= S_COUNT
        git_log = "git log| head -n " + str(LOG_HEAD)
        logs = os.popen(git_log).read()
        commit_ids = re.findall(regex, logs, re.S|re.M)
        if S_COUNT >= 16:
            raise ChildProcessError
    git_diff = "git diff " + commit_ids[0] + " " + commit_ids[1]
    diff_context = os.popen(git_diff).readline()
    filename_arr = diff_context.split()
    if len(filename_arr) != 4:
        return False
    else:
        filename = filename_arr[2][2:]
        dir_path = DIFF_PATH + dirname
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        current_commit_path = dir_path + "/" + commit_id[0:8]
        if not os.path.exists(current_commit_path):
            os.mkdir(current_commit_path)
        target_file = OPENSSL_PATH + filename
        dst_file_changed = current_commit_path + "/" + "ch_" + filename.split('/')[-1]
        copy_cmd = 'cp ' + target_file + ' ' + dst_file_changed
        os.system(copy_cmd)
        reset_version = "git reset --hard " + commit_ids[1] + " > /dev/null"
        os.system(reset_version)
        dst_file_origin = current_commit_path + "/" + "ori_" + filename.split('/')[-1]
        copy_cmd = 'cp ' + target_file + ' ' + dst_file_origin
        os.system(copy_cmd)
        diff_cmd = 'diff ' + dst_file_changed + " " + dst_file_origin + " >" + current_commit_path + "/diff.txt"
        os.system(diff_cmd)
        return True


if __name__ == "__main__":
    BASE_PATH = '/Users/fangdongliang/Desktop/difference/'
    with open('res.json', 'r') as infile:
        m_commit = json.load(infile)
        for (k, v) in m_commit.items():
            for commit_id in v:
                extra_file(k, commit_id)

    pass