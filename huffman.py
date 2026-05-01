import json
import os
import struct


class Node:
    def __init__(self, caractere, frequencia):
        self.caractere = caractere
        self.frequencia = frequencia
        self.esquerda = None
        self.direita = None


def contar_frequencia(texto):
    frequencia = {}
    for caractere in texto:
        frequencia[caractere] = frequencia.get(caractere, 0) + 1
    return frequencia


def construir_arvore(frequencia):
    nos = [Node(caractere, freq) for caractere, freq in frequencia.items()]
    if not nos:
        return None

    while len(nos) > 1:
        # Ordena pelos menores pesos para juntar primeiro os nós menos frequentes.
        nos = sorted(nos, key=lambda x: x.frequencia)
        esquerda = nos.pop(0)
        direita = nos.pop(0)
        # Nó interno soma as frequências dos dois filhos para subir na árvore.
        novo = Node(None, esquerda.frequencia + direita.frequencia)
        novo.esquerda = esquerda
        novo.direita = direita
        nos.append(novo)

    return nos[0]


def gerar_codigos(no, codigo_atual, codigos):
    if no is None:
        return

    if no.caractere is not None:
        codigos[no.caractere] = codigo_atual
        return

    # Caminhar à esquerda adiciona 0 e à direita adiciona 1 no código de Huffman.
    gerar_codigos(no.esquerda, codigo_atual + "0", codigos)
    gerar_codigos(no.direita, codigo_atual + "1", codigos)


def compactar_arquivo(caminho_entrada, caminho_saida):
    with open(caminho_entrada, "r", encoding="utf-8") as arquivo:
        texto = arquivo.read()

    frequencia = contar_frequencia(texto)
    raiz = construir_arvore(frequencia)
    codigos = {}
    gerar_codigos(raiz, "", codigos)

    # Substitui cada caractere pela sequência de bits gerada na árvore.
    texto_compactado = "".join(codigos[caractere] for caractere in texto)
    padding = 8 - (len(texto_compactado) % 8)
    if padding != 8:
        texto_compactado += "0" * padding
    else:
        padding = 0

    # Os 8 primeiros bits guardam quanto padding foi adicionado no final.
    texto_compactado = f"{padding:08b}" + texto_compactado
    bytes_array = bytearray()
    for i in range(0, len(texto_compactado), 8):
        byte = texto_compactado[i:i+8]
        # Converte cada bloco de 8 bits em um byte real para gravar no arquivo.
        bytes_array.append(int(byte, 2))

    # O cabeçalho salva o mapa de códigos para permitir a descompactação depois.
    header = json.dumps(codigos, ensure_ascii=False).encode("utf-8")
    # ">I" empacota o tamanho do cabeçalho como inteiro sem sinal de 4 bytes.
    header_length = struct.pack(">I", len(header))

    with open(caminho_saida, "wb") as arquivo:
        arquivo.write(header_length)
        arquivo.write(header)
        arquivo.write(bytes(bytes_array))

    return os.path.getsize(caminho_entrada), os.path.getsize(caminho_saida)


def descompactar_arquivo(caminho_entrada, caminho_saida):
    if not caminho_entrada.lower().endswith(".huff"):
        raise ValueError("Selecione um arquivo com extensão .huff para descompactar.")

    with open(caminho_entrada, "rb") as arquivo:
        header_length_bytes = arquivo.read(4)
        if len(header_length_bytes) != 4:
            raise ValueError("Arquivo .huff inválido ou corrompido.")

        header_length = struct.unpack(">I", header_length_bytes)[0]
        header_bytes = arquivo.read(header_length)
        codigos = json.loads(header_bytes.decode("utf-8"))
        dados = arquivo.read()

    # Reconstrói a sequência binária lendo cada byte como 8 bits.
    bits = "".join(f"{byte:08b}" for byte in dados)
    padding = int(bits[:8], 2)
    bits = bits[8:]
    if padding > 0:
        bits = bits[:-padding]

    # Inverte o dicionário para buscar caractere a partir do código binário.
    mapa_invertido = {valor: chave for chave, valor in codigos.items()}
    texto_descompactado = ""
    prefixo = ""

    for bit in bits:
        prefixo += bit
        # Quando o prefixo vira um código válido, recuperamos um caractere completo.
        if prefixo in mapa_invertido:
            texto_descompactado += mapa_invertido[prefixo]
            prefixo = ""

    with open(caminho_saida, "w", encoding="utf-8") as arquivo:
        arquivo.write(texto_descompactado)

    return caminho_entrada, caminho_saida
