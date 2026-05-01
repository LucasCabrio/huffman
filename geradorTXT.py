with open("teste_grande.txt", "w", encoding="utf-8") as f:
    for i in range(20000):
        f.write(f"Linha {i}: Este é um texto de teste para compressão Huffman. "
                "Quanto mais repetição, melhor a compressão.\n")