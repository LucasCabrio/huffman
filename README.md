# Compressão de Arquivos com Huffman

Este projeto implementa um compressor e descompressor de arquivos utilizando o algoritmo de **Huffman**, uma técnica clássica de compressão baseada na frequência de caracteres.

Além do algoritmo, o projeto conta com uma interface gráfica simples desenvolvida em **Tkinter**, permitindo a seleção e processamento de arquivos de forma intuitiva.

---

# Conceito

O algoritmo de Huffman é um método de compressão **sem perda (lossless)** que funciona da seguinte forma:

1. Conta a frequência de cada caractere no arquivo
2. Constrói uma árvore binária baseada nessas frequências
3. Gera códigos binários menores para caracteres mais frequentes
4. Substitui os caracteres pelos seus respectivos códigos

Resultado: redução do tamanho do arquivo sem perda de informação

---

# Funcionamento do Projeto

O sistema realiza:

* Leitura de arquivos `.txt`
* Cálculo da frequência dos caracteres
* Construção da árvore de Huffman
* Geração dos códigos binários
* Compressão em formato binário (`.huff`)
* Descompressão para reconstrução do arquivo original

---

# Interface

A interface foi construída com **Tkinter** e possui:

* Botão para selecionar arquivo
* Botão para compactar
* Botão para descompactar
* Exibição do caminho do arquivo
* Exibição do tamanho original e compactado
* Cálculo da taxa de compressão (%)

---

# Exemplo de Resultado

| Tipo de arquivo | Tamanho original | Compactado | Resultado          |
| --------------- | ---------------- | ---------- | ------------------ |
| Texto grande    | 22 MB            | 12 MB      | ~46% redução       |
| Texto pequeno   | 16 bytes         | 164 bytes  | aumento (overhead) |

---

# Observações Importantes

* Arquivos pequenos podem **aumentar de tamanho** devido ao overhead do algoritmo
* A eficiência depende da **repetição de padrões** no conteúdo
* A implementação atual é **didática**, focada no entendimento do algoritmo

---

# Como Executar

## 1. Pré-requisitos

* Python 3 instalado

Verifique com:

```bash
python --version
```

---

## 2. Clonar o repositório

```bash
git clone https://github.com/seuusuario/huffman.git
cd huffman
```

---

## 3. Executar a aplicação

```bash
python interface.py
```

---

## 4. Uso

1. Clique em **Selecionar arquivo**
2. Escolha um `.txt`
3. Clique em:

   * **Compactar** → gera `.huff`
   * **Descompactar** → gera `.txt`

---

# Complexidade

* Contagem de frequência: **O(n)**
* Construção da árvore: **O(n log n)**
* Compressão/Descompressão: **O(n)**

---

# Limitações

* O arquivo compactado depende da árvore gerada na execução
* Não há persistência da árvore no arquivo `.huff`
* Não utiliza processamento em streaming (carrega tudo na memória)

---

# Possíveis Melhorias

* Armazenar a árvore no arquivo compactado
* Implementar leitura em streaming (para arquivos grandes)
* Melhorar performance com manipulação direta de bits
* Criar interface web (Flask)

---

