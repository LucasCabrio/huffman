import os
import tkinter as tk
from tkinter import filedialog, messagebox

from huffman import compactar_arquivo, descompactar_arquivo


def criar_interface():
    root = tk.Tk()
    root.title("Compressor Huffman")
    root.resizable(False, False)

    selecionado_var = tk.StringVar(value="Nenhum arquivo selecionado")
    tamanho_var = tk.StringVar(value="Tamanho original: - | Compactado: -")
    taxa_var = tk.StringVar(value="Taxa de compressão: -")

    def selecionar_arquivo():
        caminho = filedialog.askopenfilename(title="Selecionar arquivo")
        if caminho:
            selecionado_var.set(caminho)
            tamanho_var.set("Tamanho original: - | Compactado: -")
            taxa_var.set("Taxa de compressão: -")

    def compactar():
        caminho = selecionado_var.get()
        if not caminho or caminho == "Nenhum arquivo selecionado":
            messagebox.showwarning("Aviso", "Selecione um arquivo antes de compactar.")
            return

        destino = caminho + ".huff"
        try:
            tamanho_original, tamanho_compactado = compactar_arquivo(caminho, destino)
            tamanho_var.set(
                f"Tamanho original: {tamanho_original} bytes | Compactado: {tamanho_compactado} bytes"
            )
            if tamanho_original > 0:
                taxa = (1 - (tamanho_compactado / tamanho_original)) * 100
                taxa_var.set(f"Taxa de compressão: {taxa:.2f}%")
            else:
                taxa_var.set("Taxa de compressão: 0.00%")
            messagebox.showinfo("Compactar", f"Arquivo compactado salvo em:\n{destino}")
        except Exception as erro:
            messagebox.showerror("Erro", str(erro))

    def descompactar():
        caminho = selecionado_var.get()
        if not caminho or caminho == "Nenhum arquivo selecionado":
            messagebox.showwarning("Aviso", "Selecione um arquivo .huff antes de descompactar.")
            return

        if not caminho.lower().endswith(".huff"):
            messagebox.showwarning("Aviso", "Selecione um arquivo com extensão .huff para descompactar.")
            return

        destino = caminho[:-5] + "_descompactado.txt"
        try:
            _, destino = descompactar_arquivo(caminho, destino)
            messagebox.showinfo("Descompactar", f"Arquivo descompactado salvo em:\n{destino}")
        except Exception as erro:
            messagebox.showerror("Erro", str(erro))

    label_arquivo = tk.Label(root, textvariable=selecionado_var, anchor="w", width=60)
    label_arquivo.grid(row=0, column=0, columnspan=3, padx=10, pady=(10, 5), sticky="w")

    btn_selecionar = tk.Button(root, text="Selecionar arquivo", command=selecionar_arquivo, width=18)
    btn_compactar = tk.Button(root, text="Compactar", command=compactar, width=18)
    btn_descompactar = tk.Button(root, text="Descompactar", command=descompactar, width=18)

    btn_selecionar.grid(row=1, column=0, padx=10, pady=5)
    btn_compactar.grid(row=1, column=1, padx=10, pady=5)
    btn_descompactar.grid(row=1, column=2, padx=10, pady=5)

    label_tamanhos = tk.Label(root, textvariable=tamanho_var, anchor="w", width=60)
    label_tamanhos.grid(row=2, column=0, columnspan=3, padx=10, pady=(5, 10), sticky="w")

    label_taxa = tk.Label(root, textvariable=taxa_var, anchor="w", width=60)
    label_taxa.grid(row=3, column=0, columnspan=3, padx=10, pady=(0, 10), sticky="w")

    root.mainloop()


if __name__ == "__main__":
    criar_interface()
