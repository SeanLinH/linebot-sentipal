import sqlite3
import uuid



class Mood:
    def __init__(self, **kwargs):
        self.user_id = kwargs.get("user_id") if kwargs.get("user_id") != None else f'{uuid.uuid4()}'
        self.group_id = kwargs.get("group_id") 
        self.user_text = kwargs.get("user_text") 
        self.user_mood = kwargs.get("user_mood") 
        self.mood_score = kwargs.get("mood_score") 
        self.stable_score = kwargs.get("stable_score") 
        self.engage = kwargs.get("engage") 
        if any(value is None for value in [self.user_id, self.user_text, self.user_mood, self.mood_score, self.stable_score, self.engage]): 
            raise ValueError("請輸入完整的屬性")
            
    def update(self, **kwargs):
        self.group_id = kwargs.get("group_id") 
        self.user_text = kwargs.get("user_text") 
        self.user_mood = kwargs.get("user_mood") 
        self.mood_score = kwargs.get("mood_score") 
        self.stable_score = kwargs.get("stable_score") 
        self.engage = kwargs.get("engage")
        if "user_id" in kwargs.keys():
            raise ValueError("UPDATE 不用設定user_id")
        
        update_comm = list(kwargs.keys())
        update_comm = " = ?, ".join(str(x) for x in update_comm)
        lst = list(kwargs.values())
        lst.append(self.user_id)
        conn = sqlite3.connect('src/db/database.db')
        c = conn.cursor()
        
        
        try:
            print(f"UPDATE mood SET {update_comm} = ? WHERE user_id = ?")
            c.execute(f"UPDATE mood SET {update_comm} = ? WHERE user_id = ?", tuple(lst))
            conn.commit()
            print("Command executed successfully")
        except Exception as e:
            print("Update Failed")
            print(e)
        conn.close()

    def insert(self):
        conn = sqlite3.connect('src/db/database.db')
        c = conn.cursor()
        try:
            c.execute(f"INSERT INTO mood (user_id, group_id, user_text, user_mood, mood_score, stable_score, engage) VALUES (?, ?, ?, ?, ?, ?, ?)",
                          (self.user_id, self.group_id, self.user_text, self.user_mood, self.mood_score, self.stable_score, self.engage))
            conn.commit()
            print("Command executed successfully")
        except Exception as e:
            print("Insert Failed")
            print(e)
        conn.close()
    def fetch_group_memory(self):
        conn = sqlite3.connect('src/db/database.db')
        c = conn.cursor()
        c.execute(f"SELECT user_text FROM users WHERE name = ?", ())
        

class AIresponse:
    def __init__(self, **kwargs):
        self.user_id = kwargs.get("user_id")
        self.group_id = kwargs.get("group_id") 
        self.ai_text = kwargs.get("ai_text") 
        if self.user_id == None:
            raise ValueError("請輸入完整的屬性")

    def insert(self):
        conn = sqlite3.connect('src/db/database.db')
        c = conn.cursor()
        try:
            c.execute(f"INSERT INTO response (user_id, group_id, ai_text) VALUES (?, ?, ?)",
                          (self.user_id, self.group_id, self.ai_text))
            conn.commit()
            print("Command executed successfully")
        except Exception as e:
            print("Insert Failed")
            print(e)
        conn.close()


class UserAPI:
    def __init__(self, **kwargs):
        self.user_id = kwargs.get("user_id")
        self.group_id = kwargs.get("group_id") 
        self.user_api = kwargs.get("user_api") 
        if any(value is None for value in [self.user_id, self.user_api]): 
            raise ValueError("請輸入完整的屬性")

    def insert(self):
        conn = sqlite3.connect('src/db/database.db')
        c = conn.cursor()
        try:
            c.execute(f"INSERT INTO user_api (user_id, group_id, user_api) VALUES (?, ?, ?)",
                          (self.user_id, self.group_id, self.user_api))
            conn.commit()
            print("Command executed successfully")
        except Exception as e:
            print("Insert Failed")
            print(e)
        conn.close()


class GroupAPI:
    def __init__(self, **kwargs):
        self.group_id = kwargs.get("group_id") 
        self.group_api = kwargs.get("group_api") 
        if any(value is None for value in [self.group_id, self.group_api]): 
            raise ValueError("請輸入完整的屬性")

    def insert(self):
        conn = sqlite3.connect('src/db/database.db')
        c = conn.cursor()
        try:
            c.execute(f"INSERT INTO group_api (group_id, group_api) VALUES (?, ?)",
                          (self.group_id, self.group_api))
            conn.commit()
            print("Command executed successfully")
        except Exception as e:
            print("Insert Failed")
            print(e)
        conn.close()

class Users:
    def __init__(self, **kwargs):
        self.user_id = kwargs.get("user_id")
        self.user_role = kwargs.get("user_role") if kwargs.get("user_role") !=None else "general"
        self.summary = kwargs.get("summary") 
        self.last_mood = kwargs.get("last_mood")
        self.last_response = kwargs.get("last_response")
       
        if any(value is None for value in [self.user_id, self.user_role, self.summary, self.last_mood, self.last_response]): 
            raise ValueError("請輸入完整的屬性")

    def insert(self):
        conn = sqlite3.connect('src/db/database.db')
        c = conn.cursor()
        try:
            c.execute(f"INSERT INTO user (user_id, user_role, summary, last_mood, last_response) VALUES (?, ?, ?, ?, ?)",
                          (self.user_id, self.group_id, self.user_api))
            conn.commit()
            print("Command executed successfully")
        except Exception as e:
            print("Insert Failed")
            print(e)
        conn.close()
        
    def update(self, **kwargs):
        self.user_role = kwargs.get("user_role") 
        self.summary = kwargs.get("summary") if kwargs.get("summary") !=None else "general"
        self.last_mood = kwargs.get("last_mood")
        self.last_response = kwargs.get("last_response")
        
        if "user_id" in kwargs.keys():
            raise ValueError("UPDATE 不用設定user_id")
        
        update_comm = list(kwargs.keys())
        update_comm = " = ?, ".join(str(x) for x in update_comm)
        lst = list(kwargs.values())
        lst.append(self.user_id)
        conn = sqlite3.connect('src/db/database.db')
        c = conn.cursor()
        
        try:
            print(f"UPDATE user SET {update_comm} = ? WHERE user_id = ?")
            c.execute(f"UPDATE user SET {update_comm} = ? WHERE user_id = ?", tuple(lst))
            conn.commit()
            print("Command executed successfully")
        except Exception as e:
            print("Update Failed")
            print(e)
        conn.close()

    def fetch(self):
        conn = sqlite3.connect('src/db/database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE name = ?;", (self.user_id,))
        user = c.fetchone()
        conn.commit()
        conn.close()
        return user

    



'''

### 新增用戶資料
def insert_user(user_id, name, domain, role, goal, tag):
    conn = sqlite3.connect('src/db/database.db')
    c = conn.cursor()
    print(f"INSERT INTO users VALUES ({user_id}, {name}, {domain}, {role}, {goal}, {tag})")
    try:
        c.execute(f"INSERT INTO users (user_id, name, domain, role, goal, tag) VALUES (?, ?, ?, ?, ?, ?);",(user_id, name, domain, role, goal, tag))
        conn.commit()
        print("Command executed successfully")

    except Exception as e:
        print("Update Failed")
        print(e)
    conn.close()

### 新增問題到叢集裡
def insert_qst(question, user_id, state='待解決'):
    qst_id = f'{uuid.uuid4()}'
    conn = sqlite3.connect('src/db/database.db')
    c = conn.cursor()

    try:
        c.execute(f"INSERT INTO question_cluster (qst_id, qst_text, ask_user, expert_user, ai_response, expert_response, state) VALUES (?, ?, ?, ?, ?, ?, ?);", (qst_id, question, user_id, None, None, None, '待解決'))
        conn.commit()
        print("Command executed successfully")
    except Exception as e:
        print("Update Failed")
        print(e)
    conn.close()

### AI 回答問題
def ai_response(user_id, question, ans):
    qst_id = f'{uuid.uuid4()}'
    conn = sqlite3.connect('src/db/database.db')
    c = conn.cursor()

    try:
        c.execute(f"INSERT INTO question_cluster (qst_id, qst_text, ask_user, expert_user, ai_response, expert_response, state) VALUES (?, ?, ?, ?, ?, ?, ?);", (qst_id, question, None, user_id, ans, None, '已解決'))
        conn.commit()
        print("Command executed successfully")
    except Exception as e:
        print("Update Failed")
        print(e)
    conn.close()
    
    
### 更新用戶資料
def update(user_id, name, domain, role, goal, tag):
    conn = sqlite3.connect('src/db/database.db')
    c = conn.cursor()
    
    try:
        c.execute(f"UPDATE users SET name = ?, domain = ?, role = ?, goal = ?, tag = ? WHERE user_id = ?",(name, domain, role, goal, tag, user_id))
        conn.commit()
        print("Command executed successfully")

    except Exception as e:
        print("Update Failed")
        print(e)
    conn.close()    
    
    
### 查詢用戶名是否存在
def check_username(name):
    conn = sqlite3.connect('src/db/database.db')
    c = conn.cursor()
    c.execute("SELECT user_id, goal FROM users WHERE name = ? ORDER BY timestamp DESC;", (name,))
    user = c.fetchone()
    conn.commit()
    conn.close()
    if user:
        return user[0], user[1]
    else:
        return None, None


### 抓取用戶問題
def fetch_user_qst():
    pass



def fetch_group_qst():
    pass
    
'''
    

