import cv2
import base64
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential


GITHUB_TOKEN = "COLOQUE_SEU_TOKEN_GITHUB_AQUI" 


endpoint = "digite o endpoint do seu recurso de IA aqui"
model_name = "gpt-4o-mini"

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(GITHUB_TOKEN),
)

def analisar_imagem_e_gerar_copy(imagem_cv2):
    """
    Função que pega a imagem da webcam, codifica e envia para o GPT-4o.
    """
    print("🤖 Processando imagem com IA... aguarde...")
    

    _, buffer = cv2.imencode('.jpg', imagem_cv2)
    imagem_base64 = base64.b64encode(buffer).decode('utf-8')
    url_imagem = f"data:image/jpeg;base64,{imagem_base64}"

    # 2. Preparar o prompt de Marketing
    prompt_sistema = """
    Você é um especialista em Marketing Digital e Copywriting. 
    Seu objetivo é analisar a imagem de um produto e criar um post de vendas curto e atraente.
    Retorne APENAS no seguinte formato:
    
    📦 PRODUTO: [Nome do produto identificado]
    🔥 LEGENDA: [Uma frase criativa e persuasiva para vender]
    🎯 PÚBLICO: [Quem compraria isso]
    Hashtags: #exemplo #marketing
    """

    
    try:
        response = client.complete(
            messages=[
                SystemMessage(content=prompt_sistema),
                UserMessage(content=[
                    {"type": "text", "text": "Analise este produto e crie o post."},
                    {"type": "image_url", "image_url": {"url": url_imagem}}
                ]),
            ],
            model=model_name,
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Erro na IA: {e}"


webcam = cv2.VideoCapture(0)

print("------------------------------------------------")
print("🎥 MARKETING CAM INICIADA")
print("1. Aponte um produto para a câmera.")
print("2. Aperte a tecla 'Espaço' para gerar o anúncio.")
print("3. Aperte 'ESC' para sair.")
print("------------------------------------------------")

while webcam.isOpened():
    validacao, frame = webcam.read()
    if not validacao:
        break

 
    cv2.imshow("Marketing Cam - Aperte ESPACO para analisar", frame)

    tecla = cv2.waitKey(5)
  
    if tecla == 27: 
        break
   
    elif tecla == 32:
       
        cv2.imshow("Marketing Cam - Aperte ESPACO para analisar", frame)
        cv2.waitKey(100) 
        
       
        resultado = analisar_imagem_e_gerar_copy(frame)
        
        print("\n" + "="*40)
        print(resultado)
        print("="*40 + "\n")
        print("Pode mostrar o próximo produto...")

webcam.release()
cv2.destroyAllWindows()