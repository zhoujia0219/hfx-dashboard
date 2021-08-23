base_html_string2 = """
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>Target Material Design Bootstrap Admin Template</title>
    
    <link rel="stylesheet" href="assets/1materialize.min.css" media="screen,projection"/>
    
    <!-- Bootstrap Styles-->
    <link href="assets/2bootstrap.css" rel="stylesheet"/>
    <!-- FontAwesome Styles-->
    <link href="assets/3font-awesome.css" rel="stylesheet"/>
    <!-- Morris Chart Styles-->
    <link href="assets/4morris-0.4.3.min.css" rel="stylesheet"/>
    <!-- Custom Styles-->
    <link href="assets/5custom-styles.css" rel="stylesheet"/>
    <!-- Google Fonts-->
    <link href='http://fonts.googleapis.com/css?family=Open+Sans' rel='stylesheet' type='text/css'/>
    <link rel="stylesheet" href="assets/6cssCharts.css">
    {%favicon%}

    
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
        {%css%}
</head>

<body>
<div id="wrapper">
    <nav class="navbar-dash navbar-default-dash top-navbar-dash" role="navigation">
        <div class="navbar-header-dash">
            <button type="button" class="navbar-toggle waves-effect waves-dark" data-toggle="collapse"
                    data-target=".sidebar-collapse">
                <span class="sr-only">Toggle navigation</span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
            </button>
            <a class="navbar-brand waves-effect waves-dark" href="index.html"><i class="large material-icons">track_changes</i>
                <strong>RUIPOS</strong></a>

            <div id="sideNav" href=""><i class="material-icons dp48">toc</i></div>
        </div>

        <ul class="nav-dash navbar-top-links navbar-right">
            <li><a class="dropdown-button waves-effect waves-dark" href="#!" data-activates="dropdown4"><i
                    class="fa fa-envelope fa-fw"></i> <i class="material-icons right">arrow_drop_down</i></a></li>
            <li><a class="dropdown-button waves-effect waves-dark" href="#!" data-activates="dropdown3"><i
                    class="fa fa-tasks fa-fw"></i> <i class="material-icons right">arrow_drop_down</i></a></li>
            <li><a class="dropdown-button waves-effect waves-dark" href="#!" data-activates="dropdown2"><i
                    class="fa fa-bell fa-fw"></i> <i class="material-icons right">arrow_drop_down</i></a></li>
            <li><a class="dropdown-button waves-effect waves-dark" href="#!" data-activates="dropdown1"><i
                    class="fa fa-user fa-fw"></i> <b>江广锋</b> <i
                    class="material-icons right">arrow_drop_down</i></a></li>
        </ul>
    </nav>
    <!-- Dropdown Structure -->
    <ul id="dropdown1" class="dropdown-content">
        <li><a href="#"><i class="fa fa-user fa-fw"></i> 个人信息</a>
        </li>
        <li><a href="#"><i class="fa fa-gear fa-fw"></i> 设置</a>
        </li>
        <li><a href="#"><i class="fa fa-sign-out fa-fw"></i> 注销</a>
        </li>
    </ul>
    <ul id="dropdown2" class="dropdown-content w250">
        <li>
            <div>
                <i class="fa fa-comment fa-fw"></i> 新消息
                <span class="pull-right text-muted small">4 min</span>
            </div>
            </a>
        </li>
        <li class="divider"></li>
        <li>
            <div>
                <i class="fa fa-twitter fa-fw"></i> 3 新消息
                <span class="pull-right text-muted small">12 min</span>
            </div>
            </a>
        </li>
        <li class="divider"></li>
        <li>
            <div>
                <i class="fa fa-envelope fa-fw"></i>消息中心
                <span class="pull-right text-muted small">4 min</span>
            </div>
            </a>
        </li>
        <li class="divider"></li>
        <li>
            <div>
                <i class="fa fa-tasks fa-fw"></i> 新的会话
                <span class="pull-right text-muted small">4 min</span>
            </div>
            </a>
        </li>
        <li class="divider"></li>
        <li>
            <div>
                <i class="fa fa-upload fa-fw"></i> 重新加载
                <span class="pull-right text-muted small">4 min</span>
            </div>
            </a>
        </li>
        <li class="divider"></li>
        <li>
            <a class="text-center" href="#">
                <strong>查看更多</strong>
                <i class="fa fa-angle-right"></i>
            </a>
        </li>
    </ul>
    <ul id="dropdown3" class="dropdown-content dropdown-tasks w250">
        <li>
            <a href="#">
                <div>
                    <p>
                        <strong>任务 1</strong>
                        <span class="pull-right text-muted">60% Complete</span>
                    </p>
                    <div class="progress progress-striped active">
                        <div class="progress-bar progress-bar-success" role="progressbar" aria-valuenow="60"
                             aria-valuemin="0" aria-valuemax="100" style="width: 60%">
                            <span class="sr-only">60% Complete (success)</span>
                        </div>
                    </div>
                </div>
            </a>
        </li>
        <li class="divider"></li>
        <li>
            <a href="#">
                <div>
                    <p>
                        <strong>任务 2</strong>
                        <span class="pull-right text-muted">28% Complete</span>
                    </p>
                    <div class="progress progress-striped active">
                        <div class="progress-bar progress-bar-info" role="progressbar" aria-valuenow="28"
                             aria-valuemin="0" aria-valuemax="100" style="width: 28%">
                            <span class="sr-only">28% Complete</span>
                        </div>
                    </div>
                </div>
            </a>
        </li>
        <li class="divider"></li>
        <li>
            <a href="#">
                <div>
                    <p>
                        <strong>任务 3</strong>
                        <span class="pull-right text-muted">60% Complete</span>
                    </p>
                    <div class="progress progress-striped active">
                        <div class="progress-bar progress-bar-warning" role="progressbar" aria-valuenow="60"
                             aria-valuemin="0" aria-valuemax="100" style="width: 60%">
                            <span class="sr-only">60% Complete (warning)</span>
                        </div>
                    </div>
                </div>
            </a>
        </li>
        <li class="divider"></li>
        <li>
            <a href="#">
                <div>
                    <p>
                        <strong>任务 4</strong>
                        <span class="pull-right text-muted">85% Complete</span>
                    </p>
                    <div class="progress progress-striped active">
                        <div class="progress-bar progress-bar-danger" role="progressbar" aria-valuenow="85"
                             aria-valuemin="0" aria-valuemax="100" style="width: 85%">
                            <span class="sr-only">85% Complete (danger)</span>
                        </div>
                    </div>
                </div>
            </a>
        </li>
        <li class="divider"></li>
        <li>
    </ul>
    <ul id="dropdown4" class="dropdown-content dropdown-tasks w250 taskList">
        <li>
            <div>
                <strong>江广锋</strong>
                <span class="pull-right text-muted">
                                        <em>今天</em>
                                    </span>
            </div>
            <p>中华人民共和国万岁...</p>
            </a>
        </li>
        <li class="divider"></li>
        <li>
            <div>
                <strong>江广锋</strong>
                <span class="pull-right text-muted">
                                        <em>昨天</em>
                                    </span>
            </div>
            <p>中华人民共和国万岁...</p>
            </a>
        </li>
        <li class="divider"></li>
        <li>
            <a href="#">
                <div>
                    <strong>江广锋</strong>
                    <span class="pull-right text-muted">
                                        <em>昨天</em>
                                    </span>
                </div>
                <p>中华人民共和国万岁...</p>
            </a>
        </li>
        <li class="divider"></li>
        <li>
            <a class="text-center" href="#">
                <strong>查看所有</strong>
                <i class="fa fa-angle-right"></i>
            </a>
        </li>
    </ul>
    <!--/. NAV TOP  -->
    <nav class="navbar-default-dash navbar-side" role="navigation">


        <div class="sidebar-collapse">    
            <ul class="nav-dash" id="main-menu">

                <li>
                    <a class="active-menu waves-effect waves-dark" href="index.html"><i class="fa fa-dashboard"></i>
                        dash首页</a>
                </li>
                <li>
                    <a href="ui-elements.html" class="waves-effect waves-dark"><i class="fa fa-desktop"></i> 第一个</a>
                </li>
                <li>
                    <a href="chart.html" class="waves-effect waves-dark"><i class="fa fa-bar-chart-o"></i> 第一个</a>
                </li>
                <li>
                    <a href="tab-panel.html" class="waves-effect waves-dark"><i class="fa fa-qrcode"></i> 第一个</a>
                </li>

                <li>
                    <a href="table.html" class="waves-effect waves-dark"><i class="fa fa-table"></i> 第一个
                        </a>
                </li>
                <li>
                    <a href="form.html" class="waves-effect waves-dark"><i class="fa fa-edit"></i> 第一个 </a>
                </li>


                <li>
                    <a href="#" class="waves-effect waves-dark"><i class="fa fa-sitemap"></i> 第二个</a>
                    
                </li>
                <li>
                    <a href="empty.html" class="waves-effect waves-dark"><i class="fa fa-fw fa-file"></i> 第一个</a>
                </li>
            </ul>

        </div>

    </nav>
    <!-- /. NAV SIDE  -->
    内容

    <div id="page-wrapper-dash">
            # 内容
        <div id="page-wrapper-dash">

            {%app_entry%}
        </div>

        <!-- /. PAGE INNER  -->
    </div>
    <!-- /. PAGE WRAPPER  -->
            {%config%}
            {%scripts%}
            {%renderer%}
</div>
<!-- /. WRAPPER  -->
<!-- JS Scripts-->
<!-- jQuery Js -->

<!-- Bootstrap Js -->
<script src="assets/bootstrap.min.js"></script>

<script src="assets/materialize.min.js"></script>

<!-- Metis Menu Js -->
<script src="assets/jquery.metisMenu.js"></script>
<!-- Morris Chart Js -->
<script src="assets/raphael-2.1.0.min.js"></script>
<script src="assets/morris.js"></script>


<script src="assets/easypiechart.js"></script>
<script src="assets/easypiechart-data.js"></script>

<script src="assets/jquery.chart.js"></script>

<!-- Custom Js -->
<script src="assets/custom-scripts.js"></script>

</body>

</html>
"""

#<script src="assets/js/jquery-1.10.2.js"></script>

