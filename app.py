from flask import Flask, render_template, request, jsonify
import tictactoe as ttt

app = Flask(__name__, template_folder="templates", static_folder="static")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/ai", methods=["POST"])
def ai_move():
    """
    接收 JSON: {"board": [[...], [...], [...]]}
    返回 JSON: {"move": [i, j]} 或 {"move": null}
    """
    data = request.get_json(force=True)
    board = data.get("board")
    if board is None:
        return jsonify({"error": "missing board"}), 400

    # 将嵌套列表包装成 ttt.board（若已经是 board 实例则直接用）
    b = ttt.board(board) if not hasattr(board, "_board") else board

    if ttt.terminal(b):
        return jsonify({"move": None})

    move = ttt.minimax(b)
    return jsonify({"move": None if move is None else list(move)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)