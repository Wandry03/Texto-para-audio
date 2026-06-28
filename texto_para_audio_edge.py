import asyncio
import edge_tts
import os
import re

def carregar_texto(nome_arquivo):
    with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
        return arquivo.read()

def limpar_nome_arquivo(nome):
    # Remove caracteres que o Windows não aceita em nome de arquivo
    nome = re.sub(r'[\\/:*?"<>|]', "", nome)
    nome = nome.strip()

    if not nome:
        nome = "narracao"

    return nome

def dividir_texto(texto, tamanho_maximo=3000):
    partes = []
    texto = texto.strip()

    while len(texto) > tamanho_maximo:
        corte = texto.rfind(".", 0, tamanho_maximo)

        if corte == -1:
            corte = texto.rfind("!", 0, tamanho_maximo)

        if corte == -1:
            corte = texto.rfind("?", 0, tamanho_maximo)

        if corte == -1:
            corte = texto.rfind(",", 0, tamanho_maximo)

        if corte == -1:
            corte = texto.rfind(" ", 0, tamanho_maximo)

        if corte == -1:
            corte = tamanho_maximo

        parte = texto[:corte + 1].strip()
        partes.append(parte)

        texto = texto[corte + 1:].strip()

    if texto:
        partes.append(texto)

    return partes

async def gerar_mp3_unico(
    texto,
    caminho_saida,
    voz="pt-BR-AntonioNeural",
    rate="+10%",
    volume="+0%",
    ao_processar_parte=None
):

    partes = dividir_texto(texto)

    print(f"Texto dividido internamente em {len(partes)} parte(s).")
    print("Gerando MP3 único...")

    with open(caminho_saida, "wb") as arquivo_audio:
        for i, parte in enumerate(partes, start=1):
            print(f"Processando parte {i}/{len(partes)}...")
            if ao_processar_parte:
                ao_processar_parte(i, len(partes))

            comunicador = edge_tts.Communicate(
                text=parte,
                voice=voz,
                rate=rate,
                volume=volume
            )

            async for trecho in comunicador.stream():
                if trecho["type"] == "audio":
                    arquivo_audio.write(trecho["data"])

async def main():
    arquivo_texto = "texto.txt"
    pasta_saida = "audios_gerados"

    os.makedirs(pasta_saida, exist_ok=True)

    if not os.path.exists(arquivo_texto):
        print("Erro: o arquivo texto.txt não foi encontrado.")
        return

    texto = carregar_texto(arquivo_texto)

    if not texto.strip():
        print("Erro: o arquivo texto.txt está vazio.")
        return

    nome_audio = input("Digite o nome do áudio: ")
    nome_audio = limpar_nome_arquivo(nome_audio)

    formato = input("Escolha o formato: mp3 ou wav: ").lower().strip()

    if formato not in ["mp3", "wav"]:
        print("Formato inválido. Usando MP3 por padrão.")
        formato = "mp3"

    if formato == "wav":
        print("WAV não está disponível diretamente nesta versão do edge-tts.")
        print("Gerando MP3 no lugar...")
        formato = "mp3"

    caminho_saida = os.path.join(pasta_saida, f"{nome_audio}.{formato}")
    await gerar_mp3_unico(texto, caminho_saida)

    print()
    print("Pronto! Áudio gerado com sucesso:")
    print(caminho_saida)

if __name__ == "__main__":
    asyncio.run(main())
