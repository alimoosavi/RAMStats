import sqlite3
import time
import psutil
import threading
import settings


class DBInteractionException(Exception):
    def __init__(self, message="Something bad occurred about db connection"):
        self.message = message
        super().__init__(self.message)


class DataStore:
    # _instance = None
    #
    # def __new__(cls, *args, **kwargs):
    #     if not cls._instance:
    #         cls._instance = super().__new__(cls, *args, **kwargs)
    #     return cls._instance

    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS ram_stats (
                                id INTEGER PRIMARY KEY,
                                total_mb REAL,
                                free_mb REAL,
                                used_mb REAL,
                                timestamp INTEGER
                                )''')
        # self.cursor.execute('''CREATE INDEX time_stamp_index ON ram_stats(timestamp);''')
        self.conn.commit()

    def insert_data(self, total, free, used, time_stamp):
        # timestamp = int(time.time())
        try:
            self.cursor.execute('''INSERT INTO ram_stats (total_mb, free_mb, used_mb, timestamp) 
                                    VALUES (?, ?, ?, ?)''', (total, free, used, int(time_stamp)))
            self.conn.commit()
        except sqlite3.Error:
            self.conn.rollback()
            raise DBInteractionException()

    # def tables_exist(self):
    #     self.cursor.execute("SELECT name FROM sqlite_master WHERE type='ram_stats';")
    #     tables = self.cursor.fetchall()
    #     return len(tables) > 0

    def get_last_n_records(self, n):
        self.cursor.execute('''SELECT total_mb, free_mb, used_mb, timestamp FROM ram_stats
                                ORDER BY timestamp DESC LIMIT ?''', (n,))
        items = self.cursor.fetchall()
        if items is None:
            raise DBInteractionException()
        return [{"total": item[0], "free": item[1], "used": item[2]} for item in items]

    def teardown(self):
        self.conn.close()


class RAMStatsCollector:
    def __init__(self, interval_seconds: int):
        # self.store = store
        self.store = DataStore(settings.SETTINGS['db']['path'])
        self.interval_seconds = interval_seconds

    @staticmethod
    def collect_ram_data():
        ram = psutil.virtual_memory()
        total = ram.total
        free = ram.available
        used = ram.used
        return total, free, used

    def store_ram_data(self):
        while True:
            total, free, used = self.collect_ram_data()
            self.store.insert_data(total=total, free=free, used=used, time_stamp=time.time())
            time.sleep(self.interval_seconds)

    def store_ram_job(self):
        store_thread = threading.Thread(target=self.store_ram_data)
        store_thread.daemon = True
        store_thread.start()

#
# def store_ram_data_job():
#     store_thread = threading.Thread(target=store_ram_data)
#     store_thread.daemon = True
#     store_thread.start()
