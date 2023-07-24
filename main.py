import streamlit as st
import pandas as pd

st.set_page_config(page_title="DCCMAPI - AutoAvaliação", layout="wide")

docente_sel = 'Alexandre César Muniz de Oliveira'
ano_inicio_sel = 2019
ano_fim_sel = 2022

producao_periodico_colulm_config = {
    'id_docente': None,
    'nome': None, 
    'titulo': 'Título', 
    'tipo': None,
    'issn_ou_sigla': 'ISSN',
    'nome_local': 'Periódico',
    'ano': 'Ano',
    'qualis': 'Qualis', 
    'natureza': None,
    'percentile_ou_h5': 'Percentile', 
    'autores': None, 
    'doi': None
}

producao_evento_colulm_config = {
    'id_docente': None,
    'nome': None, 
    'titulo': 'Título', 
    'tipo': None,
    'issn_ou_sigla': 'SIGLA',
    'nome_local': 'Conferência',
    'ano': 'Ano',
    'qualis': 'Qualis', 
    'natureza': None,
    'percentile_ou_h5': 'H5', 
    'autores': None, 
    'doi': None
}


producao_periodico_todos_colulm_config = {
    'id_docente': None,
    'nome': 'Docente', 
    'titulo': 'Título', 
    'tipo': None,
    'issn_ou_sigla': 'ISSN',
    'nome_local': 'Periódico',
    'ano': 'Ano',
    'qualis': 'Qualis', 
    'natureza': None,
    'percentile_ou_h5': 'Percentile', 
    'autores': None, 
    'doi': None
}

producao_evento_todos_colulm_config = {
    'id_docente': None,
    'nome': 'Todos', 
    'titulo': 'Título', 
    'tipo': None,
    'issn_ou_sigla': 'SIGLA',
    'nome_local': 'Conferência',
    'ano': 'Ano',
    'qualis': 'Qualis', 
    'natureza': None,
    'percentile_ou_h5': 'H5', 
    'autores': None, 
    'doi': None
}


tecnica_colum_config = {
    'id_docente': None,
    'nome': None,     
    'tipo': 'Tipo',
    'titulo': 'Título', 
    'ano': 'Ano',
    'financiadora': 'Financiadora', 
    'outras_informacoes': None,
    'autores': None
}

tecnica_todos_colum_config = {
    'id_docente': None,
    'nome': 'Docente',     
    'tipo': 'Tipo',
    'titulo': 'Título', 
    'ano': 'Ano',
    'financiadora': 'Financiadora', 
    'outras_informacoes': None,
    'autores': None
}


orientacao_colum_config = {
    'id_docente': None,
    'nome': None,     
    'tipo': 'Tipo',
    'discente': 'Discente', 
    'titulo': 'Titulo', 
    'ano': 'Ano',
    'instituicao': 'Instituição', 
    'curso': 'Curso',
    'status': 'Status',
    'natureza' : None    
}

orientacao_todos_colum_config = {
    'id_docente': None,
    'nome': 'Docente',     
    'tipo': 'Tipo',
    'discente': 'Discente', 
    'titulo': 'Titulo', 
    'ano': 'Ano',
    'instituicao': 'Instituição', 
    'curso': 'Curso',
    'status': 'Status',
    'natureza' : None    
}


@st.cache_data
def loadData():  
    docentes = pd.read_csv('docentes.csv', delimiter=';')
    producao = pd.read_csv('producao.csv', delimiter=';')
    tecnica = pd.read_csv('tecnica.csv', delimiter=';')
    orientacao = pd.read_csv('orientacao.csv', delimiter=';')

    return docentes, producao, tecnica, orientacao

def refresh():
    print("refresh")

def main():
    docentes, producao, tecnica, orientacao = loadData()
    filtro_ori  = ''
    
    st.header("DCCMAPI - Auto Avaliação")
 
   
    [c1, c2, c3, c4] = st.columns([4, 1, 1, 1])
    with c1:
        docente_sel = st.selectbox("Selecione um Docente:",options=(docentes.nome))            
    with c2: 
        ano_inicio_sel = st.text_input("Ano inicial", value="2019")
        
    with c3:
        ano_fim_sel = st.text_input("Ano final", value="2022")

    #dashboard, 
    prod_tab, ori_tab, tec_tab = st.tabs(['Produção', 'Orientações', 'Técnicas'])

    #with dashboard:
    #    st.write('Estatísticas') 
    #    qualis_periodicos = producao.loc[(producao.tipo=='ARTIGO-PUBLICADO') | (producao.tipo=='ARTIGO-ACEITO-PARA-PUBLICACAO')].groupby(['qualis'])['qualis'].count()
    #    qualis_periodicos_ano = producao.loc[(producao.tipo=='ARTIGO-PUBLICADO') | (producao.tipo=='ARTIGO-ACEITO-PARA-PUBLICACAO')].groupby(['qualis','ano'])['qualis', 'ano'].count()
    #    st.dataframe(qualis_periodicos_ano)
        

        

    with prod_tab:
        st.write('Produção')

        tipo_prod = st.radio("Tipo", options=['Periódicos', 'Eventos'], horizontal=True)
        if docente_sel != 'Todos':
            if  tipo_prod == 'Periódicos':                
                st.dataframe(producao.loc [ (producao['nome'] == docente_sel) 
                                            & (producao['ano'] >= int(ano_inicio_sel) )
                                            & (producao['ano'] <= int(ano_fim_sel) ) 
                                            & ((producao['tipo'] == 'ARTIGO-ACEITO-PARA-PUBLICACAO' ) 
                                            | (producao['tipo'] == 'ARTIGO-PUBLICADO' ))], 
                                    column_config = producao_periodico_colulm_config)
            else:
                st.dataframe(producao.loc [ (producao['nome'] == docente_sel) 
                                            & (producao['ano'] >= int(ano_inicio_sel) )
                                            & (producao['ano'] <= int(ano_fim_sel) )                                         
                                            & (producao['tipo'] == 'TRABALHO-EM-EVENTOS' )], 
                                            column_config=producao_evento_colulm_config)
        else:
            if  tipo_prod == 'Periódicos':                
                st.dataframe(producao.loc [(producao['ano'] >= int(ano_inicio_sel) )
                                            & (producao['ano'] <= int(ano_fim_sel) ) 
                                            & ((producao['tipo'] == 'ARTIGO-ACEITO-PARA-PUBLICACAO' ) 
                                            | (producao['tipo'] == 'ARTIGO-PUBLICADO' ))], 
                                    column_config = producao_periodico_todos_colulm_config)
            else:
                st.dataframe(producao.loc [ (producao['ano'] >= int(ano_inicio_sel) )
                                            & (producao['ano'] <= int(ano_fim_sel) )                                         
                                            & (producao['tipo'] == 'TRABALHO-EM-EVENTOS' )], 
                                            column_config=producao_evento_todos_colulm_config)

    with ori_tab:
        tipo_ori = st.radio("Tipo", 
                            options=['Todos', 'Tese', 'Dissertação', 'Especialização', 'IC', 'TCC',  'Outra'],                             
                            horizontal=True)
        print(tipo_ori)
        
        if tipo_ori == 'Tese':
            filtro_ori = 'Tese de doutorado'
        if tipo_ori == 'Dissertação':
            filtro_ori = 'Dissertação de mestrado'
        if tipo_ori == 'Especialização':
            filtro_ori = 'MONOGRAFIA_DE_CONCLUSAO_DE_CURSO_APERFEICOAMENTO_E_ESPECIALIZACAO'
        if tipo_ori == 'IC':
            filtro_ori = 'INICIACAO_CIENTIFICA'
        if tipo_ori == 'TCC':
            filtro_ori = 'TRABALHO_DE_CONCLUSAO_DE_CURSO_GRADUACAO'
        if tipo_ori == 'Outra':
            filtro_ori = 'ORIENTACAO-DE-OUTRA-NATUREZA'

        print(filtro_ori)
        
        if docente_sel != 'Todos':
            if tipo_ori == 'Todos':
                st.dataframe(orientacao.loc [ (orientacao['nome'] == docente_sel) 
                                            & (orientacao['ano'] >= int(ano_inicio_sel) )
                                            & (orientacao['ano'] <= int(ano_fim_sel) )], 
                                            column_config=orientacao_colum_config)
            else: 
                st.dataframe(orientacao.loc [ (orientacao['nome'] == docente_sel) 
                                            & (orientacao['ano'] >= int(ano_inicio_sel) )
                                            & (orientacao['ano'] <= int(ano_fim_sel)) 
                                            & (orientacao['tipo'] == filtro_ori)], 
                                            column_config=orientacao_colum_config)
        else:
            if tipo_ori == 'Todos':
                st.dataframe(orientacao.loc [ (orientacao['ano'] >= int(ano_inicio_sel) )
                                            & (orientacao['ano'] <= int(ano_fim_sel) )], 
                                            column_config=orientacao_todos_colum_config)
            else: 
                st.dataframe(orientacao.loc [ (orientacao['ano'] >= int(ano_inicio_sel) )
                                            & (orientacao['ano'] <= int(ano_fim_sel)) 
                                            & (orientacao['tipo'] == filtro_ori)], 
                                            column_config=orientacao_todos_colum_config)

    with tec_tab:
        if docente_sel != 'Todos':
            st.dataframe(tecnica.loc [ (tecnica['nome'] == docente_sel) 
                                            & (tecnica['ano'] >= int(ano_inicio_sel) )
                                            & (tecnica['ano'] <= int(ano_fim_sel) )], 
                                    column_config = tecnica_colum_config)
        else: 
            st.dataframe(tecnica.loc [ (tecnica['ano'] >= int(ano_inicio_sel) )
                                        & (tecnica['ano'] <= int(ano_fim_sel) )], 
                                    column_config = tecnica_todos_colum_config)

main()


