import os
import shutil
import re
from org.guga.contagil.scripting.utils import PDFExtrator
from org.guga.contagil.scripting.utils import ArquivoPDF

from nltk.tokenize import sent_tokenize

def incrementar(n): #cria índices a partir do valor recebido
    while n < 900:     
        yield n
        n += 1

def atributo_assunto(acordao):          
    try:            
        limites = "assunto: (.*)\n"
        assunto = re.search(limites, acordao).group(1)
        assunto = assunto.replace('  ', ' ')
        assunto = assunto.replace('  ', ' ')
        assunto = assunto.strip().lower()
        assunto = assunto.lstrip().rstrip()
        if 'irpj' in assunto:
            assunto = 'irpj'                                                                                                     
        elif 'imposto sobre a renda das pessoas jur' in assunto:
            assunto = 'irpj'   
        elif 'imposto sobre a renda de pessoa jur' in assunto:
            assunto = 'irpj'  
        elif 'imposto sobre a renda pessoa jur' in assunto:
            assunto = 'irpj'
        elif 'contribuição social' in assunto:
            assunto = 'csll'             
        elif 'irpf' in assunto:
            assunto = 'irpf'                                                                                                                              
        elif 'imposto sobre a renda de pessoa f' in assunto:
            assunto = 'irpf'                                                                                                                 
        elif 'imposto sobre a renda pessoa f' in assunto:
            assunto = 'irpf'
        elif 'contribuição para o financiamento' in assunto:
            assunto = 'cofins'
        elif 'contribuição para o pis' in assunto:
            assunto = 'pis'                                                                                                                                                     
        elif 'imposto sobre a renda retido' in assunto:
            assunto = 'irrf'
        elif 'contribuições sociais' in assunto:
            assunto = 'cp'                                                                                                                                                                                                                                                                                                                                                                                                                                                       
        elif 'ngdt' in assunto:
            assunto = 'ngdt'                                                                                                                                                                   
        elif 'normas gerais' in assunto:
            assunto = 'ngdt'                                                                                                                                                                             
        elif 'normas de administração' in assunto:
            assunto = 'nadm'                                                                                                                                                                                       
        elif 'obriga' in assunto:
            assunto = 'obrig'                                                                                                                                                                                                 
        elif 'outro' in assunto:
            assunto = 'outros'                                                                                                                                                                                                                                                                                                                                                                                                                               
        elif 'processo' in assunto:
            assunto = 'paf'
        elif 'imposto sobre produtos' in assunto:
            assunto = 'ipi'                                                              
        elif 'imposto sobre a exportação' in assunto:
            assunto = 'ie'                                                                         
        elif 'imposto sobre a importação' in assunto:
            assunto = 'ii'                                                                                   
        elif 'imposto sobre a propriedade' in assunto:
            assunto = 'itr'                         
        elif 'simples nacional' in assunto:
            assunto = 'sn'                                                                                                                                                                                                                                     
        elif 'simples' in assunto:
            assunto = 'simples'                                                                                                                                                                                                                                        
        elif 'sistema' in assunto:
            assunto = 'simples'                                                                                                                                                                                                                                                  
        elif 'regimes aduaneiros' in assunto:
            assunto = 'aduana'
        elif 'imposto sobre operações' in assunto:
            assunto = 'iof'            
        elif 'contribuição provisória' in assunto:
            assunto = 'cpmf'              
        elif 'contribuição de intervenção' in assunto:
            assunto = 'cide'                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
        elif 'direitos antidumping' in assunto:
            assunto = 'antidumping'                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
    except:
        assunto = ""
    return assunto     
       
def atributo_materia(acordao):
    try:
        limites = "mat.ria(.*)\n"
        materia = re.search(limites, acordao).group(1)
        materia = materia.strip().lower()
    except:
        materia = ""     
    return materia  
  
def atributo_presidente(acordao):
    try:                    
        limites = "\n(.*)presidente"
        presidente = re.search(limites, acordao).group(1)
        presidente = presidente.strip().lower()
        presidente = re.sub('[^\wÀ-ú ]','', presidente)
        presidente = re.sub('presidente [a-zA-Z_0-9-–,_ ]+','', presidente)
    except:
        presidente = ""
    return presidente  
    
def atributo_conselheiros(acordao):
    try:            
        limites = "(?s)julgamento os conselheiros(.*)"
        conselheiros = re.search(limites, acordao).group(1)
        conselheiros = conselheiros.replace('  ', ' ')
        conselheiros = conselheiros.replace('  ', ' ')
        conselheiros = conselheiros.replace(':', ' ')
        conselheiros = re.sub('\([a-zA-Z_0-9-–,_ ]+\)', '', conselheiros)
        conselheiros = conselheiros.strip()
    except:
        conselheiros = "erro"
        
    if conselheiros == 'erro':  
        try:               
            limites = "(?s)conselheiros(.*)"
            conselheiros = re.search(limites, acordao).group(1)
            conselheiros = conselheiros.replace('  ', ' ')
            conselheiros = conselheiros.replace('  ', ' ')
            conselheiros = conselheiros.replace(':', ' ')
            conselheiros = re.sub('\([a-zA-Z_0-9-–,_ ]+\)', '', conselheiros)
            conselheiros = conselheiros.strip()
        except:
            conselheiros = ""         
        
    return conselheiros
    
def atributo_decisao(acordao):
    try:    
        limites = "(?i)unanimidade|maioria|voto de qualidade"
        decisao = re.search(limites, acordao).group(0)
        decisao = decisao.strip().lower()
    except:
        decisao = ""          
    return decisao  
            
def atributo_recurso(acordao):
    try:
        limites = "recurso nº(.*)\n"
        recurso = re.search(limites, acordao).group(1)
    except:
        recurso = "erro"
        
    if recurso == 'erro':  
        try:
            limites = "recurso(.*)\n"
            recurso = re.search(limites, acordao).group(1)
        except:
            recurso = ""
            
    recurso = re.sub(r'\d', '', recurso)
    recurso = recurso.replace('.', '')
    recurso = recurso.replace('­', '')
    recurso = recurso.replace('-', '')
    recurso = recurso.replace('?', '')
    recurso = recurso.strip().lower()                
    recurso = recurso.replace('nº', '')
    recurso = recurso.replace('n°', '')
    recurso = recurso.lstrip().rstrip() 
    return recurso    

def atributo_relator(acordao):
    try:                           
        limites = "\n(.*)Presidente e"
        relator = re.search(limites, acordao).group(1)
        relator = relator.strip().lower()
        relator = re.sub('[^\wÀ-ú ]','', relator)
        relator = re.sub('presidente [a-zA-Z_0-9-–,_ ]+','', relator)
        relator = relator.lstrip().rstrip()
    except:
        relator = "erro"
     
    if relator == 'erro':  
        try:               
            limites = "\n(.*)Relator"
            relator = re.search(limites, acordao).group(1)
            relator = relator.strip().lower()
            relator = re.sub('[^\wÀ-ú ]','', relator)
            relator = re.sub('presidente [a-zA-Z_0-9-–,_ ]+','', relator)
            relator = relator.lstrip().rstrip()
        except:
            relator = "erro"
            
    if relator == 'erro':  
        try:               
            limites = "\n(.*)Redator"
            relator = re.search(limites, acordao).group(1)
            relator = relator.strip().lower()
            relator = re.sub('[^\wÀ-ú ]','', relator)
            relator = re.sub('presidente [a-zA-Z_0-9-–,_ ]+','', relator)
            relator = relator.lstrip().rstrip()
        except:
            relator = ""            
    return relator

def limpar_texto(texto_recebido):
    texto_recebido = texto_recebido.replace('CPC.', 'CPC')
    texto_recebido = texto_recebido.replace('CC.', 'CC')
    texto_recebido = texto_recebido.replace('ART.','ARTIGO')
    texto_recebido = texto_recebido.replace('ARTS.','ARTIGOS') 
    
    texto_recebido = re.sub('([0-9]*)[\.]*([0-9]+,[0-9]+)', r'\1\2', texto_recebido) #tratamento valores numéricos em real. Exclui o ponto, pois estava influenciando a tokenização.      
    texto_recebido = re.sub('([0-9]+)[.]+([0-9]+)\/([0-9]+)\.', r'\1\2 de \3,', texto_recebido) #altera a codificação de leis. De 9.240/96 para 9240 de 96 e nas ementas troca o ponto final para vírgula.
    texto_recebido = re.sub('([0-9]+)[.]+([0-9]+)\/([0-9]+)', r'\1\2 de \3', texto_recebido) #altera a codificação de leis. De 9.240/96 para 9240 de 96     
    texto_recebido = re.sub('([A-Z0-9À-Ü]+[ ]+[A-Z0-9À-Ü]+)\.', r'\1,', texto_recebido) #tratamento para ementas. substitui o ponto após duas palavras maiúsculas por vírgula.

    texto_recebido = re.sub('([A-ZÀ-Ü]+[0-9]*[A-ZÀ-Ü]*)\.', r'\1,', texto_recebido) #tratamento para ementas. substitui o ponto após palavra maiúscula por vírgula.
    texto_recebido = re.sub('(\([A-ZÀ-Ü ]+[0-9]*\))\.', r'\1,', texto_recebido) #tratamento para ementas. substitui o ponto final por vírgula após palavras maiúsculas com número dentro de parênteses (ANO DE 2003). 
    texto_recebido = re.sub('([A-ZÀ-Ü]+[ ]+[0-9]+)\.', r'\1,', texto_recebido) #tratamento para ementas. substitui o ponto final por vírgula em datas. DE 1995.

    texto_recebido = texto_recebido.lower()
    texto_recebido = texto_recebido.replace("\xAD","-") #transforma o soft hiphen em hífen.
    texto_recebido = re.sub('n[º°]', '', texto_recebido)
    texto_recebido = re.sub('[º°]', '', texto_recebido)
    texto_recebido = re.sub('(\((.)*grif[a-zà-ú ]+[a-zà-úA-Z_0-9-–,_ ]+\))', '', texto_recebido)
    texto_recebido = re.sub('(\((.)*real[a-zà-ú ]+[a-zà-úA-Z_0-9-–,_ ]+\))', '', texto_recebido)
    texto_recebido = re.sub('(\((.)*negrit[a-zà-ú ]+[a-zà-úA-Z_0-9-–,_ ]+\))', '', texto_recebido)
    texto_recebido = re.sub('(\(redação [\wÀ-ú_0-9-–.,º°_ ]+\))', '', texto_recebido)
    texto_recebido = re.sub('[eéEÉ] como voto.', '', texto_recebido)
    texto_recebido = re.sub('(\. .*)razão[, ]*pela qual', ', razão, pela qual', texto_recebido)
    
    texto_recebido = re.sub('conselheir. [a-zà-ú ]+[a-zA-Z_0-9-–,_ ]+.', '', texto_recebido)
    texto_recebido = re.sub('\.[ ]*\.', '.', texto_recebido) #substitui dois pontos por um ponto final (. .), (..), (.    .)
    
    texto_recebido = re.sub('\.[\n ]+dele conheço', ' dele conheço', texto_recebido)
    
    texto_recebido = re.sub('\[[\.]+\]', '', texto_recebido) #[...]
    texto_recebido = re.sub('\([\.]+\)', '', texto_recebido) #(...)
    texto_recebido = texto_recebido.replace('doc.', 'doc')
    texto_recebido = texto_recebido.replace('cpc.', 'cpc')
    texto_recebido = texto_recebido.replace('rel.', 'rel')
    texto_recebido = texto_recebido.replace('cc.', 'cc')
    texto_recebido = re.sub('[ ][ ]+', ' ', texto_recebido) #excluir espaços duplos   
    
    texto_recebido = texto_recebido.replace('(documento assinado digitalmente)','') 
    texto_recebido = texto_recebido.replace('documento assinado digitalmente','') 
    texto_recebido = texto_recebido.replace('assinado digitalmente','')
    texto_recebido = texto_recebido.replace('(assinatura digital)','')
    texto_recebido = texto_recebido.replace('assinatura digital','')
    texto_recebido = texto_recebido.replace('art.','artigo')
    texto_recebido = texto_recebido.replace('arts.','artigos')
    texto_recebido = texto_recebido.replace('fl.','folha')
    texto_recebido = texto_recebido.replace('fls.','folhas')
    texto_recebido = texto_recebido.replace('“','')
    texto_recebido = texto_recebido.replace('”','')
    texto_recebido = texto_recebido.replace('–','')
    texto_recebido = texto_recebido.replace('"','')
    texto_recebido = texto_recebido.replace("'",'')
    texto_recebido = texto_recebido.replace(";",',')
    texto_recebido = texto_recebido.replace("•", "")
    texto_recebido = texto_recebido.replace("?", ",")
    texto_recebido = texto_recebido.replace("?", ",")
    texto_recebido = texto_recebido.lstrip().rstrip()

    return texto_recebido

def parametro_PdfClasse_leitura_preliminar(pdfClasse, pastaPesquisarPdf, Pdf):
    pdfClasse.setRotacaoMaxima(5)
    pdfClasse.setPosicaoYMinima(782.30)
    tamanhoFonteDesprezar = 0
    try:
        pdf = pdfClasse.abrirPDFComoTexto(pastaPesquisarPdf, Pdf)
        tab = pdfClasse.getDadosUltimaExtracao().getTamanhosAmostras(True)       
        for linhaFonte in range(0, tab.getNumLinhas()):  
            if 'Impresso em ' in tab.getCelula(linhaFonte, 'TEXTO') or 'Assinado digitalmente em'  in tab.getCelula(linhaFonte, 'TEXTO'):
                tamanhoFonteDesprezar = tab.getValorNumerico(linhaFonte, 'TAMANHO')
                break
    except:
        pass
    return tamanhoFonteDesprezar
            
def parametro_PdfClasse_leitura_definitiva(pdfClasse, tamanhoFonteDesprezar):
    pdfClasse.setRotacaoMaxima(5)
    pdfClasse.setPosicaoYMaxima(782.30)
    pdfClasse.setPosicaoYMinima(64.32)
    pdfClasse.addTamanhoDesprezar(tamanhoFonteDesprezar)
        
def processamento():

    tab_B = tabelas.nova()
    tab_B.addColuna(0, 'Processo', 'TEXTO')
    tab_B.addColuna(1, 'Recurso', 'TEXTO')
    tab_B.addColuna(2, 'Materia', 'TEXTO')
    tab_B.addColuna(3, 'Assunto', 'TEXTO')
    tab_B.addColuna(4, 'Relator', 'TEXTO')
    tab_B.addColuna(5, 'Presidente', 'TEXTO')
    tab_B.addColuna(6, 'Conselheiros', 'TEXTO')
    tab_B.addColuna(7, 'Decisao', 'TEXTO')
    tab_B.addColuna(8, 'Voto vencedor', 'TEXTO')    
    
    tab_D = tabelas.nova()
    tab_D.addColuna(0, "Processo", "TEXTO")
    numCol = incrementar(1)
    for iOcor in range(1, 511): 
        tab_D.addColuna(next(numCol), "Frase"+str(iOcor).zfill(3), "TEXTO")  
                      
    # janela para escolher a pasta com os arquivos das impugnações a serem pesquisados
    pastaPesquisarPdf = janelas.pedePasta(u"{}: {}".format('Escolha a pasta com os PDF a serem pesquisados','' ), )
    
    pdfClasse = PDFExtrator()
            
    indLinha = 0         
    for Pdf in os.listdir(pastaPesquisarPdf):
        if Pdf[-3:] != "pdf":
            continue
                 
        nomeSemExtensao = Pdf.rstrip('.pdf') #retira a extensão pdf do nome do arquivo
        
        try:
            pdfClasse = PDFExtrator()
            tamanhoFonteDesprezar = parametro_PdfClasse_leitura_preliminar(pdfClasse, pastaPesquisarPdf, Pdf)

            pdfClasse = PDFExtrator()
            parametro_PdfClasse_leitura_definitiva(pdfClasse, tamanhoFonteDesprezar)    
            
            pdf = pdfClasse.abrirPDFComoTexto(pastaPesquisarPdf, Pdf)
            txtPdf = pdf.getTexto()               
            
            acordao = ""
            relatorio = ""
            voto = ""
            votoVencedor = "" 
            fimRelatorio = 0
            inicioVoto = 0
            
            matchRelatorio = re.search('\n( *Relat.rio *)\n', txtPdf)
            matchVoto = re.search('\n( *Voto *)\n', txtPdf)
            matchVotoVencedor = re.search('\n( *Voto Vencedor *)\n', txtPdf)
            matchVotoVencido = re.search('\n( *Voto Vencido *)\n', txtPdf)

            if matchVoto:
                fimRelatorio = matchVoto.start()
                inicioVoto = matchVoto.end()
            else:
                if matchVotoVencedor:
                    fimRelatorio = matchVotoVencedor.start()
                    inicioVoto = matchVotoVencedor.end() 
                    votoVencedor = "sim" 
                if matchVotoVencido:
                    fimRelatorio = matchVotoVencido.start()                  

            if matchRelatorio:
                acordao = txtPdf[:matchRelatorio.start()] 
                acordao = acordao.strip() 
                
                if fimRelatorio - matchRelatorio.end() < 65000:
                    relatorio = txtPdf[matchRelatorio.end():fimRelatorio]
                else:    
                    relatorio = txtPdf[matchRelatorio.end():matchRelatorio.end()+65000]
                         
                relatorio = relatorio.strip()  
            
            relator = atributo_relator(acordao)              
            voto = txtPdf[inicioVoto:len(txtPdf)]       
                          
        except: #copia o DD com problema para outra pasta
            print(Pdf, " - arquivo com erro ou não pesquisável") 
            continue                                                                                                                                                                                                                                                                                                            
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
        acordao = limpar_texto(acordao)
       
        match = re.search('processo', acordao)
        if match:    
            acordao = acordao[match.start():]
        
        relatorio = limpar_texto(relatorio)
        
        voto = limpar_texto(voto) 
        voto = voto.replace(relator,'')
        voto = voto.replace('- relator','')
        voto = voto.lstrip().rstrip()
                       
        recurso = atributo_recurso(acordao) 
        materia = atributo_materia(acordao)
        assunto = atributo_assunto(acordao)
        presidente = atributo_presidente(acordao)
        conselheiros = atributo_conselheiros(acordao)
        decisao = atributo_decisao(acordao)          
               
        tab_B.setCelula(indLinha, "Processo", nomeSemExtensao[:17])
        tab_B.setCelula(indLinha, "Recurso" , recurso)                                                                                                                                                 
        tab_B.setCelula(indLinha, "Materia" , materia)
        tab_B.setCelula(indLinha, "Assunto" , assunto)             
        tab_B.setCelula(indLinha, "Relator" , relator)                                                                                                                                                 
        tab_B.setCelula(indLinha, "Presidente" , presidente)
        tab_B.setCelula(indLinha, "Conselheiros" , conselheiros)
        tab_B.setCelula(indLinha, "Decisao" , decisao)     
        tab_B.setCelula(indLinha, "Voto vencedor" , votoVencedor)  
        
        #grava tabela voto    
        frases = sent_tokenize(voto.lower())
        
        tab_D.setCelula(indLinha, "Processo", nomeSemExtensao[:17])
        iOcor = 0
        for frase in frases:
            iOcor += 1
            tab_D.setCelula(indLinha, "Frase"+str(iOcor).zfill(3), frase)
        
        if len(frases) > 510:
            print(nomeSemExtensao[:17], len(frases))
            continue
                   
        indLinha = indLinha + 1  
        
    print("{} pdf processados.".format(indLinha))      
    
    tab_B.exportaTabelaUsuario("Carf_atributos", 0, False)
    pasta = "D:\IACarf\csv"
    nomeArq = os.path.join(pasta, "Carf_atributos.txt")
    tab_B.exportaCSV(nomeArq)    
    
    tab_D.exportaTabelaUsuario("Carf_Voto_Dividido_Em_Frases", 0, False)
    pasta = "D:\IACarf\csv"
    nomeArq = os.path.join(pasta, "Carf_Voto_Dividido_Em_Frases.txt")
    tab_D.exportaCSV(nomeArq)

####### inicio
processamento()