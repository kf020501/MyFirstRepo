import logging
import time

# プログラム開始時刻
start_time = time.time()

# 経過時間を計算して hh:mm:ss.ddd で表示するためのカスタムフォーマッタ
class ElapsedTimeFormatter(logging.Formatter):
    def format(self, record):
        # 経過時間を計算
        elapsed_time = time.time() - start_time
        
        # 時間、分、秒、小数点以下のミリ秒を計算
        hours, rem = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(rem, 60)
        
        # hh:mm:ss.ddd 形式にフォーマット
        record.elapsed_time = f"{int(hours):02}:{int(minutes):02}:{seconds:06.3f}"
        return super().format(record)

# ロガーの設定
logger = logging.getLogger('custom_logger')
logger.setLevel(logging.DEBUG)

# カスタムフォーマットの設定
formatter = ElapsedTimeFormatter('%(asctime)s,%(elapsed_time)s,%(levelname)s,%(message)s')

# ストリームハンドラ（コンソール用）を設定
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)  # コンソールにはDEBUGレベル以上を表示
console_handler.setFormatter(formatter)

# ファイルハンドラ（ファイル用）を設定
file_handler = logging.FileHandler('logfile.log', mode='w')
file_handler.setLevel(logging.INFO)  # ファイルにはINFOレベル以上を出力
file_handler.setFormatter(formatter)

# ハンドラをロガーに追加
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# 実行時間のリスト
execution_times = []

# 何かの処理
def some_processing():
    logger.debug("some_processing 関数の開始")
    start = time.time()  # 処理開始時刻
    
    # ダミー処理
    time.sleep(1)  
    
    # 処理時間の計測
    end = time.time()
    elapsed = end - start
    logger.info(f"some_processing の実行時間: {elapsed:.3f} 秒")
    
    # 実行時間をリストに追加
    execution_times.append(elapsed)

# メイン処理
logger.info("プログラムが開始されました")

# ループ
for i in range(5):  # 5回ループします（適宜変更してください）
    logger.debug(f"現在のループカウンタ: {i}")
    # 開始時間からi * 5秒の時間までsleep
    target_time = start_time + i * 5
    sleep_duration = target_time - time.time()
    
    logger.debug(f"スリープ時間の計算結果: {sleep_duration:.3f} 秒")
    
    # 何秒スリープするか表示 (hh:mm:ss.ddd)
    if sleep_duration > 0:
        logger.info(f"{i} 回目のスリープ時間: {sleep_duration:.3f} 秒")
        time.sleep(sleep_duration)
    else:
        logger.debug("スリープ時間が0以下のためスキップします")
    
    # 何かの処理
    some_processing()

# プログラム終了時に平均と最大値を計算
if execution_times:
    average_time = sum(execution_times) / len(execution_times)
    max_time = max(execution_times)
    logger.info(f"some_processing の平均実行時間: {average_time:.3f} 秒")
    logger.info(f"some_processing の最大実行時間: {max_time:.3f} 秒")
