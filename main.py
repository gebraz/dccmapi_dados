import streamlit as st
import pandas as pd
import io
import math
from dataframe_format import *

buffer = io.BytesIO()

st.set_page_config(page_title="DCCMAPI - AutoAvaliação", layout="wide")

docente_sel = 'Alexandre César Muniz de Oliveira'
ano_inicio_sel = 2019
ano_fim_sel = 2022


@st.cache_data
def loadData():  
    docentes = pd.read_csv('docentes.csv', delimiter=';')
    producao = pd.read_csv('producao.csv', delimiter=';')
    tecnica = pd.read_csv('tecnica.csv', delimiter=';')
    orientacao = pd.read_csv('orientacao.csv', delimiter=';')
    projeto = pd.read_csv('projeto.csv', delimiter=';')
    vinculo = pd.read_csv('vinculo.csv', delimiter=';')

    return docentes, producao, tecnica, orientacao, projeto, vinculo

def main():
    docentes, producao, tecnica, orientacao, projeto, vinculo = loadData()
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
    per_tab, eve_tab, ori_tab, proj_tab, tec_tab, vinc_tab, download = st.tabs(['Periódicos', 'Eventos', 'Orientações', 'Projetos', 'Técnicas', 'Vinculos', 'Download'])
        

    with per_tab:
        st.write('Periódicos')

        if docente_sel != 'Todos':
            st.dataframe(producao.loc [ (producao['nome'] == docente_sel) 
                                        & (producao['ano'] >= int(ano_inicio_sel) )
                                        & (producao['ano'] <= int(ano_fim_sel) ) 
                                        & ((producao['tipo'] == 'ARTIGO-ACEITO-PARA-PUBLICACAO' ) 
                                        | (producao['tipo'] == 'ARTIGO-PUBLICADO' ))], 
                                column_config = producao_periodico_colulm_config)
        else:
            st.dataframe(producao.loc [(producao['ano'] >= int(ano_inicio_sel) )
                                        & (producao['ano'] <= int(ano_fim_sel) ) 
                                        & ((producao['tipo'] == 'ARTIGO-ACEITO-PARA-PUBLICACAO' ) 
                                        | (producao['tipo'] == 'ARTIGO-PUBLICADO' ))], 
                                column_config = producao_periodico_todos_colulm_config)
    
    with eve_tab:
        st.write('Eventos')

        if docente_sel != 'Todos':
            st.dataframe(producao.loc [ (producao['nome'] == docente_sel) 
                                        & (producao['ano'] >= int(ano_inicio_sel) )
                                        & (producao['ano'] <= int(ano_fim_sel) )                                         
                                        & (producao['tipo'] == 'TRABALHO-EM-EVENTOS' )], 
                                        column_config=producao_evento_colulm_config)
        else:
            st.dataframe(producao.loc [ (producao['ano'] >= int(ano_inicio_sel) )
                                        & (producao['ano'] <= int(ano_fim_sel) )                                         
                                        & (producao['tipo'] == 'TRABALHO-EM-EVENTOS' )], 
                                        column_config=producao_evento_todos_colulm_config)


    with ori_tab:
        tipo_ori = st.radio("Tipo", 
                            options=['Todos', 'Tese', 'Dissertação', 'Especialização', 'IC', 'TCC',  'Outra'],                             
                            horizontal=True)        
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

    with proj_tab:                
        
        if docente_sel != 'Todos':            
            st.dataframe(projeto.loc [ (projeto['nome'] == docente_sel) &
                                        (
                                            (projeto['ano_fim'].isnull()) 
                                            | 
                                            ((projeto['ano_fim'] >= int(ano_inicio_sel))
                                             &
                                            (projeto['ano_fim'] <= int(ano_fim_sel)))
                                        )], 
                                    column_config = projeto_colum_config)
        else: 
            st.dataframe(projeto.loc [  (projeto['ano_fim'].isnull()) 
                                            | 
                                            ((projeto['ano_fim'] >= int(ano_inicio_sel))
                                             &
                                            (projeto['ano_fim'] <= int(ano_fim_sel)))
                                    ], 
                                    column_config = projeto_todos_colum_config)

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
            
    with vinc_tab:
        tipo_vinc = st.radio("Tipo", 
                            options=['Todos', 'Revisor de periódico', 'Membro de corpo editorial', 'Membro de comitê assessor', 'Revisor de projeto de fomento'],     
                            horizontal=True)
        if tipo_vinc == 'Todos':
            if docente_sel != 'Todos':
                st.dataframe(vinculo.loc [ (vinculo['nome'] == docente_sel) 
                                                & 
                                                (
                                                    (vinculo['ano_fim'].isnull()) 
                                                    | 
                                                    ((vinculo['ano_fim'] >= int(ano_inicio_sel)) & (vinculo['ano_fim'] <= int(ano_fim_sel)))
                                                )
                                                  ], 

                                        column_config = vinculo_colum_config)
            else: 
                st.dataframe(vinculo.loc [(
                                                ((vinculo['ano_fim'].isnull()) | ((vinculo['ano_fim'] >= int(ano_inicio_sel)) & (vinculo['ano_fim'] <= int(ano_fim_sel))))
                                                )], 
                                        column_config = vinculo_todos_colum_config)
        else:
            if docente_sel != 'Todos':
                st.dataframe(vinculo.loc [ (vinculo['nome'] == docente_sel) 
                                                & ((vinculo['ano_fim'].isnull()) | ((vinculo['ano_fim'] >= int(ano_inicio_sel)) & (vinculo['ano_fim'] <= int(ano_fim_sel))))
                                                & (vinculo['tipo'] == tipo_vinc )], 
                                        column_config = vinculo_colum_config)
            else: 
                st.dataframe(vinculo.loc [ ((vinculo['ano_fim'].isnull()) | ((vinculo['ano_fim'] >= int(ano_inicio_sel)) & (vinculo['ano_fim'] <= int(ano_fim_sel))))
                                           & (vinculo['tipo'] == tipo_vinc)], 
                                        column_config = vinculo_todos_colum_config)

    with download:
        
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            if docente_sel != 'Todos':
                
                producao.loc [ (producao['nome'] == docente_sel) 
                                        & (producao['ano'] >= int(ano_inicio_sel) )
                                        & (producao['ano'] <= int(ano_fim_sel) ) 
                                        & ((producao['tipo'] == 'ARTIGO-ACEITO-PARA-PUBLICACAO' ) 
                                        | (producao['tipo'] == 'ARTIGO-PUBLICADO' ))].to_excel(writer, sheet_name='Periódicos')
            
                producao.loc [ (producao['nome'] == docente_sel) 
                                        & (producao['ano'] >= int(ano_inicio_sel) )
                                        & (producao['ano'] <= int(ano_fim_sel) )                                         
                                        & (producao['tipo'] == 'TRABALHO-EM-EVENTOS' )].to_excel(writer, sheet_name='Eventos')
            else:
                           
                producao.loc [(producao['ano'] >= int(ano_inicio_sel) )
                                        & (producao['ano'] <= int(ano_fim_sel) ) 
                                        & ((producao['tipo'] == 'ARTIGO-ACEITO-PARA-PUBLICACAO' ) 
                                        | (producao['tipo'] == 'ARTIGO-PUBLICADO' ))].to_excel(writer, sheet_name='Periódicos')
            
                producao.loc [ (producao['ano'] >= int(ano_inicio_sel) )
                                        & (producao['ano'] <= int(ano_fim_sel) )                                         
                                        & (producao['tipo'] == 'TRABALHO-EM-EVENTOS' )].to_excel(writer, sheet_name='Eventos')


            #producao.to_excel(writer, sheet_name='Produção')
            #orientacao.to_excel(writer, sheet_name='Orientação')
            if docente_sel != 'Todos':
                if tipo_ori == 'Todos':
                    orientacao.loc [ (orientacao['nome'] == docente_sel) 
                                                & (orientacao['ano'] >= int(ano_inicio_sel) )
                                                & (orientacao['ano'] <= int(ano_fim_sel) )].to_excel(writer, sheet_name='Orientação')
                else: 
                    orientacao.loc [ (orientacao['nome'] == docente_sel) 
                                                & (orientacao['ano'] >= int(ano_inicio_sel) )
                                                & (orientacao['ano'] <= int(ano_fim_sel)) 
                                                & (orientacao['tipo'] == filtro_ori)].to_excel(writer, sheet_name='Orientação')
            else:
                if tipo_ori == 'Todos':
                    orientacao.loc [ (orientacao['ano'] >= int(ano_inicio_sel) )
                                                & (orientacao['ano'] <= int(ano_fim_sel) )].to_excel(writer, sheet_name='Orientação')
                else: 
                    orientacao.loc [ (orientacao['ano'] >= int(ano_inicio_sel) )
                                                & (orientacao['ano'] <= int(ano_fim_sel)) 
                                                & (orientacao['tipo'] == filtro_ori)].to_excel(writer, sheet_name='Orientação')
                
            if docente_sel != 'Todos':            
                projeto.loc [ (projeto['nome'] == docente_sel) & 
                                            (projeto['ano_fim'].isnull()) 
                                            | 
                                            ((projeto['ano_fim'] >= int(ano_inicio_sel))
                                             &
                                            (projeto['ano_fim'] <= int(ano_fim_sel))
                              )].to_excel(writer, sheet_name='Projetos')
                                    
            else: 
                projeto.loc [  (projeto['ano_fim'].isnull()) 
                                | 
                                ((projeto['ano_fim'] >= int(ano_inicio_sel))
                                    &
                                (projeto['ano_fim'] <= int(ano_fim_sel))
                                    )].to_excel(writer, sheet_name='Projetos')
                                        
            
            #tecnica.to_excel(writer, sheet_name='Técnica')
            if docente_sel != 'Todos':
                tecnica.loc [ (tecnica['nome'] == docente_sel) 
                                                & (tecnica['ano'] >= int(ano_inicio_sel) )
                                                & (tecnica['ano'] <= int(ano_fim_sel) )].to_excel(writer, sheet_name='Técnica')
            else: 
                tecnica.loc [ (tecnica['ano'] >= int(ano_inicio_sel) )
                                            & (tecnica['ano'] <= int(ano_fim_sel) )].to_excel(writer, sheet_name='Técnica')

            if docente_sel != 'Todos':
                vinculo.loc [ (vinculo['nome'] == docente_sel) 
                                                & 
                                                (
                                                    (vinculo['ano_fim'].isnull()) 
                                                    | 
                                                    ((vinculo['ano_fim'] >= int(ano_inicio_sel)) & (vinculo['ano_fim'] <= int(ano_fim_sel)))
                                                )].to_excel(writer, sheet_name='Vínculos')
            else: 
                vinculo.loc [(((vinculo['ano_fim'].isnull()) | ((vinculo['ano_fim'] >= int(ano_inicio_sel)) & (vinculo['ano_fim'] <= int(ano_fim_sel))))
                                                )].to_excel(writer, sheet_name='Vínculos')
                                        

            # Close the Pandas Excel writer and output the Excel file to the buffer
            writer.close()

            if docente_sel != 'Todos':
                st.download_button(
                    label="Download Excel",
                    data=buffer,
                    file_name=f"dados_{docente_sel}.xlsx",
                    mime="application/vnd.ms-excel"
                )
            else:
                st.download_button(
                    label="Download Excel",
                    data=buffer,
                    file_name=f"dados.xlsx",
                    mime="application/vnd.ms-excel"
                )
main()


