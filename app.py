import os
import pytesseract
from PIL import Image
from flask import Flask, render_template, request

# Caminho para o diretório onde o executável do Tesseract está localizado
tesseract_dir = r'C:\Program Files\Tesseract-OCR'

# Configurando o caminho para o arquivo de treinamento do Tesseract (por.traineddata)
tessdata_dir = os.path.join(tesseract_dir, 'tessdata')
os.environ['TESSDATA_PREFIX'] = tessdata_dir

app = Flask(__name__)

def extrair_texto_da_imagem(caminho_imagem):
    try:
        # Carregando a imagem
        imagem = Image.open(caminho_imagem)

        # Extraindo o texto da imagem usando o Tesseract OCR
        texto_extraido = pytesseract.image_to_string(imagem, lang='por')

        return texto_extraido

    except Exception as e:
        print("Erro ao extrair texto da imagem:", str(e))
        return None

def verificar_documento(texto_documento):
    # Verifique se o texto contém palavras-chave ou informações específicas de documento válido.
    palavras_chave_validas = ["CARTEIRA NACIONAL DE HABILITAÇÃO", "Cadastro de Pessoas Físicas", "REGISTRO DE IDENTIDADE CIVIL"]
    
    for palavra_chave in palavras_chave_validas:
        if palavra_chave in texto_documento:
            return True

    return False

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        imagem = request.files['imagem']
        caminho_imagem = 'uploads/' + imagem.filename
        imagem.save(caminho_imagem)

        texto_documento = extrair_texto_da_imagem(caminho_imagem)

        if texto_documento:
            if verificar_documento(texto_documento):
                resultado = "Documento válido."
            else:
                resultado = "Documento inválido."
        else:
            resultado = "Não foi possível extrair texto da imagem."

        # Renderiza a página de resultado com o texto extraído
        return render_template('resultado.html', resultado=resultado)

    return render_template('index.html')

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
