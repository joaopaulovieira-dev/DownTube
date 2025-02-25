# DownTube

# Baixador de Vídeos e Playlists do YouTube com Python

Este projeto fornece um script Python para baixar vídeos e playlists do YouTube, utilizando as bibliotecas `pytubefix` e `ffmpeg`. Ele lida com resoluções progressivas e adaptativas, combinando streams de vídeo e áudio quando necessário, e inclui uma interface de linha de comando amigável.

## Características

*   **Download de Vídeos Únicos e Playlists:** Baixa tanto vídeos individuais quanto playlists completas do YouTube.
*   **Seleção de Resolução:** Permite especificar a resolução desejada (ex: 1080p, 720p) ou baixar a melhor resolução disponível.
*   **Streams Progressivos e Adaptativos:** Suporta tanto streams progressivos (vídeo e áudio combinados) quanto adaptativos (vídeo e áudio separados).
*   **Combinação Automática de Vídeo e Áudio:** Usa o `ffmpeg` para combinar automaticamente os streams de vídeo e áudio quando necessário (para streams adaptativos).
*   **Barras de Progresso:** Exibe barras de progresso (usando `tqdm`) durante o download dos vídeos e áudios.
*   **Efeitos de "Loading":** Apresenta animações de "loading" simples para indicar que o script está trabalhando.
*   **Tratamento de Erros:** Lida com URLs inválidas, vídeos indisponíveis e outros erros comuns.
*   **Nomes de Arquivo Seguros:** Garante que os nomes dos arquivos baixados sejam seguros para o sistema de arquivos, substituindo caracteres inválidos.
*   **Script de Instalação de Dependências:** Inclui um script separado para facilitar a instalação de todas as dependências (incluindo o `ffmpeg`) em sistemas Windows.

## Pré-requisitos

*   **Python 3.6+:**  O script foi desenvolvido e testado com Python 3.6 e versões superiores.  Versões mais antigas *podem* funcionar, mas não são garantidas.
*   **FFmpeg:**  O FFmpeg é *essencial* para combinar os streams de vídeo e áudio.  O script de instalação (`install_dependencies.py`) facilita a instalação do FFmpeg.
*   **Bibliotecas Python:**  O script usa as seguintes bibliotecas:
    *   `pytubefix`: Um fork do `pytube` com correções de bugs e melhorias.
    *   `tqdm`: Para exibir barras de progresso.

## Instalação

### Método 1: Usando o Script de Instalação (Recomendado - Windows)

A maneira mais fácil de configurar tudo, *especialmente no Windows*, é usar o script de instalação fornecido (`install_dependencies.py`).  Ele instala o `ffmpeg` (via Chocolatey, se possível, ou fornece instruções para instalação manual), o `pip` (se necessário), e as bibliotecas Python.

1.  **Clone o repositório (ou baixe os arquivos):**

    ```bash
    git clone [https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git](https://www.google.com/search?q=https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git)  # Substitua pelos seus dados
    cd SEU_REPOSITORIO
    ```

    Se você não usa Git, baixe os arquivos `.py` do repositório e coloque-os em uma pasta.

2.  **Execute o script de instalação:**

    ```bash
    python requirements.py
    ```

    Siga as instruções na tela. O script tentará instalar o `ffmpeg` automaticamente usando o Chocolatey (um gerenciador de pacotes para Windows). Se isso falhar, ou se você preferir, ele fornecerá instruções detalhadas para a instalação manual do `ffmpeg`.

### Método 2: Instalação Manual (Linux, macOS, ou se você preferir)

1.  **Instale o Python 3.6+:**  Certifique-se de ter o Python 3.6 ou superior instalado.  Você pode verificar com `python --version` ou `python3 --version`.

2.  **Instale o FFmpeg:**
    *   **Linux (Debian/Ubuntu):**
        ```bash
        sudo apt update
        sudo apt install ffmpeg
        ```
    *   **Linux (Fedora/CentOS/RHEL):**
        ```bash
        sudo dnf install ffmpeg  # Ou yum, dependendo da versão
        ```
    *   **macOS (usando Homebrew):**
        ```bash
        brew install ffmpeg
        ```
    *   **Windows (Manual - *se* você *não* usou `install_dependencies.py`):**  Siga *cuidadosamente* as instruções detalhadas no script `install_dependencies.py` para baixar, descompactar e adicionar o `ffmpeg` ao PATH.  *Não* use a instalação manual se você já usou o script.

3.  **Instale as bibliotecas Python:**

    ```bash
    pip install pytubefix tqdm
    ```

    (Ou `pip3 install pytubefix tqdm`, se você tiver ambas as versões do Python instaladas.)

## Uso

1.  **Execute o script principal:**

    ```bash
    python main.py  # Ou o nome que você deu ao script
    ```

2.  **Siga as instruções:** O script irá perguntar:
    *   Se você quer baixar uma playlist ou um vídeo único.
    *   A URL do vídeo ou playlist.
    *   A resolução desejada (opcional - pressione Enter para a melhor disponível).
    *   A pasta de destino (opcional - pressione Enter para usar a pasta "downloads").

3.  **Aguarde:** O script baixará os vídeos, combinará os streams de áudio e vídeo (se necessário) e salvará os arquivos na pasta especificada.

## Código

### `main.py`

```python
# Cole o código completo de baixar_e_combinar.py aqui
import pytubefix as pytube
import os
from tqdm import tqdm
import subprocess
import re
import time


def sanitize_filename(filename):
    """Remove/substitui caracteres inválidos em nomes de arquivos."""
    bad_chars = r'[<>:"/\\|?*\[\]\(\)]'
    return re.sub(bad_chars, '_', filename)

def print_loading(message, delay=0.2):
    """Simula um efeito de 'loading'."""
    for _ in range(3):
        print(f"{message}", end=".", flush=True)
        time.sleep(delay)
    print("\r" + " " * (len(message) + 3) + "\r", end="", flush=True)

def baixar_playlist_youtube(url_playlist, pasta_destino="downloads", resolucao_desejada=None):
    """Baixa vídeos de uma playlist."""
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)

    try:
        print_loading("Carregando playlist")
        playlist = pytube.Playlist(url_playlist)
        print(f"Baixando playlist: {playlist.title}")

        video_urls = list(playlist.video_urls)
        if not video_urls:
            print("Playlist vazia.")
            return

        for url in tqdm(video_urls, desc="Baixando Vídeos", unit="video"):
            baixar_video_unico(url, pasta_destino, resolucao_desejada)

    except pytube.exceptions.RegexMatchError:
        print(f"URL inválida: {url_playlist}")
    except Exception as e:
        print(f"Erro: {e}")


def baixar_video_unico(url, pasta_destino="downloads", resolucao_desejada=None):
    """Baixa um vídeo, prioriza resolução/progressivo. Combina com ffmpeg."""
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)

    try:
        print_loading("Conectando ao YouTube")
        yt = pytube.YouTube(url)
        print(f"\nBaixando: {yt.title}")

        stream = None

        # --- 1. Resolução específica ---
        if resolucao_desejada:
            print(f"Procurando resolução específica: {resolucao_desejada}", end="")
            print_loading("")
            stream = yt.streams.filter(progressive=True, file_extension='mp4', resolution=resolucao_desejada).first()
            if stream:
                print(f"Resolução encontrada (progressiva): {stream.resolution}")
                # Barra de progresso para streams progressivos
                with tqdm(total=stream.filesize, desc="Baixando", unit="B", unit_scale=True, unit_divisor=1024) as pbar:
                    def progress_func(stream, chunk, bytes_remaining):
                        pbar.update(len(chunk))
                    yt.register_on_progress_callback(progress_func)  # REGISTRA a função
                    stream.download(output_path=pasta_destino)
                print(f"Download concluído!")
                return

            print(f"Não há progressivo em {resolucao_desejada}. Tentando adaptativo...", end="")
            print_loading("")
            video_stream = yt.streams.filter(only_video=True, file_extension='mp4', resolution=resolucao_desejada).first()
            if video_stream:
                audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').order_by('abr').desc().first()
                if audio_stream:
                    print(f"Resolução do vídeo (adaptativo): {video_stream.resolution}")
                    stream = video_stream
                else:
                    print(f"Não há áudio para a resolução {resolucao_desejada}.")
                    video_stream = None
            else:
                print(f"Não há vídeo na resolução {resolucao_desejada}.")
                video_stream = None

        # --- 2. Melhor progressiva ---
        if stream is None:
            print("Procurando melhor resolução progressiva...", end="")
            print_loading("")
            stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            if stream:
                print(f"Resolução (progressiva): {stream.resolution}")
                # Barra de progresso para streams progressivos
                with tqdm(total=stream.filesize, desc="Baixando", unit="B", unit_scale=True, unit_divisor=1024) as pbar:
                    def progress_func(stream, chunk, bytes_remaining):
                        pbar.update(len(chunk))
                    yt.register_on_progress_callback(progress_func)  # REGISTRA a função
                    stream.download(output_path=pasta_destino)
                print(f"Download concluído!")
                return

        # --- 3. Fallback: Vídeo e Áudio Separados + Combinar ---
        if stream is None:
            print("Baixando separado (adaptativo)...", end="")
            print_loading("")
            video_stream = yt.streams.filter(only_video=True, file_extension='mp4').order_by('resolution').desc().first()
            audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').order_by('abr').desc().first()

            if not video_stream or not audio_stream:
                print(f"Não foi possível encontrar streams de vídeo e/ou áudio.")
                return

        if stream is None:
            stream = video_stream

        # Nomes de Arquivo TEMPORÁRIOS (seguros)
        safe_title = sanitize_filename(yt.title)
        video_filename = f"temp_video_{safe_title}.mp4"
        audio_filename = f"temp_audio_{safe_title}.mp4"
        output_filename = f"{safe_title}.mp4"

        video_path = os.path.join(pasta_destino, video_filename)
        audio_path = os.path.join(pasta_destino, audio_filename)
        output_path = os.path.join(pasta_destino, output_filename)

        if not stream.is_progressive:
            print(f"Resolução do vídeo: {video_stream.resolution}")
            print(f"Taxa de bits do áudio: {audio_stream.abr}")

            # Barras de progresso SEPARADAS para vídeo e áudio (adaptativos)
            with tqdm(total=video_stream.filesize, desc="Baixando Vídeo", unit="B", unit_scale=True, unit_divisor=1024) as pbar_video:
                with tqdm(total=audio_stream.filesize, desc="Baixando Áudio", unit="B", unit_scale=True, unit_divisor=1024) as pbar_audio:
                    def progress_func_video(stream, chunk, bytes_remaining):
                        pbar_video.update(len(chunk))
                    def progress_func_audio(stream, chunk, bytes_remaining):
                        pbar_audio.update(len(chunk))

                    yt.register_on_progress_callback(progress_func_video)
                    video_stream.download(output_path=pasta_destino, filename=video_filename)

                    yt.register_on_progress_callback(progress_func_audio)
                    audio_stream.download(output_path=pasta_destino, filename=audio_filename)

            # --- Combinar com ffmpeg (USANDO SUBPROCESS) ---
            try:
                print("Combinando com ffmpeg (subprocess)...", end="")
                print_loading("")
                comando = [
                    "ffmpeg",
                    "-i", video_path,
                    "-i", audio_path,
                    "-c:v", "copy",
                    "-c:a", "copy",
                    output_path,
                    "-y"  # Sobrescrever
                ]
                result = subprocess.run(comando, capture_output=True, text=True, check=True)
                print(f"Vídeo combinado: {output_filename}")


                # Remover arquivos temporários
                os.remove(video_path)
                os.remove(audio_path)
                print("Arquivos temporários removidos.")

            except subprocess.CalledProcessError as e:
                print(f"Erro ao combinar com ffmpeg (subprocess): {e}")
                print(f"  Código de erro: {e.returncode}")
                print(f"  Saída de erro: {e.stderr}")
                print("Arquivos separados mantidos.")
            except FileNotFoundError:
                print("Erro: ffmpeg não encontrado. Instale-o e adicione ao PATH.")
                print("Arquivos separados mantidos.")
        else:
            # Se for progressivo, já baixou.
            pass

    except pytube.exceptions.RegexMatchError:
        print(f"URL inválida: {url}.")
    except pytube.exceptions.VideoUnavailable:
        print(f"Vídeo indisponível: {url}.")
    except pytube.exceptions.PytubeFixError as e:
        print(f"Erro Pytube: {e}")
    except Exception as e:
        print(f"Erro: {e}")



def obter_url_e_tipo():
    """Obtém URL, tipo e resolução (opcional)."""
    while True:
        print("Escolha uma opção:")
        print("1. Playlist")
        print("2. Vídeo único")
        print("3. Sair")

        opcao = input("Opção: ").strip()

        if opcao == '1':
            url = input("URL da playlist: ").strip()
            tipo = "playlist"
        elif opcao == '2':
            url = input("URL do vídeo: ").strip()
            url = url.split("?")[0]  # Remove parâmetros
            tipo = "video"
        elif opcao == '3':
            return None, None, None
        else:
            print("Opção inválida.")
            continue

        resolucao = None
        if tipo in ("video", "playlist"):
            print("Resolução (ex: 1080p, 720p, Enter para melhor):")
            resolucao = input("Resolução: ").strip().lower()
            if resolucao and not resolucao.endswith("p"):
                print("Formato inválido. Usando a melhor.")
                resolucao = None

        return url, tipo, resolucao


if __name__ == "__main__":
    url, tipo, resolucao_desejada = obter_url_e_tipo()

    if url and tipo:
        pasta_destino = input("Pasta de destino (Enter para 'downloads'): ").strip()
        pasta_destino = pasta_destino or "downloads"

        if tipo == "playlist":
            baixar_playlist_youtube(url, pasta_destino, resolucao_desejada)
        elif tipo == "video":
            baixar_video_unico(url, pasta_destino, resolucao_desejada)

    else:
        print("Encerrando.")
