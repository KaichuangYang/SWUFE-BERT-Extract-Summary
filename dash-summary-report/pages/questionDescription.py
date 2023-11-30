import dash_html_components as html
import dash_bootstrap_components as dbc
from utils import Header

left_jumbotron = dbc.Col(
    html.Div(
        [
            html.H2("Change the background", className="display-3"),
            html.Hr(className="my-2"),
            html.P(
                "Swap the background-color utility and add a `.text-*` color "
                "utility to mix up the look."
            ),
            dbc.Button("Example Button", color="light", outline=True),
        ],
        className="h-100 p-5 text-white bg-dark rounded-3",
    ),
    md=6,
)

right_jumbotron = dbc.Col(
    html.Div(
        [
            html.H2("Add borders", className="display-3"),
            html.Hr(className="my-2"),
            html.P(
                "Or, keep it light and add a border for some added definition "
                "to the boundaries of your content."
            ),
            dbc.Button("Example Button", color="secondary", outline=True),
        ],
        className="h-100 p-5 bg-light border rounded-3",
    ),
    md=6,
)



def create_layout(app):
    return html.Div(
        [
            Header(app),
            # page 4
            html.Div(
                [
                    # Row 1
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6([html.Strong("问题重述")],className="subtitle padded"),
                                    html.Br([]),
                                    html.Div(
                                        [
                                           
                                            html.Div(
                                                [   html.Br([]),
                                                    html.P(
                                                        [
                                                            "面对呈指数级增长的网络文本资源，如何快速且准确地从中提取出重要的内容，是一个迫切而有意义的需求。\
                                                                自动文本摘要技术旨在利用计算机强大的计算能力，从较长文本中提炼出关键信息，生成简洁、通顺和凝练的摘要，\
                                                                    以帮助用户快速全面地了解文本关键信息。由于不同学科领域词语表达、组合各有特色，现有预训练BERT模型在不同领域任务中表现也不尽相同。聚焦于财经领域，\
                                                                        在当前数字金融蓬勃兴起的背景下，非结构化的文本数据在舆情预测、金融风控等领域发挥了独特的作用。"
                                                        ],
                                                        className="minipara" 
                                                    )
                                                ],
                                            ),
                                            html.Div(
                                                [   html.Br([]),
                                                    html.P(
                                                        [
                                                            "BERT 是由 Google 在 2018 年开发的大型自然语言处理模型，拥有强大的语言表征能力和特征提取能力。目前开源的 BERT 模型大多适用于通用语言领域，\
                                                                在金融文本的分支赛道上少有建树。现有的开源金融 BERT 模型存在使用的语料库较小、文本来源较乱、在金融场景中广泛应用存在局限性等问题。"
                                                        ],
                                                        className="minipara" 
                                                    ),                                                    
                                                ],
                                            ),
                                        ],
                                        className="row",
                                    )
                                    
                                ],
                                className="twelve columns",
                            )
                        ],
                        className="row",
                    ),
                    html.Br([]),
                    # Row 3
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.Strong(
                                                        ["CN_BERT"],
                                                        style={
                                                            "color": "#ffffff",
                                                            "padding-left":"135px",
                                                        },
                                                    ),
                                                    html.Br([])
                                                ],
                                                className="six columns",
                                                style={
                                                    "padding-top": "20px",
                                                    "padding-left":"20px",
                                                },
                                            ),
                                            html.Div(
                                                [
                                                    html.Strong(
                                                        ["WWM_BERT"],
                                                        style={
                                                            "color": "#ffffff",
                                                            "padding-left":"140px",
                                                            "padding-right":"10px"
                                                        },
                                                    )
                                                ],
                                                className="six columns",
                                                style={
                                                    "padding-top": "20px",
                                                    "padding-right":"20px",
                                                },
                                            ),
                                            html.Div(
                                                [
                                                    html.P(
                                                        ["谷歌官方发布的BERT-base，Chinese，以每种语言的整个Wikipedia转储数据作为每种语言的训练数据。该模型使用的WordPiece的分词\
                                                            方式会把一个完整的词切分成若干个子词，在生成训练样本时，这些被分开的子词会随机被mask。这种分词方式没有考虑到传统NLP中的中文分词。"],
                                                        className="minipara" ,
                                                        style={
                                                            "color": "#ffffff"
                                                        }
                                                    )
                                                ],
                                                className="six columns",
                                                style={
                                                    "padding-top": "20px",
                                                    "padding-left":"20px",
                                                },
                                            ),
                                            html.Div(
                                                [
                                                    html.P(
                                                        ["wwm-bert使用中文维基百科（包括简体和繁体）进行训练，并且使用了哈工大LTP作为分词工具，即对组成同一个词的汉字全部进行Mask，是谷歌在2019年5月31日发布的\
                                                            一项BERT的升级版本，主要更改了原预训练阶段的训练样本生成策略。在全词Mask中，如果一个完整的词的部分WordPiece字词被mask，则同属该词的其他部分也会被mask。"],
                                                        className="minipara" ,
                                                        style={
                                                            "color": "#ffffff"
                                                        }
                                                    )
                                                ],
                                                className="six columns",
                                                style={
                                                    "padding-top": "20px",
                                                    "padding-left":"50px",
                                                },
                                            ),
                                        ],
                                        className="row",
                                        style={
                                             "background-color": "#98151b",
                                        },
                                    ),  
                                    html.Div(
                                        [   
                                            html.Br([]),
                                            html.Br([]),
                                            html.P(
                                                [
                                                    "目前金融领域对文本数据的处理还缺乏成熟的技术工具，因此我们基于包含1500万条金融新闻和机构研报的超过200G语料库的大型金融语言模型SWUFE-BERT，\
                                                        进行抽取式新闻摘要任务的 Fine-Tuning，期望对于金融文本处理的分支赛道上有更好的表现。"
                                                ],
                                                className="minipara" 
                                            ),                                                    
                                            html.Br([])
                                        ],
                                    ),                                           
                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.Br([]),
                                                    html.Br([]),
                                                    html.Br([]),
                                                    html.Strong(
                                                        ["SWUFE_BERT"],
                                                        style={
                                                            "color": "#ffffff"
                                                        },
                                                    )
                                                ],
                                                className="two columns right-aligned",
                                            ),
                                            html.Div(
                                                [
                                                    html.Br([]),
                                                    html.P(
                                                        ["金融领域大型通用语言模型SWUFE-BERT，在包含1500万条金融新闻和机构研报的超过200G语料库中进行预训练，采用Transformer模型构架与Whole Word Mask中文分词掩码技术。与现有BERT模型在通用语料库中训练不同，SWUFE-BERT通过在大量高质量财经语料库中训练，且结合Whole Word Mask中文分词掩码技术，使其吸收了WWM-BERT的优势同时也弥补了其他现有BERT模型在财经领域的不足。"],
                                                        className="minipara" ,
                                                        style={
                                                            "color": "#ffffff"
                                                        }
                                                    )
                                                ],
                                                className="ten columns",
                                            ),
                                        ],
                                        className="row",
                                        style={"background-color": "#98151b"},
                                    ), 
                                ],
                                className="twelve columns",
                            )
                        ],
                        className="row",
                    ),
                ],
                className="sub_page",
            ),
        ],
        className="page",
    )
