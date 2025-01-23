
# OCR Image Processor

Este projeto utiliza OCR (Reconhecimento Óptico de Caracteres) para extrair texto de imagens e salvar os resultados em arquivos de texto.

## Como Executar

### Requisitos

Instale as dependências com o comando:

```bash
pip install -r requirements.txt
```

### Executando o Script

Com os diretórios padrão:

```bash
python main.py
```

Com diretórios personalizados:

```bash
python main.py --input <diretório_de_entrada> --output <diretório_de_saída>
```

## Como Funciona

- O script verifica se o CUDA está disponível (senão usa a CPU).
- Processa imagens (.png, .jpg, .jpeg, .bmp, .tiff).
- Salva o texto extraído em arquivos `.txt`.

## Exemplo de Saída

```
OCR Image Extractor
[2025/01/22 14:32:15.123] Usando CUDA: GeForce GTX 1080
[2025/01/22 14:32:20.456] OCR para imagem1.jpg processado
...
--------------------------------------------------------------
Tempo total decorrido: 120.32 segundos
Imagens processadas: 50
Imagens com falha: 2
Taxa média de processamento: 2.41 segundos/imagem
```

## Dependências

- `torch`
- `easyocr`
