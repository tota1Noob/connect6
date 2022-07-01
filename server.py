import json
from time import time

from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route("/game_playback/<game_id>")
def playback(game_id):
    path = game_id + ".json"
    game_record = {}
    with open(path, "r") as f:
        game_record = json.load(f)

        timestamp = game_record["gameTimeStamp"]
        game_record["gameTimeStamp"] = "{}/{}/{} {}:{}:{}".format(
            timestamp[0:4], timestamp[4:6], timestamp[6:8], timestamp[8:10], timestamp[10:12], timestamp[12:14]
        )

        if game_record["winner"] == "black":
            game_record["winner"] = "黑方 {}".format(game_record["blackID"])
        else:
            game_record["winner"] = "白方 {}".format(game_record["whiteID"])

        max_cost, min_cost = 0, 10 ** 9
        for step in game_record["steps"]:
            min_cost = min(min_cost, step["cost"])
            max_cost = max(max_cost, step["cost"])
        
        time_mapping = max_cost - min_cost
        for step in game_record["steps"]:
            step["cost"] = (1000 + (step["cost"] - min_cost) // time_mapping) * 2
            if step["round"] == 1:
                step["cost"] //= 2

        black_player_pic = url_for('static', filename = 'Euler.jpg')
        white_player_pic = url_for('static', filename = 'Gauss.jpg')

    return render_template("game_playback.html", game_record=game_record, black_player_pic=black_player_pic, white_player_pic=white_player_pic)



if __name__ == "__main__":
    app.run("", port=5001)

#玩家信息
#头像
#ID：fjdskfjlsdf(执黑)
#昵称：是JFK但是
#天梯积分：2400
#段位：黄金/白银
#战绩：44胜23负