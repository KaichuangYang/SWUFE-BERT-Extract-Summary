from dash import dcc,html
from utils import Header


def create_layout(app):
    return html.Div(
        [
            Header(app),
            # page 6
            html.Div(
                [
                    # Row 1
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(html.Strong("Transformer Encoder"), className="subtitle padded"),
                                    html.Br(),
                                    html.Div(
                                        [
                                            html.P(
                                                "Transformer模型抛弃了传统的CNN和RNN，只使用注意力机制，以其优秀的表现成为机器学习领域热点，而翻译任务与摘要任务极为相似，我们有理由相信Transformer在文本摘要任务中也一定能够持续稳定输出。不同于论文中Transformer 使用6层encoder-decoder结构，在本次实训中经过多方面考量，我们采用至多2层encoder，由于本阶段不涉及decoder，所以我们不设置decoder。且本次实训直接提供了输入向量，所以不涉及embedding的部分。我们选取vrelu函数作为激活函数，对输出先使用Tanh函数处理，再使用Sigmoid函数得到介于0,1之间的概率值，如图为我们采用的Transformer模型结构图。",
                                            ),
                                        ],
                                        className='red-author1',
                                        style = {"line-height":"250%"}
                                    ),
                                ],
                                className="row",
                            ),
                    html.Br(),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Img(src='/assets/Transformer_Encoder.png',className="TransformerEncoder")
                                ],
                                className='four columns'#网页1行12列
                                
                            ),
                            html.Div(
                                [
                                    html.Img(src='/assets/Multi_Head.png',className="MultiHead",)
                                ],
                                className='eight columns'
                            ),
                        ],
                        className="row ",
                        style={
                            "padding-bottom": "2px",
                            'textAlign':'center'
                        },
                    ),
                    html.Div(
                        [
                            html.H6(html.Strong("Muti-Head Attention"), className="subtitle padded"),
                            html.Br(),
                            html.Div(
                                [
                                    html.P("Transformer的注意力机制与人类的注意力机制相似，由于注意力有限，它将注意力资源更多的投入到目标区域，使用多头注意力机制（本次实训使用4头）从不同方面提取v特征。上右图是注意力机制的图解。"),
                                    html.P(
                                        "单个注意力机制用数学公式可以简单表达为（其中softmax除以根号下Q，K点乘的方差dk是为了防止梯度消失）："
                                    ),
                                ],
                                className='red-author1',
                                id="multi-bullet-pts",
                                style = {"line-height":"250%"},
                                ),
                            html.Br(),
                            html.Div(
                                [
                                     html.Img(
                                        src="/assets/AttentionSoftmax.png",className='AttenSoftmax'
                                    ),   
                                ],
                                 style={
                                            "background-color": "#f0e8e8",
                                            "padding-bottom": "5px",
                                            'textAlign':'center'
                                        },
                                ),
                        ],
                        className="row",
                    ),
                    html.Br(),
                    html.Div(
                        [
                            html.H6(html.Strong("Positional Encoding"), className="subtitle padded"),
                            html.Br(),
                            html.Div(
                                [
                                    html.P("没有采用RNN的Transformer没有捕捉序列信息的功能，它不能分清到底是“我很开心”还是“开心很我”，所以在输入词向量后还需要进行Positional Encoding，位置编码公式如下："),
                                ],
                                style = {"line-height":"250%"},
                                className='red-author1',
                                id="posi1-bullet-pts",
                                ),
                            html.Br(),
                            html.Div(
                                [
                                    html.Img(
                                        src="/assets/positionalencoding1.png", className='PosEnco'
                                    ),
                                    html.Br(),
                                    html.Img(
                                        src="/assets/positionalencoding2.png", className='PosEnco'
                                    ),      
                                ],
                                style={
                                            "background-color": "#f0e8e8",
                                            "padding-bottom": "5px",
                                            'textAlign':'center'
                                        },
                                ),
                             html.Div(
                                [
                                    html.P("其中pos代表目前token在序列的位置，dmodel代表模型的维度也就是inputsize。",
                                    className='minipara',
                                    style = {"line-height":"250%"}
                                    ),
                                ],
                                 style={
                                            "background-color": "#f0e8e8",
                                            "padding-bottom": "5px",
                                            'textAlign':'center'
                                        },
                                id="posi2-bullet-pts",
                                ),
                        ],
                        className="row",
                    ),
                        ],
                        className="row ",
                    ),
                ],
                className="sub_page",
            ),
        ],
        className="page",
    )