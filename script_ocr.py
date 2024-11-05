# para baixar o pytessect: https://github.com/UB-Mannheim/tesseract/wiki

#C:\Program Files\Tesseract-OCR

from PIL import Image
import pytesseract
import cv2
import numpy as np

# Defina o caminho do Tesseract (caso necessário)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Carrega a imagem
imagem_caminho = r'F:\Receitas_Dona_Angela\imagem.jpeg'
img = cv2.imread(imagem_caminho)

# Pré-processamento: converter para escala de cinza
img_cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Aumentar contraste e normalizar a imagem
img_cinza = cv2.convertScaleAbs(img_cinza, alpha=1.5, beta=-50)

# Aplicar um filtro de desfoque para reduzir o ruído
img_denoised = cv2.medianBlur(img_cinza, 5)  # Aumentei para 5

# Binarização adaptativa para lidar com diferentes condições de iluminação
img_bin = cv2.adaptiveThreshold(img_denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                 cv2.THRESH_BINARY_INV, 11, 2)

# (Opcional) Aplicar dilatação para conectar caracteres
kernel = np.ones((3, 3), np.uint8)
img_dilated = cv2.dilate(img_bin, kernel, iterations=1)

# Executar o OCR com Tesseract
texto_detectado = pytesseract.image_to_string(img_dilated, lang='por')  # 'lang' para português

print("Texto detectado na imagem:")
print(texto_detectado)

# (Opcional) Exibir a imagem processada
cv2.imshow("Imagem Binária", img_dilated)
cv2.waitKey(0)
cv2.destroyAllWindows()
