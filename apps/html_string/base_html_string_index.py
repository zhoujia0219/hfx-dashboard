base_html_string_index = r"""
<!DOCTYPE html>
<html lang="zxx">
   <head>
       <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>

      <!-- The above 6 meta tags *must* come first in the head; any other head content must come *after* these tags -->
      <meta charset="utf-8">
      <meta http-equiv="x-ua-compatible" content="IE=edge">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <meta name="description" content="">
      <meta name="keyword" content="">
      <meta name="author"  content=""/>
      <!-- Page Title -->
      <title>HFX</title>
      <!-- Main CSS -->			
      <link type="text/css" rel="stylesheet" href="assets/1bootstrap.min.css"/>
      <link type="text/css" rel="stylesheet" href="assets/2font-awesome.min.css"/>
      <link type="text/css" rel="stylesheet" href="assets/3flag-icon.min.css"/>
      <link type="text/css" rel="stylesheet" href="assets/4simple-line-icons.css">
      <link type="text/css" rel="stylesheet" href="assets/5ionicons.css">
      <link type="text/css" rel="stylesheet" href="assets/6toastr.min.css">
      <link type="text/css" rel="stylesheet" href="assets/7chartist.css">
      <link type="text/css" rel="stylesheet" href="assets/8apexcharts.css">
      <link type="text/css" rel="stylesheet" href="assets/9app.min.css"/>
      <link type="text/css" rel="stylesheet" href="assets/10style.min.css"/>
      <!-- Favicon -->	
      <link rel="icon" href="assets/favicon.ico" type="image/x-icon">
      <script src="http://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="http://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
      <![endif]-->
      
        {%favicon%}
        {%css%}

      
   </head>
   <body>
      <!--================================-->
      <!-- Page Container Start -->
      <!--================================-->
      <div class="page-container">
         <!--================================-->
         <!-- Page Sidebar Start -->
         <!--================================-->
             <div class="page-sidebar-dash">
        <div class="logo log-dash">
            <a class="logo-img " href="index.html">
                <img class="desktop-logo" src="assets/images/睿博数据__4_.png" alt="">
                 
                 <!--                    <img class="small-logo" src="assets/images/睿博数据__4_.png" alt="">-->


<!--                <h3><strong>RUIPOS</strong></h3>-->
            </a>
            <i class="ion-ios-close-empty" id="sidebar-toggle-button-close"></i>
        </div>

            <!--================================-->
            <!-- Sidebar Menu Start -->
            <!--================================-->
            <div class="page-sidebar-inner">
               <div class="page-sidebar-menu">
                  <ul class="accordion-menu">
                     <li class="open active">
                        <a href="/sales/bymonth/"><i data-feather="home"></i>
                        <span>首页</span></a>
                     </li>
                     
                      <li class="menu-divider mg-y-20-force"></li>
                     <li>
                        <a href="/real_time/"><i data-feather="mail"></i>
                        <span>实时销售看板</span></a>
                     </li>
                   <li class="menu-divider mg-y-20-force"></li>
                     <li>
                        <a href="/store_inspection/"><i data-feather="layout"></i>
                        <span>常规巡检看板</span></a>
                     </li>
                     <li class="menu-divider mg-y-20-force"></li>
                     <li>
                        <a href="/self/checking"><i data-feather="grid"></i>
                        <span>自检看板</span></a>
                     </li>
                                          <li class="menu-divider mg-y-20-force"></li>

                     <li>
                        <a href=""><i data-feather="gift"></i>
                        <span></span></a>
                     </li>
                                          <li class="menu-divider mg-y-20-force"></li>

                     <li>
                        <a href="/to_import/0"><i data-feather="command"></i>  
                        <span>数据传输</span></a>
                     </li>
                                          <li class="menu-divider mg-y-20-force"></li>

                     <li>
                        <a href="/caidapang_data/"><i data-feather="calendar"></i>
                        <span>门店数据模型</span></a>
                     </li>
                                          <li class="menu-divider mg-y-20-force"></li>

                     <li>
                        <a href=""><i data-feather="database"></i>
                        <span>第八个页面</span></a>
                     </li>
                                          <li class="menu-divider mg-y-20-force"></li>

                     <li>
                        <a href=""><i data-feather="pie-chart"></i>
                        <span>第九个页面</span></a>
                     </li>
                                          <li class="menu-divider mg-y-20-force"></li>

                     <li>
                        <a href=""><i data-feather="map"></i>
                        <span>第十个页面</span></a>
                     </li>
                    
                   
                   
                  </ul>
               </div>
            </div>
            <!--/ Sidebar Menu End -->
            <!--================================-->
            <!-- Sidebar Footer Start -->
            <!--================================-->
            <div class="sidebar-footer">									
               <a class="pull-left" href="page-profile.html" data-toggle="tooltip" data-placement="top" data-original-title="Profile">
               <i data-feather="user" class="ht-15"></i></a>									
               <a class="pull-left " href="mailbox.html" data-toggle="tooltip" data-placement="top" data-original-title="Mailbox">
               <i data-feather="mail" class="ht-15"></i></a>
               <a class="pull-left" href="page-unlock.html" data-toggle="tooltip" data-placement="top" data-original-title="Lockscreen">
               <i data-feather="lock" class="ht-15"></i></a>
               <a class="pull-left" href="page-singin.html" data-toggle="tooltip" data-placement="top" data-original-title="Sing Out">
               <i data-feather="log-out" class="ht-15"></i></a>
            </div>
            <!--/ Sidebar Footer End -->
         </div>
         <!--/ Page Sidebar End -->
         <!--================================-->
         <!-- Page Content Start -->
         <!--================================-->
         <div class="page-content">
            <!--================================-->
            <!-- Page Header Start -->
            <!--================================-->
            <div class="page-header">
               <div class="search-form">
                  <form action="#" method="GET">
                     <div class="input-group">
                        <input class="form-control search-input" name="search" placeholder="Type something..." type="text"/>
                        <span class="input-group-btn">
                        <span id="close-search"><i class="ion-ios-close-empty"></i></span>
                        </span>
                     </div>
                  </form>
               </div>
               <!--================================-->
               <!-- Page Header  Start -->
               <!--================================-->
               <nav class="navbar navbar-expand-lg">
                  <ul class="list-inline list-unstyled mg-r-20">
                     <!-- Mobile Toggle and Logo -->
                     <li class="list-inline-item align-text-top"><a class="hidden-md hidden-lg" href="#" id="sidebar-toggle-button"><i class="ion-navicon tx-20" ></i></a></li>
                     <!-- PC Toggle and Logo -->
                     <li class="list-inline-item align-text-top"><a class="hidden-xs hidden-sm" href="#" id="collapsed-sidebar-toggle-button"><i class="ion-navicon tx-20" data-feather="align-left"><-</i></a></li>
                  </ul>
                  <!--================================-->
                  <!-- Mega Menu Start -->
                  <!--================================-->
                  <div class="collapse navbar-collapse">
                     
                  </div>
                  <!--/ Mega Menu End-->
                  <!--/ Brand and Logo End -->
                  <!--================================-->
                  <!-- Header Right Start -->
                  <!--================================-->
                  <div class="header-right pull-right">
                     <ul class="list-inline justify-content-end">
                        <li class="list-inline-item align-middle"><a  href="#" id="search-button"><i class="ion-ios-search-strong tx-20" data-feather="search"></i></a></li>
                        <!--================================-->
                        
                        <!--/ Notifications Dropdown End -->
                        <!--================================-->
                        <!-- Messages Dropdown Start -->
                        <!--================================-->
                        
                        <!--/ Messages Dropdown End -->
                        <!--================================-->
                        <!-- Profile Dropdown Start -->
                        <!--================================-->
                        <li class="list-inline-item dropdown">
                           <a  href="" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"><span class="select-profile">Hi, 江广锋!</span><img src="assets/976e7fdcdb3a30b0063dd4c312aa1a94.jpeg"" class="img-fluid wd-35 ht-35 rounded-circle" alt=""></a>
                           <div class="dropdown-menu dropdown-menu-right dropdown-profile shadow-2">
                              <div class="user-profile-area">
                                 <div class="user-profile-heading">
                                    <div class="profile-thumbnail">
                                       <img src="https://via.placeholder.com/100x100" class="img-fluid wd-35 ht-35 rounded-circle" alt="">
                                    </div>
                                    <div class="profile-text">
                                       <h6>江广锋</h6>
                                       <span>jiangguangfeng@163.com</span>
                                    </div>
                                 </div>
                                 <a href="" class="dropdown-item"><i class="icon-user" aria-hidden="true"></i> 个人信息</a>
                                 <a href="" class="dropdown-item"><i class="icon-envelope" aria-hidden="true"></i> 消息 <span class="badge badge-success ft-right mg-t-3">10+</span></a>
                                 <a href="" class="dropdown-item"><i class="icon-settings" aria-hidden="true"></i> 配置</a>
                                 <a href="" class="dropdown-item"><i class="icon-share" aria-hidden="true"></i> 我的活动 <span class="badge badge-warning ft-right mg-t-3">5+</span></a>
                                 <a href="" class="dropdown-item"><i class="icon-cloud-download" aria-hidden="true"></i> 我的下载 <span class="badge badge-success ft-right mg-t-3">10+</span></a>
                                 <a href="" class="dropdown-item"><i class="icon-heart" aria-hidden="true"></i> 帮助</a>
                                 <a href="page-singin.html" class="dropdown-item"><i class="icon-power" aria-hidden="true"></i> 注销</a>
                              </div>
                           </div>
                        </li>
                        <!-- Profile Dropdown End -->
                        <!--================================-->
                        <!-- Setting Sidebar Start -->
                        <!--================================-->
                        
                        <!--/ Setting Sidebar End -->
                     </ul>
                     
                  </div>
                  <!--/ Header Right End -->
               </nav>
            </div>
            <!--/ Page Header End -->
            <!--================================-->
            <!-- Page Inner Start -->
            <!--================================-->
            <div class="page-inner">
               <div id="main-wrapper">

               <!-- Main Wrapper -->
<!--               ## 内容-->
                {%app_entry%}
                </div>
               <!--/ Main Wrapper End -->
            </div>
            <!--/ Page Inner End -->
            <!--================================-->
            <!-- Page Footer Start -->	
            <!--================================-->
            <footer class="page-footer">
               <div class="pd-t-4 pd-b-0 pd-x-20">
                  <div class="tx-10 tx-uppercase">
                     <p class="pd-y-10 mb-0">Copyright&copy; 2019 | All rights reserved. | Created By <a href="http://www.bootstrapmb.com/" target="_blank">ColorlibCode</a></p>
                  </div>
               </div>
            </footer>
            <!--/ Page Footer End -->		
         </div>
         <!--/ Page Content End -->
      </div>
      <!--/ Page Container End -->
      <!--================================-->
      <!-- Scroll To Top Start-->
      <!--================================-->	
      <a href="" data-click="scroll-top" class="btn-scroll-top fade"><i class="fa fa-arrow-up"></i></a>
      <!--/ Scroll To Top End -->
      <!--================================-->
      <!-- Setting Sidebar Start -->
      <!--================================-->
      
      	  

      
      <!--/ Setting Sidebar End  -->      
      <!--================================-->
 
      <!--================================-->
      <!-- Footer Script -->
      <!--================================-->

      


            {%config%}
            {%scripts%}
            {%renderer%}  
   </body>
</html>
"""
