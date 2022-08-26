from datetime import date
import dash
from dash import html, dcc, Input, Output
from dash import dash_table as dt
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from dash_bootstrap_templates import ThemeSwitchAIO


# ========= App ============== #
FONT_AWESOME = ["https://use.fontawesome.com/releases/v5.10.2/css/all.css"]
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.4/dbc.min.css"

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY, dbc_css])
app.scripts.config.serve_locally = True
server = app.server

# ========== Estilos ============ #

template_theme1 = "flatly"
template_theme2 = 'vapor'
url_theme1 = dbc.themes.FLATLY
url_theme2 = dbc.themes.VAPOR
tab_card = {'height':'100%'}
text_style = {'width': '100%', 'display': 'flex', 'align-items':'center', 'justify-content':'center'}


# ===== Tratamento dos dados ====== #
df = pd.read_excel('Controle de Documentos.xlsx', sheet_name='CONTROLE DE DOCUMENTOS',header=0)
df.drop([0],axis=0, inplace=True)
df.drop(['Unnamed: 0','Unnamed: 1'],axis=1, inplace=True)
df.rename(columns=df.iloc[0], inplace=True)
df.drop([1],axis=0, inplace=True)
df.fillna(0, inplace=True)
df['PRAZO DE RESPOSTA CONTRATUAL'] = pd.to_datetime(df['PRAZO DE RESPOSTA CONTRATUAL'])
df['DATA DE RECEBIMENTO PARA ANÁLISE'] = pd.to_datetime(df['DATA DE RECEBIMENTO PARA ANÁLISE'])
df.drop(df.columns[len(df.columns)-1], axis=1, inplace=True)
df['CONTROLE'] = 1

df_rev = pd.DataFrame(df.value_counts(['REV'])).reset_index()
df_rev.columns = ['REV','QTDE']

df_status = pd.DataFrame(df.value_counts(df.iloc[:,15])).reset_index()
df_status.columns = ['STATUS', 'QTDE']

df_store = df.to_dict()
df_store_rev = df_rev.to_dict()
df_store_status = df_status.to_dict()


#df para tabela
df_tabela = df.copy()
df_tabela.drop(df_tabela.columns[[4,6,7,9,10,11,12,13,14,16,17,18,19,20]],axis=1, inplace=True)
df_tabela.columns = df_tabela.columns.str.replace('PRAZO DE RESPOSTA CONTRATUAL','PRAZO_DE_RESPOSTA')
df_tabela['PRAZO_DE_RESPOSTA'] = df_tabela['PRAZO_DE_RESPOSTA'].dt.strftime("%d-%m-%Y")

df_atrasado = df_tabela[df_tabela['AÇÃO'] == 'Atrasado']
df_em_alerta = df_tabela[df_tabela['AÇÃO'] == 'Em alerta']
df_no_prazo = df_tabela[df_tabela['AÇÃO'] == 'No prazo']

df_filtro = pd.concat([df_atrasado,df_em_alerta,df_no_prazo])
df_filtro.sort_values(by=['SISTEMA'])
df_filtro.drop(df_filtro.columns[[7,8,9]],axis=1, inplace=True)



#Estilos
main_config = {
    'hovermode':'x unified',
    'legend':{'yanchor':'top',
            'y':0.9,
            'xanchor':'left',
            'x':0.1,
            'title':{'text':None},
            'font':{'color':'white'},
            'bgcolor':'rgba(0,0,0,0.5)'},
    'margin':{'l':0, 'r':0, 't':10, 'b':0}
}

# =========  Layout  =========== #
app.layout = dbc.Container(children=[
    dcc.Store(id='dataset', data=df_store),
    dcc.Store(id='datasetrev', data=df_store_rev),
    dcc.Store(id='datasetstatus', data=df_store_status),


# ======= Linha 1 ==============#
    dbc.Row([
#Filtro e links# 
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.H4('Controle de documentos'),
                            dbc.Button('By Tractebel',
                            href='https://www.linkedin.com/in/j%C3%BAlio-casagrande/', target='blank', color='transparent',size='sm')
                        ], sm=8),
                        dbc.Col([
                            html.I(className='fa fa-filter', style={'font-size':'300%'})
                        ], sm=4, align='center')
                    ]),
                    
                    dbc.Row([
                        dbc.Col([
                            ThemeSwitchAIO(aio_id='theme', themes=[url_theme1, url_theme2])
                        ])
                    ], style={'margin-top':'10px'}),

                    dbc.Row([
                        dbc.Col([
                            dbc.Button('Acesso ao Colaborativo',
                            href='https://servidor2.colaborativo.com/', target='blank',size='sm')
                        ]),
                    ], style={'margin-top':'10px'})
                ])
            ], style=tab_card)
        ], sm=4, lg=3),
#Dias de análise#
#        dbc.Col([
#            dbc.Card([
#                dbc.CardBody([
#                    dbc.Row([
#                        html.H4('Média de dias para análise dos documentos')
#                    ]),
 #               
  #                  dbc.Row([
   #                     dbc.Col([
    #                        html.H5(['',dbc.Badge('SPIC',color='danger')], style=text_style)
     #                   ]),
      #                  dbc.Col([
       #                     html.H5(['',dbc.Badge('TRACTEBEL',color='info')], style=text_style)
        #                ]),
         #               dbc.Col([
          #                  html.H5(['',dbc.Badge('CMSS',color='secondary')], style=text_style)
           #             ])
            #        ], style={'margin-top':'15px'}),

 #                   dbc.Row([
  #                      dbc.Col([
   #                         html.H3(children=['2'], style=text_style)
    #                    ]),
     #                   dbc.Col([
      #                      html.H3(children=['10'], style=text_style)
       #                 ]),
        #                dbc.Col([
         #                   html.H3(children=['15'], style=text_style)
          #              ])
           #         ]),
            #        dbc.Row([
             #           dbc.Col([
              #              html.H6(children=['DIAS'], style=text_style)
               #         ]),
                #        dbc.Col([
                 #           html.H6(children=['DIAS'], style=text_style)
    #                    ]),
     #                   dbc.Col([
      #                      html.H6(children=['DIAS'], style=text_style)
       #                 ])
        #            ])
         #       ])
    #        ])
     #   ],sm=8, md=2, lg=2),
#Graficos revisoes#
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                        html.H4('Documentos por REVISÃO'),
                        dcc.Graph(id='grafico-rev', config={'displayModeBar':False, 'showTips':False})
                        ]),
                    ],align='center')
                ])
            ])
        ],sm=8, lg=9),
#        dbc.Col([
#            dbc.Card([
 #               dbc.CardBody([
  #                  dbc.Row([
   #                     dbc.Col([
    #                        daq.Gauge(
     #                           color={"gradient":True,"ranges":{"red":[-0.2,0.0],"yellow":[0.0,0.3],"green":[0.3,1]}},
      #                          value=df['DIAS ATÉ O PRAZO'].sum()/df['PRAZO DE ANÁLISE'].sum(),
       #                         size=152,
        #                        max=1,
         #                       min=-0.2,
          #                      style={'margin-right':'0'}
           #                 )
            #            ],className='m-auto')
             #       ])
              #  ],className='d-flex')
     #       ])
      #  ],sm=12, md=2 ,lg=2)
     ], className='g-2 my-auto'),

# ======= Linha 2 ==============#
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.H6('SELEÇÃO DE DATA'),#with_full_screen_portal, with_portal
                            dcc.DatePickerRange(id='escolhe-data',
                            min_date_allowed=df['PRAZO DE RESPOSTA CONTRATUAL'].min(),
                            max_date_allowed=df['PRAZO DE RESPOSTA CONTRATUAL'].max(),
                            initial_visible_month=date.today(),
                            start_date=date(2022,8,1),
                            end_date=df['PRAZO DE RESPOSTA CONTRATUAL'].max(),
                            day_size=40,
                            display_format='DD/MM/YY'),
                            html.H3(''),
                            html.H6('SELEÇÃO DOS SISTEMAS',style={'margin-top':'7px'}),
                            
                            dcc.Checklist(id='select-sistema',
                                options=[
                                {'label':x, 'value':x} for x in df.SISTEMA.unique()
                            ],value=['GERADOR','SDSC','TURBINA'],labelStyle={'display': 'block','cursor': 'pointer', 'margin-right':'7px'}
                            ),
                        ],lg=3),
                        dbc.Col([
                            html.H5('Prazos contratuais para entrega dos documentos'),
                            dcc.Graph(id='grafico-docs', config={'displayModeBar':False, 'showTips':False})
                        ],lg=6),
                        dbc.Col([
                            html.H6('STATUS DOS DOCUMENTOS'),
                            dcc.Graph(id='grafico-pizza', config={'displayModeBar':False, 'showTips':False})
                        ],lg=3)
                    ]),
                ])
            ])
        ]),              
    ], className='g-2 my-auto'),

# ======= Linha 3 ==============#
    dbc.Row([
        #dbc.Card([
            #dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        dt.DataTable(
                            df_filtro.to_dict('records'),
                            [{"name": i, "id": i} for i in df_filtro.columns],
                            style_cell_conditional=[
                                                {
                                                'if': {'column_id': ['DESCRIÇÃO','SISTEMA']},
                                                'textAlign': 'left'
                                                },
                                                {
                                                'if': {'column_id': 'DESCRIÇÃO'},
                                                'width': '130px'
                                                }
                            ], fixed_rows={'headers': True}, style_table={'height': 300},
                            style_header={
                                'backgroundColor': 'transparent',
                                'color': 'dark-gray'
                            },
                            style_data={
                                'backgroundColor': 'transparent',
                                'color': 'dark-gray'
                            }, 
                        )
                    ])
                ])
            #])
        #])
    ]#className='g-2 my-auto'
    )

# ======= Linha 4 ==============#

# ======= Linha 5 ==============#

#FINAL DO LAYOUT#
],fluid=True)
# ======== Callbacks ========== #

#Gráfico de revisões
@app.callback(
    Output('grafico-rev','figure'),
    [Input('datasetrev','data'),
    Input(ThemeSwitchAIO.ids.switch('theme'),'value')]
)

def render(data,toogle):
    template = template_theme1 if toogle else template_theme2

    dff = pd.DataFrame(data)
    fig = px.bar(dff, y=dff['REV'], x=dff['QTDE'], template=template, orientation='h',opacity=0.8, labels={'REV':'Revisão','QTDE':'Quantidade'} )
    fig.update_layout(main_config, template=template, height=150)

    return fig

#Gráfico de prazos
@app.callback(
    Output('grafico-docs','figure'),
    [Input('dataset','data'),
    Input('escolhe-data','start_date'),
    Input('escolhe-data','end_date'),
    Input('select-sistema','value'),
    Input(ThemeSwitchAIO.ids.switch('theme'),'value')]
)

def render(data,inicio,final,sistema,toogle):
    template = template_theme1 if toogle else template_theme2

    df = pd.DataFrame(data)

    df_filtered = df.SISTEMA.isin(sistema)

    fig = px.bar(df[df_filtered], y='CONTROLE', x='PRAZO DE RESPOSTA CONTRATUAL', range_x=[inicio,final], color='AÇÃO',
    color_discrete_map={'Ok':'gray','-':'brown','Atrasado':'red', 'Em alerta':'yellow', 'No prazo':'green'},
    labels={'CONTROLE':'Quantidade de docs','PRAZO DE RESPOSTA CONTRATUAL':'Prazo para resposta'}, template=template, opacity=0.8)
    fig.update_layout(main_config,template=template,height=350)

    return fig

#Gráfico de pizza
@app.callback(
    Output('grafico-pizza','figure'),
    [Input('dataset','data'),
    Input('select-sistema','value'),
    Input(ThemeSwitchAIO.ids.switch('theme'),'value')]
)

def pizza(data,sistema,toogle):
     template = template_theme1 if toogle else template_theme2

     df = pd.DataFrame(data)

     df_filtered = df.SISTEMA.isin(sistema)

     fig = px.pie(df[df_filtered], values='CONTROLE', names='AÇÃO', height=330, labels={'CONTROLE':'QUANTIDADE DE DOCUMENTOS NO TOTAL'})
     fig.update_layout(template=template)

     return fig

# Run server
#if __name__ == '__main__':
#    app.run_server(debug=False,port=8080)
if __name__ == '__main__':
    app.run_server(debug=False,port=8080)
