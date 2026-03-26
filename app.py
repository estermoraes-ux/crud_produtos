from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# Arquivo onde os produtos serão salvos
ARQUIVO = "produtos.json"

# Função para carregar os produtos
def carregar_produtos():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r") as f:
            return json.load(f)
    return []

# Função para salvar os produtos
def salvar_produtos(produtos):
    with open(ARQUIVO, "w") as f:
        json.dump(produtos, f, indent=4)

# Rota GET - listar produtos
@app.route("/produtos", methods=["GET"])
def listar_produtos():
    produtos = carregar_produtos()
    return jsonify(produtos)

# Rota POST - adicionar produto
@app.route("/produtos", methods=["POST"])
def adicionar_produto():
    produtos = carregar_produtos()
    novo_produto = request.get_json()
    novo_produto["id"] = len(produtos) + 1
    produtos.append(novo_produto)
    salvar_produtos(produtos)
    return jsonify(novo_produto), 201

# Rota PUT - atualizar produto
@app.route("/produtos/<int:id>", methods=["PUT"])
def atualizar_produto(id):
    produtos = carregar_produtos()
    for produto in produtos:
        if produto["id"] == id:
            dados = request.get_json()
            produto.update(dados)
            salvar_produtos(produtos)
            return jsonify(produto)
    return jsonify({"erro": "Produto não encontrado"}), 404

# Rota DELETE - remover produto
@app.route("/produtos/<int:id>", methods=["DELETE"])
def deletar_produto(id):
    produtos = carregar_produtos()
    for produto in produtos:
        if produto["id"] == id:
            produtos.remove(produto)
            salvar_produtos(produtos)
            return jsonify({"mensagem": "Produto removido"})
    return jsonify({"erro": "Produto não encontrado"}), 404

if __name__ == "__main__":
    app.run(debug=True)