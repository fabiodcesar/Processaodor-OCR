import torch
import easyocr
import argparse
import sys
import os
from datetime import datetime

def get_current_timestamp():
    return datetime.now().strftime('%Y/%m/%d %H:%M:%S.%f')[:-3]

print(f"Processador OCR")

if torch.cuda.is_available():
    device = torch.device("cuda")
    print(f"[{get_current_timestamp()}] Usando CUDA: {torch.cuda.get_device_name(0)}")
else:
    device = torch.device("cpu")
    print(f"[{get_current_timestamp()}] CUDA não está disponível; usando CPU.")

# Suprimir toda a saída do easyocr (incluindo avisos)
class SuppressOutput:
    def __init__(self):
        self.null = open(os.devnull, 'w')

    def __enter__(self):
        # Redireciona stdout e stderr para null para suprimir a saída
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
        sys.stdout = self.null
        sys.stderr = self.null

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Restaura o stdout e stderr originais
        sys.stdout = self.original_stdout
        sys.stderr = self.original_stderr

# Configurar o parsing dos argumentos
parser = argparse.ArgumentParser(description="OCR para imagens em uma pasta")
parser.add_argument("--input", type=str, default="data/input", help="Diretório contendo as imagens a serem processadas")
parser.add_argument("--output", type=str, default="data/output", help="Diretório para salvar os resultados do OCR")

# Analisar os argumentos
args = parser.parse_args()

# Inicializar o leitor OCR
reader = easyocr.Reader(['pt'])

# Criar o diretório de saída, caso não exista
os.makedirs(args.output, exist_ok=True)

total_processed = 0
failed_files = []  # Lista para armazenar os nomes dos arquivos que falharam no processamento
start_date = datetime.now()

print(f"[{get_current_timestamp()}] Iniciando o processamento das imagens")

# Processar cada imagem no diretório de entrada
for filename in os.listdir(args.input):
    # Processar apenas arquivos de imagem (você pode adicionar mais extensões, se necessário)
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
        image_path = os.path.join(args.input, filename)

        try:
            # Suprimir saída durante a execução do OCR
            with SuppressOutput():
                result = reader.readtext(image_path)

            # Gerar o nome do arquivo de saída
            output_filename = f"{filename}.txt"
            output_path = os.path.join(args.output, output_filename)

            # Salvar o resultado do OCR no arquivo de saída
            with open(output_path, 'w', encoding='utf-8') as output_file:
                for detected in result:
                    output_file.write(detected[1] + '\n')

            print(f"[{get_current_timestamp()}] OCR para {filename} processado")
            total_processed += 1

        except Exception as e:
            failed_files.append(filename)
            print(f"[{get_current_timestamp()}] Erro ao processar {filename}: {e}")

print(f"[{get_current_timestamp()}] Processamento concluído")

# Registrar os nomes dos arquivos que falharam
if failed_files:
    print(f"\n[{get_current_timestamp()}] Os seguintes arquivos não puderam ser processados:")
    for failed_file in failed_files:
        print(f" - {failed_file}")

time_difference = datetime.now() - start_date
seconds_elapsed = time_difference.total_seconds()
minutes_elapsed = seconds_elapsed / 60
print(f"--------------------------------------------------------------")
print(f"Tempo total decorrido: {seconds_elapsed} segundos")
print(f"Tempo total decorrido: {minutes_elapsed:.2f} minutos")
print(f"Imagens processadas: {total_processed}")
print(f"Imagens com falha: {len(failed_files)}")
if total_processed > 0:
    print(f"Taxa média de processamento: {seconds_elapsed/total_processed:.2f} segundos/imagem")
