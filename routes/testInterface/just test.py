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
    # print(mini_service["migration"]["index"])
    # print(mini_service["migration"][2])
    minServiceAddr = "http://47.103.27.246:5000/ui/test/function_4"
    us_data = {"test_string": "string add begin:"}
    res = requests.post(minServiceAddr, json=us_data, )
    print(res.status_code)
    print(res.text)
