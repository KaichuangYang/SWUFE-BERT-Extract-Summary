# -*- coding: utf-8 -*-
import dash
from dash import dcc,html,callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output ,State
from news_to_summary import NewsToSummary
import plotly.graph_objs as go
from utils import get_data_loss_weighted, get_data_bert, get_data_network, process_dil_file, data2fig,bar_compare_auc,bar_compare_loss
from pages import (
    first_page,
    eighth_page_summary,
    nine_page,
    tenth_page_2,
    plot_test_page,
    firstlstm,
    measures,
    questionDescription,
    transformer_model,
    
)
app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"},]
)
app.title = "Summary Report"
server = app.server
 
df =  process_dil_file() 
# Describe the layout/ UI of the app
page_layout = html.Div(
    [dcc.Location(id="url"), html.Div(id="page-content")]
)

app.layout = page_layout
app.validation_layout = html.Div([
    page_layout,
    tenth_page_2.create_layout(app),
    plot_test_page.create_layout(app),
    plot_test_page.create_full_view_layout(app),
    plot_test_page.return_bert_compare(),
    plot_test_page.return_loss_function_compare(),
    plot_test_page.return_network_compare(),
    plot_test_page.return_compare(),
])
# Update page
@callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/dash-summary-report/price-performance":
        return first_page.create_layout(app)
    elif pathname == "/dash-summary-report/summary-display":
         return eighth_page_summary.create_layout(app)
    elif pathname == "/dash-summary-report/question-improvement":
         return nine_page.create_layout(app)
    elif pathname == "/dash-summary-report/extract-summary":
         return tenth_page_2.create_layout(app)
    elif pathname == "/dash-summary-report/plot-display":
         return plot_test_page.create_layout(app)
    elif pathname == "/dash-summary-report/plot-display/page-4":
         return plot_test_page.create_layout(app)
    elif pathname == "/dash-summary-report/plot-display/page-1":
         return plot_test_page.create_layout(app)
    elif pathname == "/dash-summary-report/plot-display/page-2":
         return plot_test_page.create_layout(app)
    elif pathname == "/dash-summary-report/plot-display/page-3":
        return plot_test_page.create_layout(app)
    elif pathname == "/dash-summary-report/lstm-model":
        return firstlstm.create_layout(app)
    elif pathname == "/dash-summary-report/measures":
        return measures.create_layout(app)
    elif pathname == "/dash-summary-report/question-description":
        return questionDescription.create_layout(app)
    elif pathname == "/dash-summary-report/transfomer-model":
        return transformer_model.create_layout(app)
    elif pathname == "/dash-summary-report/full-view":
        return (
            first_page.create_layout(app),
            questionDescription.create_layout(app),
            firstlstm.create_layout(app),
            transformer_model.create_layout(app),
            measures.create_layout(app),
            plot_test_page.create_full_view_layout(app),
            eighth_page_summary.create_layout(app),
            nine_page.create_layout(app),
            tenth_page_2.create_layout(app),
            )
    else:
        return first_page.create_layout(app)

@callback(
    Output("summary-accordion", "children"),
    Input("button-run", "n_clicks"),
    State("which-bert", "value"),
    State("which-network", "value"),
    State("which-loss", "value"),
    State("original-text", "value"),
)
def summarize(n_clicks, bert, network, loss, original_text):
    output = []
    if original_text is None or original_text == "" or bert is None or network is None or loss is None :
        return [dbc.AccordionItem([html.Div(["Did not run"])])]
    text = original_text
    for n in network:
        for l in loss:
            for b in bert:
                N = "LSTM"if n=="lstm1" else "Transformer"
                B = "SWUFE bert" if b=="swufe_bert" else "CN bert"
                B = "WWM bert" if b=="wwm_bert" else "CN bert"
                L = "Weighted" if l else "Unweighted"
                lo = "w_BCEloss" if l else "BCEloss"
                color_dict = {"bg":"#97151c","ft":"white"} if b=="swufe_bert" else {"ft":"#97151c","bg":"white"}
                color_dict = {"bg":"#97151c","ft":"white"} if b=="wwm_bert" else {"ft":"#97151c","bg":"white"}
                news_to_summary = NewsToSummary(network=n,bert=b,loss=lo,
                            text=text)
                news_to_summary.summary_modified[0]
                item = dbc.AccordionItem(
                        [
                            html.P(news_to_summary.summary_modified[0],style={"color":color_dict['ft']}),
                        ],
                        title=f'{B}-{N}-{L}-summary:',
                        style={"background":color_dict['bg']}
                    )   
                output.append(item)
    return output


@callback(Output("plot-page-content", "children"), [Input("plot-url", "pathname")])
def render_page_content(pathname):
    if pathname == "/dash-summary-report/plot-display":
        return plot_test_page.return_plot_homepage()
    elif pathname == "/dash-summary-report/plot-display/page-1":
        return plot_test_page.return_network_compare()
    elif pathname == "/dash-summary-report/plot-display/page-2":
        return plot_test_page.return_loss_function_compare()
    elif pathname == "/dash-summary-report/plot-display/page-3":
        return plot_test_page.return_bert_compare()
    elif pathname == "/dash-summary-report/plot-display/page-4":
        return plot_test_page.return_compare()
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )

        
@callback(
    Output("graph-loss-n", "figure"),
    Output("graph-auc-n", "figure"),
    Input("which-bert-n", "value"),
    Input("which-loss-n", "value"),
    Input("which-network-n", "value"),
    )
def update_graph_1(bertn,lossn,networkn):
    print("in...")
    datasets = get_data_network(df,'loss',networkn,bertn,lossn)
    fig_loss = data2fig(datasets)
    datasets = get_data_network(df,'auc_score',networkn,bertn,lossn)
    fig_auc = data2fig(datasets)
    return fig_loss,fig_auc


@callback(
    Output("graph-loss-l", "figure"),
    Output("graph-auc-l", "figure"),
    Input("which-bert-l", "value"),
    Input("which-loss-l", "value"),
    Input("which-network-l", "value"),
    )
def update_graph_2(bertl,lossl,networkl):
    print("in...")
    datasets = get_data_loss_weighted(df,'loss',networkl,bertl,lossl)
    fig_loss = data2fig(datasets)
    datasets = get_data_loss_weighted(df,'auc_score',networkl,bertl,lossl)
    fig_auc = data2fig(datasets)  
    return fig_loss,fig_auc


@callback(
    Output("graph-loss-b", "figure"),
    Output("graph-auc-b", "figure"),
    Input("which-bert-b", "value"),
    Input("which-loss-b", "value"),
    Input("which-network-b", "value"),
    )
def update_graph_3(bertn,lossn,networkn):
    print("in...")
    datasets = get_data_bert(df,'loss',networkn,bertn,lossn)
    fig_loss = data2fig(datasets)
    datasets = get_data_bert(df,'auc_score',networkn,bertn,lossn)
    fig_auc = data2fig(datasets)
    return fig_loss,fig_auc        

@callback(
    Output("graph_compare_loss", "figure"),
    Output("graph_compare_auc", "figure"),
    Input("which-bert-bar", "value"),
    )
def update_graph_4(option):
    datasets_cn_loss = get_data_network(df,'loss',['lstm1','transformer1'],'cn_bert',False)
    datasets_wwm_loss = get_data_network(df,'loss',['lstm1','transformer1'],'wwm_bert',False)
    datasets_swufe_loss = get_data_network(df,'loss',['lstm1','transformer1'],'swufe_bert',False)
    fig_loss = bar_compare_loss(datasets_cn_loss,datasets_wwm_loss,datasets_swufe_loss,option)
    
    datasets_cn_auc = get_data_network(df,'auc_score',['lstm1','transformer1'],'cn_bert',False)
    datasets_wwm_auc = get_data_network(df,'auc_score',['lstm1','transformer1'],'wwm_bert',False)
    datasets_swufe_auc = get_data_network(df,'auc_score',['lstm1','transformer1'],'swufe_bert',False)
    fig_auc = bar_compare_auc(datasets_cn_auc,datasets_wwm_auc,datasets_swufe_auc,option)
    
    return fig_loss,fig_auc


@callback(
    Output("p1", "children"),
    Output("p2", "children"),
    Output("p3", "children"),
    Output("p4", "children"),
    Output("p5", "children"),
    Input("full-view-url", "pathname"))
def full_plot_content(pathname):
    if pathname == "/dash-summary-report/full-view":
        return (plot_test_page.return_plot_homepage(),
        plot_test_page.return_compare(),
        plot_test_page.return_network_compare(),
        plot_test_page.return_loss_function_compare(),
        plot_test_page.return_bert_compare(),)




if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=8666, debug=True)
