from xml.dom.minidom import getDOMImplementation
from org.guga.contagil.scripting.utils import Janelas
from org.guga.contagil.scripting.utils import Textos
import os

def pesquisaBaixados():
    # cria tabela temporaria - mesma função da excel - para decidir qual fica
    t = tabelas.nova()
    t.addColuna(0, "Processo", "TEXTO")
    
    pastaPesquisar = u'D:\\IACarf\\AcordaoBaixadoCarf - completo'
    
    ind = 0
    numProcessoAnt = ''              
    
    for reg in os.listdir(pastaPesquisar):
        pasta = os.path.join(pastaPesquisar, reg)
        nomeArquivo = os.path.basename(pasta)
            
        if os.path.isfile(pasta): 
            numProcesso, ext = os.path.splitext(nomeArquivo)
            numProcesso = numProcesso[:17]    #equivale a esquerda com tamanho 17 - pega número do processo no ínicio do nome do arquivo
        
        if numProcesso != numProcessoAnt:
            t.setCelula( ind , 0 , numProcesso)
            ind = ind + 1        
            numProcessoAnt = numProcesso
    
    t.removeLinhasDuplicadas()   
    t.exportaTabelaUsuario("Processos baixados", False)

def incrementar(n): #cria índices a partir do valor recebido
    while n < 500:     
        yield n
        n += 1

def usarCopiarColar():
    listaProcessos = Janelas.pedeLista("Insira a lista de processos:")
    
    if (listaProcessos.size() > 0):
        listaProcessos = listaProcessos.getListaElementosDistintos()
        qtdeProcessos = str(listaProcessos.size())+" processo(s) carregado(s)"
        print(str(listaProcessos.size())+" processo(s) carregado(s).")
    else:
        qtdeProcessos = "Nenhum processo carregado."
        print("Nenhum processo carregado.")
    return listaProcessos

def lerTabelaUsuario():
    print("» Selecione uma tabela de usuário...")
    tabelaProcessos = Janelas.getTabelaUsuarioPerguntaUsuario()
    if (tabelaProcessos == None): 
        print("Nenhuma tabela selecionada.")
    else: 
        numeroColuna = Janelas.pedeTextoNoFormato("Digite o número da coluna onde estãos os números de processo (1 para a primeira coluna).","1", "NUMERO")
        if (numeroColuna == None): 
            print("Nenhuma coluna informada.")
        else:  
            if (int(numeroColuna) < 2): 
                numeroColuna = 0
            else: 
                numeroColuna = int(numeroColuna)-1
            listaProcessos = tabelaProcessos.getColunaComoLista(numeroColuna)
            print("número de processos selecionados ", len(listaProcessos))
    return listaProcessos
    
def consultaProcesso(nrProcesso):
    tab_usu_B = contagil.getTabelaUsuario("Processos baixados") 
    tab_B = tab_usu_B.getTabela() 
    listaProcessosBaixados = tab_B.getColunaComoLista('Processo')
    
    tab_A = tabelas.nova()
    numCol = incrementar(0)    
    tab_A.addColuna(next(numCol), 'Processo', 'TEXTO')
    tab_A.addColuna(next(numCol), 'Ementa', 'TEXTO')
    
    cont = 0
    linhaCarf = 0  
    for nrProcesso in listaProcessos:
        if nrProcesso in listaProcessosBaixados:
            continue
            
        try:
            web.abrirPagina("https://carf.fazenda.gov.br/sincon/public/pages/ConsultarJurisprudencia/consultarJurisprudenciaCarf.jsf")       
        except Exception as erro:
            print(f'Processo {nrProcesso} com erro ao acessar página consultarJurisprudenciaCarf. \nErro: {erro}.')
            continue    
    
        try:
            # formulario para pesquisa
            form = web.getPaginaAtual().getFormulario("consultaJurisprudenciaForm")
                
            form.setCampo("valor_pesquisa1", nrProcesso)
            form.setCampo("AJAXREQUEST", "_viewRoot")
            form.setCampo("consultaJurisprudenciaForm", "consultaJurisprudenciaForm")
            form.setCampo("j_id51", "j_id51")
        
            web.submeterFormulario(form)
        
            # formulario para detalhamento
            form = web.getPaginaAtual().getFormulario("formAcordaos")
        
            form.setCampo("tblJurisprudencia:0:numDecisao", "tblJurisprudencia:0:numDecisao")
            form.removeCampo("j_id89")
            form.removeCampo("botaoImprimir")
        
            web.submeterFormulario(form)
            
            tabela = web.getPaginaAtual().getTabela(0) 

            for linha in range(0, tabela.getNumLinhas()):
                if str(tabela.getCelula(linha, "COLUNA-00"))[:6] == "Ementa":
                    tab_A.setCelula(linhaCarf, "Processo", nrProcesso)
                    tab_A.setCelula(linhaCarf, "Ementa", tabela.getCelula(linha, "COLUNA-0"))
                    linhaCarf += 1
                    
        except Exception as erro:
            print(f'Processo {nrProcesso} com erro ao acessar o formulário consultaJurisprudenciaForm. \nErro: {erro}.')
            continue
              
        cont += 1                     
        if cont > 50:
            tab_A.exportaTabelaUsuario("Carf - ementas temp", False)
            gravados += cont
            print(f'{gravados} processos gravados.')
            cont = 0
    
        try:
            # pegando o anexo
            form = web.getPaginaAtual().getFormulario("formAcordaos")
            form.removeCampo("formAcordaos:j_id64")
            form.removeCampo("botaoImprimir")
            form.setCampo("formAcordaos:_idcl","formAcordaos:j_id60:0:j_id61")
            web.submeterFormulario(form)
            web.exportaConteudoBinario("D:\\IACarf\\AcordaoBaixadoCarf\\"+nrProcesso+"_AcordaoCarf.pdf")              
        except Exception as erro:
            print(f'Processo {nrProcesso} com erro no download do acórdão. \nErro: {erro}.')
            continue 
            
    tab_A.exportaTabelaUsuario("Carf - ementas temp", False) 
    tab_A.exportaTabelaUsuario("Carf - ementas", True)               
  
pesquisaBaixados()
lista = ["Usar copiar e colar", "Ler tabela de usuário"]                
resposta = janelas.pedeOpcao("Escolha o modo de incluir a lista de processos", lista)
if resposta == "Usar copiar e colar":
    listaProcessos = usarCopiarColar()
else:
    listaProcessos = lerTabelaUsuario()
    
consultaProcesso(listaProcessos)