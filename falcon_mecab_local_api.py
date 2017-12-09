# -*- coding: utf-8 -*-
import json
import falcon
import MeCab

# local-apiアクセス
# ex) localhost:8000/mecab?sentence=文章&hinshi=名詞_形容詞_助動詞

# mecab部分
class ReturnJson(object):
    # getメソッド
    def on_get(self, req, resp):
        params = req.params
        # パラメータの複数品詞指定は_で繋げる
        hinshi_list = params["hinshi"].split("_")
        res = self.get_token_list(params["sentence"],hinshi_list)
        msg = {"wordList":str(res)}
        resp.body = json.dumps(msg,ensure_ascii=False)

    def get_token_list(self, text, hinshi):
        token_list = []
        mt = MeCab.Tagger("-Ochasen")
        mt.parse('')
        node = mt.parseToNode(text)
        while node:
            feats = node.feature.split(',')
            if feats[0] in hinshi :
                try:
                    token_list.append(node.surface)
                except:
                    print("err: " + str(node.surface))
            node = node.next
        print(token_list)
        return token_list

# インスタンス作成
api_app = falcon.API()
api_app.add_route("/mecab",ReturnJson())

if __name__ == "__main__":
    # apiserverの起動
    from wsgiref import simple_server
    httpd = simple_server.make_server("", 8000, api_app)
    httpd.serve_forever()
