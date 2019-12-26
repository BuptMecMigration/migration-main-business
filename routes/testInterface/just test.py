import threading
import time

import requests

mini_service = {
                    "migration":
                        {
                            "index1": "111",
                            "index2": "222",
                            "index3": "333"
                        }
               }

if __name__ == '__main__':

    def hold1(limit):
        i = 0
        while 1:
            i += 1
            print(t1.name,"is runing")
            time.sleep(1)
        print(t1.name, "is over")

    def hold2(limit):
        i = 0
        while 1:
            i += 1
            print(t2.name , "is runing")
            time.sleep(1)
        print(t2.name , "is over")

    start_time = time.time()
    workers = []
    t1 = threading.Thread(target=hold1, args=(3,))
    t2 = threading.Thread(target=hold2, args=(6,))

    workers.append(t1)
    workers.append(t2)

    for worker in workers:
        worker.start()

    # for worker in workers:
    #     worker.join()

    print(threading.current_thread().name, "耗时", time.time()-start_time)


# if __name__ == '__main__':
#     # print(mini_service["migration"]["index"])
#     # print(mini_service["migration"][2])
#     minServiceAddr = "http://47.103.27.246:5000/ui/test/function_4"
#     us_data = {"test_string": "string add begin:"}
#     res = requests.post(minServiceAddr, json=us_data)
#     print(res.status_code)
#     print(res.text)
#     print(res.raw.read())

