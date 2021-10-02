from tinydb import TinyDB, Query
import uuid
from datetime import datetime

class ChallengeHandler:
    """
    handle all the challenges
    """
    def __init__(self, IP, username, cookie):
        self.ip = IP
        self.db = TinyDB('db.json')
        self.info_table = self.db.table('info')
        self.submit_table = self.db.table('submit')
        self.flag_table = self.db.table('flag')
        self.query = Query()
        self.info = self.get_info_by_IP(username=username, cookie=cookie)
        if not self.info:
            # first time visiter
            user_dict = self.create_new_user(IP, username)
            self.info = user_dict

    def add_to_submit(self, flag, cha_no):
        """
        once verified, add the info to submit
        return:
            status: -1: already submitted, 1: success
        """
        user_dict = {}
        user_dict['IP'] = self.ip
        user_dict['username'] = self.info.get('username')
        user_dict['cookie'] = self.info.get('cookie')
        user_dict['cha_no'] = cha_no
        selected = self.submit_table.search(self.query.fragment(user_dict))
        if len(selected):
            return -1

        user_dict['flag'] = flag
        user_dict['time'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.submit_table.insert(user_dict)
        return 1

    def insert_right_answer(self, question, answer, cha_no):
        """
        insert the right answer to db based on the cookie
        """
        self.flag_table.insert({"question": question, "answer": answer, "cookie": self.info.get('cookie'), 'cha_no': cha_no})

    def create_new_user(self, IP, username):
        """
        create a new user based on IP and username
        """
        user_dict = {}
        user_dict['cookie'] = uuid.uuid4().hex
        user_dict['IP'] = IP
        user_dict['username'] = username
        self.info_table.insert(user_dict)
        return user_dict

    def get_info_by_IP(self, username=None, cookie=None):
        """
        return the info of the ip
        """
        search_dict = {'IP': self.ip}
        if username:
            search_dict['username'] = username
        if cookie:
            search_dict['cookie'] = cookie

        selected = self.info_table.search(self.query.fragment(search_dict))
        return selected[0] if len(selected) else None

    def get_flag_by_cookie(self, cookie, cha_no):
        """
        get the right flag by cookie
        """
        selected = self.flag_table.search(self.query.fragment({'cookie': cookie, 'cha_no': cha_no}))
        return selected

    def get_a_new_key_pair(self):
        """
        generate a new key pairs
        """
        from cryptography.hazmat.primitives import serialization as crypto_serialization
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography.hazmat.backends import default_backend as crypto_default_backend

        key = rsa.generate_private_key(
            backend=crypto_default_backend(),
            public_exponent=65537,
            key_size=2048
        )
        private_key = key.private_bytes(
            crypto_serialization.Encoding.PEM,
            crypto_serialization.PrivateFormat.PKCS8,
            crypto_serialization.NoEncryption())
        public_key = key.public_key().public_bytes(
            crypto_serialization.Encoding.OpenSSH,
            crypto_serialization.PublicFormat.OpenSSH
        )
        return private_key, public_key
    
    def get_md5(self, string):
        """
        get the md5 of a string
        """
        import hashlib
        return hashlib.md5(string.encode()).hexdigest()

    def verify_flag(self, flag, cha_no):
        """
        verify a flag based on the cha_no and cookie
        """
        selected = self.flag_table.search(self.query.fragment({'cookie': self.info.get('cookie'), 'cha_no': cha_no}))
        if len(selected):
            print("Right:", selected[0]['answer'], "User: ", flag)
            return flag.lower() == selected[0]['answer']
        return False

    def handle_q1(self):
        """
        handle question 1
        """
        flag = self.get_flag_by_cookie(self.info.get('cookie'), '1')
        if len(flag):
            return flag[0].get('question')

        # request a new key pair
        pri, pub = self.get_a_new_key_pair()
        pri = pri.decode()
        pub_md5 = self.get_md5(pub.decode().split(' ')[1])
        self.insert_right_answer(pri, pub_md5, '1')
        return pri
