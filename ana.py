import numpy as np
import cv2 as cv
import haadCascate
# método que retorna vazio
def analyse():
    return
    
def filtrosGenericos(Frame, referenceFrame):
    #tranforma a imagem de capturada e a referencia em cinza
    grayFrame = cv.cvtColor(Frame, cv.COLOR_BGR2GRAY)
    grayReferenceFrame = cv.cvtColor(referenceFrame, cv.COLOR_BGR2GRAY)
        
    #aplica o filtro gaussiano na imagem de capturada e a referencia em cinza
    grayBlurred = cv.GaussianBlur(grayFrame,(5,5),0)
    grayBlurredReferenceFrame = cv.GaussianBlur(grayReferenceFrame,(5,5),0)
        
    #diferença entre a imagems coletadas da camera e a imagem de referencia tanto em cima quanto em baixo
    DifferenceImage= cv.absdiff(grayBlurredReferenceFrame,grayBlurred)
    return DifferenceImage

def filtros_imagem1(Frame, ReferenceFrame):
    #aplica o filtro de binarização nas imagens de diferença(de cima e de de baixo)
    ret,DifferenceArea= cv.threshold(filtrosGenericos(Frame, ReferenceFrame), thresholdValue,255,cv.THRESH_BINARY)

    #conta o numero de pixels nas imagens binarizadas de cima e de baixo que não são pretos e salva em variáveis
   #chamadas Areas
    AreaCount= cv.countNonZero(DifferenceArea)
    return AreaCount

def filtros_imagem2(Frame, ReferenceFrame):
    #aplica o filtro  laplaciano nas imagens binarizadas
    PerimeterImage= cv.Laplacian(filtrosGenericos(Frame, ReferenceFrame), cv.CV_8U)

    #aplica o filtro de binarização nas imagens de diferença(de cima e de de baixo)
    ret,DifferencePerimeter= cv.threshold(filtrosGenericos(Frame, ReferenceFrame), thresholdValue, 255,cv.THRESH_BINARY)

    #conta o numero de pixels nas imagens que aplicou o laplaciano de cima e de baixo que não são pretos
    #e salva em variáveis chamadas Areas
    PerimeterCount= cv.countNonZero(DifferencePerimeter)

    return PerimeterCount

def monitorarArea(cam):
    global thresholdValue
    #coordenadas iniciais das janelas de cima e de baixo
    topAreaHeight, bottomAreaHeight, leftAreaHeight, rightAreaHeight= (20, 20, 20, 20)
    #valor de diferenca na deteccao de diferenca
    thresholdValue= 100
    #valores maximos de area e perimetro
    maxArea= 200
    maxPerimeter= 10000

    #coleta o primeiro frame da imagem da camera e usa como referencia para imagens futuras
    ret, referenceFrame = cam.read()
    #coordenadas finais das janelas de cima e de baixo
    height, width = referenceFrame.shape[:2]
    topReferenceFrame= referenceFrame.copy()[0:topAreaHeight, 0:width]
    bottomReferenceFrame= referenceFrame.copy()[height-bottomAreaHeight:height, 0:width]
    leftReferenceFrame= referenceFrame.copy()[topAreaHeight:height-bottomAreaHeight, 0:leftAreaHeight]
    rightReferenceFrame= referenceFrame.copy()[topAreaHeight:height-bottomAreaHeight, width-rightAreaHeight:width]
        

    isRecording= False
    beltObjectCount= 0
    #verifica se tem objeto na parte superior
    rightHasObject= False
    #verifica se tinha objeto na parte superior
    rightHadObject= False
    #verifica se tem objeto na parte inferior
    leftHasObject= False
    #verifica se tinha objeto na parte inferior
    leftHadObject= False
    #verifica se tem objeto na parte superior
    topHasObject= False
    #verifica se tinha objeto na parte superior
    topHadObject= False
    #verifica se tem objeto na parte inferior
    bottomHasObject= False
    #verifica se tinha objeto na parte inferior
    bottomHadObject= False

    while True:
        #abre a camera e armazena uma imagem dela
        ret, frame = cam.read()
        if not ret:
            print("no image")
            break
        #cria uma copia da camera e recorta a area em cima e em baixo para ser filmada
        topFrame= frame.copy()[0:topAreaHeight, 0:width]
        leftFrame= frame.copy()[topAreaHeight:height-bottomAreaHeight, 0:leftAreaHeight]
        rightFrame= frame.copy()[topAreaHeight:height-bottomAreaHeight, width-rightAreaHeight:width]
        bottomFrame= frame.copy()[height-bottomAreaHeight:height, 0:width]
        
        topAreaCount = filtros_imagem1(topFrame, topReferenceFrame)
        bottomAreaCount = filtros_imagem1(bottomFrame, bottomReferenceFrame)
        
        topPerimeterCount = filtros_imagem2(topFrame, topReferenceFrame)
        bottomPerimeterCount = filtros_imagem2(bottomFrame, bottomReferenceFrame)
        
        rightAreaCount = filtros_imagem1(rightFrame, rightReferenceFrame)
        leftAreaCount = filtros_imagem1(leftFrame, leftReferenceFrame)
        
        rightPerimeterCount = filtros_imagem2(rightFrame, rightReferenceFrame)
        leftPerimeterCount = filtros_imagem2(leftFrame, leftReferenceFrame)
        #mostra a imagem da camera
        cv.imshow('live',frame)
        #mostra as imagens recortadas e binarizadas de cima e de baixo
        #cv.imshow('TDA',topDifferenceArea)
        #cv.imshow('BDA',bottomDifferenceArea)
            
        print("topArea:",topAreaCount," |topPerimeter:",topPerimeterCount,"\n")
        print("bottomArea:",bottomAreaCount," | bottomPerimeter:",bottomPerimeterCount,"\n")
        
        print("rightArea:",rightAreaCount," |trightPerimeter:",rightPerimeterCount,"\n")
        print("leftArea:",leftAreaCount," | leftPerimeter:",leftPerimeterCount,"\n")
            
        #variavel que diz se tem objeto no canto superior
        topHasObject= (topAreaCount>maxArea and topPerimeterCount<maxPerimeter)
        
        leftHasObject= (leftAreaCount>maxArea and leftPerimeterCount<maxPerimeter)
        #variavel que diz se tem objeto no canto inferior
        bottomHasObject= (bottomAreaCount>maxArea and bottomPerimeterCount<maxPerimeter)
        
        rightHasObject= (rightAreaCount>maxArea and rightPerimeterCount<maxPerimeter)
        #condicional que testa se tem objeto no canto superior
        if topHasObject:
           #condicional que testa se tinha objeto no canto superior
            if not topHadObject:
                #contador de objetos passando no canto superior
                beltObjectCount += 1
                topHadObject= True
            else:
                topHadObject= False
            
        #condicional que testa se tem objeto no canto superior
        if bottomHasObject:
            bottomHadObject= True
        else:
            #condicional que testa se tinha objeto no canto inferior
            if bottomHadObject:
                #contador de objetos saindo no canto inferior
                beltObjectCount -= 1
                bottomHadObject= False

        if leftHasObject:
           #condicional que testa se tinha objeto no canto superior
            if not leftHadObject:
                #contador de objetos passando no canto superior
                beltObjectCount += 1
                leftHadObject= True
            else:
                leftHadObject= False
            
        #condicional que testa se tem objeto no canto superior
        if rightHasObject:
            rightHadObject= True
        else:
            #condicional que testa se tinha objeto no canto inferior
            if rightHadObject:
                #contador de objetos saindo no canto inferior
                beltObjectCount -= 1
                rightHadObject= False
        #variavel que diz se objeto na area monitorada
        isRecording= (topHasObject or bottomHasObject or rightHasObject or leftHasObject)
        if isRecording:
            cv.destroyAllWindows()
            haadCascate.goDetect(cam)
        #imprime o numero de objetos detectados
        print("\nOBJECT COUNT:",beltObjectCount)
            
    #apertar q para sair
        if cv.waitKey(100)== ord('q'):
            break
