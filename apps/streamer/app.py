from streamer import *

if __name__ == '__main__':
    s = Streamer(app_name = __name__, record = True)
    s.info()
    t_flask = threading.Thread(target=s.start_flask, args=())
    t_flask.start()
    s.start_cam()
