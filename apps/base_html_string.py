base_html_string = """
<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no" />
<title>首页 - HFX</title>
{%favicon%}
<meta name="keywords" content="HFX">
<meta name="description" content="HFX">
<meta name="author" content="jgf">
# <link href="static/css/bootstrap.min.css" rel="stylesheet">
# <link href="static/css/materialdesignicons.min.css" rel="stylesheet">
# <link href="static/css/style.min.css" rel="stylesheet">

    <link rel="stylesheet" href="assets/materialize/css/1materialize.min.css" media="screen,projection"/>

{%css%}
</head>
  
<body>
<div class="lyear-layout-web">
  <div class="lyear-layout-container">
    <!--左侧导航-->
    <aside class="lyear-layout-sidebar">
      
      <!-- logo -->
      <div id="logo" class="sidebar-header">
        <a href="index.html">
<!--          <img src="images/logo-sidebar.png" title="LightYear" alt="LightYear" />  logo引入-->
            HFX
        </a>
      </div>
      <div class="lyear-layout-sidebar-scroll"> 
        <h1 class="qwert">飛機人工費軟件股份</h1>
        <nav class="sidebar-main">
          <ul class="nav nav-drawer">
            <li class="nav-item active"> <a href="index.html"><i class="mdi mdi-home"></i> 首页</a> </li>
            <li class="nav-item nav-item-has-subnav">
              <a href="javascript:void(0)"><i class="mdi mdi-palette"></i> 第二</a>

            </li>
            <li class="nav-item nav-item-has-subnav">
              <a href="javascript:void(0)"><i class="mdi mdi-format-align-justify"></i> 第三</a>

            </li>
            <li class="nav-item nav-item-has-subnav">
              <a href="javascript:void(0)"><i class="mdi mdi-file-outline"></i> 第四分</a>

            </li>
            <li class="nav-item nav-item-has-subnav">
              <a href="javascript:void(0)"><i class="mdi mdi-language-javascript"></i> 第五分违法我</a>

            </li>
            <li class="nav-item nav-item-has-subnav">
              <a href="javascript:void(0)"><i class="mdi mdi-menu"></i> 第六分违法我</a>
            </li>
          </ul>
        </nav>
        
        <div class="sidebar-footer">
          <p class="copyright">Copyright &copy; 2019. <a target="_blank" href="http://lyear.itshubao.com">IT书包</a> All rights reserved.</p>
        </div>
      </div>
      
    </aside>
    <!--End 左侧导航-->
    
    <!--头部信息-->
    <header class="lyear-layout-header">
      
      <nav class="navbar navbar-default">
        <div class="topbar">
          
          <div class="topbar-left">
            <div class="lyear-aside-toggler">
              <span class="lyear-toggler-bar"></span>
              <span class="lyear-toggler-bar"></span>
              <span class="lyear-toggler-bar"></span>
            </div>
            <span class="navbar-page-title"> 首页 </span>
          </div>
          
          <ul class="topbar-right">
            <li class="dropdown dropdown-profile">
              <a href="javascript:void(0)" data-toggle="dropdown">
                <img class="img-avatar img-avatar-48 m-r-10" src="images/users/avatar.jpg" alt="笔下光年" />
                <span>笔下光年 <span class="caret"></span></span>
              </a>
              <ul class="dropdown-menu dropdown-menu-right">
                <li> <a href="lyear_pages_profile.html"><i class="mdi mdi-account"></i> 个人信息</a> </li>
                <li> <a href="lyear_pages_edit_pwd.html"><i class="mdi mdi-lock-outline"></i> 修改密码</a> </li>
                <li> <a href="javascript:void(0)"><i class="mdi mdi-delete"></i> 清空缓存</a></li>
                <li class="divider"></li>
                <li> <a href="lyear_pages_login.html"><i class="mdi mdi-logout-variant"></i> 退出登录</a> </li>
              </ul>
            </li>
            <!--切换主题配色-->
		    <li class="dropdown dropdown-skin">
			  <span data-toggle="dropdown" class="icon-palette"><i class="mdi mdi-palette"></i></span>
			  <ul class="dropdown-menu dropdown-menu-right" data-stopPropagation="true">
                <li class="drop-title"><p>主题</p></li>
                <li class="drop-skin-li clearfix">
                  <span class="inverse">
                    <input type="radio" name="site_theme" value="default" id="site_theme_1" checked>
                    <label for="site_theme_1"></label>
                  </span>
                  <span>
                    <input type="radio" name="site_theme" value="dark" id="site_theme_2">
                    <label for="site_theme_2"></label>
                  </span>
                  <span>
                    <input type="radio" name="site_theme" value="translucent" id="site_theme_3">
                    <label for="site_theme_3"></label>
                  </span>
                </li>
			    <li class="drop-title"><p>LOGO</p></li>
				<li class="drop-skin-li clearfix">
                  <span class="inverse">
                    <input type="radio" name="logo_bg" value="default" id="logo_bg_1" checked>
                    <label for="logo_bg_1"></label>
                  </span>
                  <span>
                    <input type="radio" name="logo_bg" value="color_2" id="logo_bg_2">
                    <label for="logo_bg_2"></label>
                  </span>
                  <span>
                    <input type="radio" name="logo_bg" value="color_3" id="logo_bg_3">
                    <label for="logo_bg_3"></label>
                  </span>
                  <span>
                    <input type="radio" name="logo_bg" value="color_4" id="logo_bg_4">
                    <label for="logo_bg_4"></label>
                  </span>
                  <span>
                    <input type="radio" name="logo_bg" value="color_5" id="logo_bg_5">
                    <label for="logo_bg_5"></label>
                  </span>
                  <span>
                    <input type="radio" name="logo_bg" value="color_6" id="logo_bg_6">
                    <label for="logo_bg_6"></label>
                  </span>
                  <span>
                    <input type="radio" name="logo_bg" value="color_7" id="logo_bg_7">
                    <label for="logo_bg_7"></label>
                  </span>
                  <span>
                    <input type="radio" name="logo_bg" value="color_8" id="logo_bg_8">
                    <label for="logo_bg_8"></label>
                  </span>
				</li>
				<li class="drop-title"><p>头部</p></li>
				<li class="drop-skin-li clearfix">
                  <span class="inverse">
                    <input type="radio" name="header_bg" value="default" id="header_bg_1" checked>
                    <label for="header_bg_1"></label>                      
                  </span>                                                    
                  <span>                                                     
                    <input type="radio" name="header_bg" value="color_2" id="header_bg_2">
                    <label for="header_bg_2"></label>                      
                  </span>                                                    
                  <span>                                                     
                    <input type="radio" name="header_bg" value="color_3" id="header_bg_3">
                    <label for="header_bg_3"></label>
                  </span>
                  <span>
                    <input type="radio" name="header_bg" value="color_4" id="header_bg_4">
                    <label for="header_bg_4"></label>                      
                  </span>                                                    
                  <span>                                                     
                    <input type="radio" name="header_bg" value="color_5" id="header_bg_5">
                    <label for="header_bg_5"></label>                      
                  </span>                                                    
                  <span>                                                     
                    <input type="radio" name="header_bg" value="color_6" id="header_bg_6">
                    <label for="header_bg_6"></label>                      
                  </span>                                                    
                  <span>                                                     
                    <input type="radio" name="header_bg" value="color_7" id="header_bg_7">
                    <label for="header_bg_7"></label>
                  </span>
                  <span>
                    <input type="radio" name="header_bg" value="color_8" id="header_bg_8">
                    <label for="header_bg_8"></label>
                  </span>
				</li>
				<li class="drop-title"><p>侧边栏</p></li>
				<li class="drop-skin-li clearfix">
                  <span class="inverse">
                    <input type="radio" name="sidebar_bg" value="default" id="sidebar_bg_1" checked>
                    <label for="sidebar_bg_1"></label>
                  </span>
                  <span>
                    <input type="radio" name="sidebar_bg" value="color_2" id="sidebar_bg_2">
                    <label for="sidebar_bg_2"></label>
                  </span>
                  <span>
                    <input type="radio" name="sidebar_bg" value="color_3" id="sidebar_bg_3">
                    <label for="sidebar_bg_3"></label>
                  </span>
                  <span>
                    <input type="radio" name="sidebar_bg" value="color_4" id="sidebar_bg_4">
                    <label for="sidebar_bg_4"></label>
                  </span>
                  <span>
                    <input type="radio" name="sidebar_bg" value="color_5" id="sidebar_bg_5">
                    <label for="sidebar_bg_5"></label>
                  </span>
                  <span>
                    <input type="radio" name="sidebar_bg" value="color_6" id="sidebar_bg_6">
                    <label for="sidebar_bg_6"></label>
                  </span>
                  <span>
                    <input type="radio" name="sidebar_bg" value="color_7" id="sidebar_bg_7">
                    <label for="sidebar_bg_7"></label>
                  </span>
                  <span>
                    <input type="radio" name="sidebar_bg" value="color_8" id="sidebar_bg_8">
                    <label for="sidebar_bg_8"></label>
                  </span>
				</li>
			  </ul>
			</li>
            <!--切换主题配色-->
          </ul>
          
        </div>
      </nav>
      
    </header>
    <!--End 头部信息-->
    
    <!--页面主要内容-->
    <main class="lyear-layout-content">
          <div class="container-fluid">
            {%app_entry%}
          </div>
    </main>
    <!--End 页面主要内容-->
    {%config%}
    {%scripts%}
    {%renderer%}
    
  </div>
</div>

<script type="text/javascript" src="js/jquery.min.js"></script>
<script type="text/javascript" src="js/bootstrap.min.js"></script>
<script type="text/javascript" src="js/perfect-scrollbar.min.js"></script>
<script type="text/javascript" src="js/main.min.js"></script>

<!--图表插件-->
<script type="text/javascript" src="js/Chart.js"></script>
<script type="text/javascript">
$(document).ready(function(e) {
    var $dashChartBarsCnt  = jQuery( '.js-chartjs-bars' )[0].getContext( '2d' ),
        $dashChartLinesCnt = jQuery( '.js-chartjs-lines' )[0].getContext( '2d' );
    
    var $dashChartBarsData = {
		labels: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
		datasets: [
			{
				label: '注册用户',
                borderWidth: 1,
                borderColor: 'rgba(0,0,0,0)',
				backgroundColor: 'rgba(51,202,185,0.5)',
                hoverBackgroundColor: "rgba(51,202,185,0.7)",
                hoverBorderColor: "rgba(0,0,0,0)",
				data: [2500, 1500, 1200, 3200, 4800, 3500, 1500]
			}
		]
	};
    var $dashChartLinesData = {
		labels: ['2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014'],
		datasets: [
			{
				label: '交易资金',
				data: [20, 25, 40, 30, 45, 40, 55, 40, 48, 40, 42, 50],
				borderColor: '#358ed7',
				backgroundColor: 'rgba(53, 142, 215, 0.175)',
                borderWidth: 1,
                fill: false,
                lineTension: 0.5
			}
		]
	};
    
    new Chart($dashChartBarsCnt, {
        type: 'bar',
        data: $dashChartBarsData
    });
    
    var myLineChart = new Chart($dashChartLinesCnt, {
        type: 'line',
        data: $dashChartLinesData,
    });
});
</script>
</body>
</html>"""
