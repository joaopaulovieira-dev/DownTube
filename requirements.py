import subprocess
import sys
import os

def run_command(command, shell=False):
    """Executa um comando no shell e retorna a saída e o código de erro."""
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True, shell=shell)
        return result.stdout, result.returncode
    except subprocess.CalledProcessError as e:
        return e.stderr, e.returncode
    except FileNotFoundError:
        return "Comando não encontrado.", 127 # Erro padrão quando não acha.

def check_python():
    """Verifica se o Python está instalado."""
    print("Verificando instalação do Python...")
    stdout, returncode = run_command([sys.executable, "--version"])
    if returncode == 0:
        print(f"  Python instalado: {stdout.strip()}")
        return True
    else:
        print("  Erro: Python não encontrado.  Instale o Python primeiro.")
        return False

def check_pip():
    """Verifica se o pip está instalado e o atualiza."""
    print("Verificando instalação do pip...")
    stdout, returncode = run_command([sys.executable, "-m", "pip", "--version"])
    if returncode == 0:
        print(f"  pip instalado: {stdout.strip()}")
        print("  Atualizando pip...")
        stdout, returncode = run_command([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        if returncode == 0:
            print("    pip atualizado com sucesso.")
        else:
            print(f"    Erro ao atualizar o pip:\n{stdout}")
        return True

    else:
        print("  Erro: pip não encontrado.  Instalando o pip...")
        #Tentar instalar o get-pip.py
        try:
            import urllib.request
            get_pip_url = "https://bootstrap.pypa.io/get-pip.py"
            print(f"    Baixando get-pip.py...")
            urllib.request.urlretrieve(get_pip_url, "get-pip.py")
            print(f"    Executando get-pip.py...")
            stdout, returncode = run_command([sys.executable, "get-pip.py"])
            if returncode == 0:
                print("Pip instalado com sucesso")
                os.remove("get-pip.py") #Limpa o arquivo.
                return True
            else:
                print(f"Erro ao instalar o pip: {stdout}")
                os.remove("get-pip.py")
                return False

        except Exception as e:
            print(f"Erro ao baixar/instalar o pip: {e}")
            if os.path.exists("get-pip.py"):
                os.remove("get-pip.py")
            return False



def install_python_packages():
    """Instala as bibliotecas Python necessárias."""
    print("Instalando bibliotecas Python...")
    packages = ["pytubefix", "tqdm", "ffmpeg-python"]
    for package in packages:
        print(f"  Instalando {package}...")
        stdout, returncode = run_command([sys.executable, "-m", "pip", "install", package])
        if returncode == 0:
            print(f"    {package} instalado com sucesso.")
        else:
            print(f"    Erro ao instalar {package}:\n{stdout}")

def check_ffmpeg():
    """Verifica se o FFmpeg está instalado e no PATH."""
    print("Verificando instalação do FFmpeg...")
    stdout, returncode = run_command(["ffmpeg", "-version"], shell=True)
    if returncode == 0:
        print(f"  FFmpeg instalado:\n{stdout.splitlines()[0]}")  # Mostra a primeira linha da saída
        return True
    else:
        print("  FFmpeg não encontrado no PATH.")
        return False

def install_ffmpeg_with_chocolatey():
    """Instala o FFmpeg usando Chocolatey."""
    print("Instalando FFmpeg com Chocolatey...")

    # 1. Verificar se o Chocolatey está instalado
    stdout, returncode = run_command(["choco", "-?"])
    if returncode != 0:
        print("  Chocolatey não encontrado. Instalando Chocolatey...")
        # Comando de instalação do Chocolatey (requer PowerShell como Administrador)
        install_command = "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
        
        try:
            # Executar o comando em um novo processo do PowerShell como Administrador
            subprocess.run(["powershell", "-Command", install_command], check=True, shell=True)
            print("  Chocolatey instalado com sucesso.")

            #Importante, recarregar as variáveis de ambiente.
            os.environ["PATH"] = os.environ["PATH"] #Forma porca, mas funciona.
            import site
            site.addsitedir(site.getusersitepackages()) #Recarrega os pacotes.

        except subprocess.CalledProcessError as e:
            print(f"  Erro ao instalar o Chocolatey: {e}")
            return False


    # 2. Instalar o FFmpeg
    print("  Instalando FFmpeg...")
    stdout, returncode = run_command(["choco", "install", "ffmpeg", "-y"])
    if returncode == 0:
        print("  FFmpeg instalado com sucesso via Chocolatey.")
        return True
    else:
        print(f"  Erro ao instalar o FFmpeg via Chocolatey:\n{stdout}")
        return False

def install_ffmpeg_manually():
    """Guia o usuário na instalação manual do FFmpeg."""
    print("-" * 40)
    print("Instalação Manual do FFmpeg (Siga os passos com atenção):")
    print("1. Baixe o FFmpeg:")
    print("   - Vá para: https://www.gyan.dev/ffmpeg/builds/")
    print("   - Baixe a versão 'ffmpeg-release-full.7z' ou 'ffmpeg-release-full.zip'.")
    print("2. Descompacte o arquivo baixado (use 7-Zip ou WinRAR).")
    print("3. Crie uma pasta chamada 'ffmpeg' em 'C:\\'.  O caminho final deve ser 'C:\\ffmpeg'.")
    print("4. Copie o *conteúdo* da pasta 'bin' (dentro da pasta que você descompactou) para 'C:\\ffmpeg'.")
    print("   - Você deve ter 'ffmpeg.exe', 'ffplay.exe' e 'ffprobe.exe' diretamente dentro de 'C:\\ffmpeg'.")
    print("5. Adicione 'C:\\ffmpeg' ao PATH do sistema (veja instruções detalhadas abaixo).")
    print("-" * 40)
    print("Adicionando ao PATH (Variáveis de Ambiente):")
    print("  1. Pressione a tecla Windows, digite 'variáveis de ambiente' e selecione 'Editar as variáveis de ambiente do sistema'.")
    print("  2. Clique em 'Variáveis de Ambiente...'.")
    print("  3. Na seção 'Variáveis do usuário', selecione 'Path' e clique em 'Editar...'.")
    print("  4. Clique em 'Novo' e adicione o caminho: C:\\ffmpeg")
    print("  5. Clique em 'OK' em todas as janelas.")
    print("  6. *Feche e reabra* o prompt de comando/terminal.")
    print("  7. Execute 'ffmpeg -version' para verificar.")
    print("-" * 40)
    input("Pressione Enter após seguir os passos acima e verificar a instalação manual...")

def main():
    """Função principal."""
    if not check_python():
        return

    check_pip()
    install_python_packages()

    if not check_ffmpeg():
        print("FFmpeg não encontrado.  Escolha uma opção:")
        print("1. Instalar FFmpeg automaticamente com Chocolatey (Recomendado)")
        print("2. Instalar FFmpeg manualmente (Requer download e configuração)")
        print("3. Sair")

        while True:
            choice = input("Opção: ").strip()
            if choice == '1':
                if install_ffmpeg_with_chocolatey():
                    break  # Sai do loop se a instalação for bem-sucedida
                else:
                    print("A instalação automática falhou. Tente a instalação manual ou verifique sua conexão com a internet.")
            elif choice == '2':
                install_ffmpeg_manually()
                if check_ffmpeg():  # Verifica novamente após a instalação manual
                    break
            elif choice == '3':
                print("Saindo...")
                return
            else:
                print("Opção inválida.")

    print("\nTodas as dependências foram instaladas/verificadas com sucesso!")
    print("Você pode agora executar o script de download do YouTube.")


if __name__ == "__main__":
    main()