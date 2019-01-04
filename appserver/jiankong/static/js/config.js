var RestConfig = {
  "restip":"127.0.0.1",
  "restport":"5000"
};

var restapi ="http://"+RestConfig.restip+":"+RestConfig.restport;
function getadminnavhtml()
{
   $("#side-menu").load("/static/pages/adminnav.html",function(){loadnavcallback();});
}

function getusernavhtml2()
{
    $("#side-menu").load("/static/pages/usernav.html",function(){loadnavcallback();});
}

function getcheckloghtml()
{
    $("#side-menu").load("/static/pages/userlog.html",function(){loadnavcallback();});
}

function getfooterhtml()
{
     $("#footer").load("/static/pages/footer.html");
}

function getheaderhtml()
{
    //load() 方法允许加载html文档的一部分
    //加载header.html的idw为userinfo的html代码
    $("#header").load("/static/pages/header.html #userinfo");
    $("#updatepwd").load("/static/pages/header.html #myModal",function(){setupdatepasswdvalidate();});
}




function getusernavhtml()
{
      $.ajax({
          url:restapi+'/getusertype',
          type:'GET',
          dataType:'json',
          crossDomain: true,
          xhrFields: {
             withCredentials: true
          },
          success:function(user)
          {
             if(user["usertype"]==1)
             {
                getadminnavhtml();
             }
             else if(user["usertype"]==0)
             {
                getusernavhtml2();
             }
             else
             {
                 getcheckloghtml();
             }
             $("#username").html(user["username"]);
             $("#days").html("密码剩余有效天数:<font color='orange' size='3px'>"+user["redays"]+"</font>");
          },
          error:function()
          {

              alert("登录超时,请重新登录!");
              //console.log("获取用户权限异常,登录会话超时");
              var url = document.location.toString();
　　　　      var arrUrl = url.split("//");
　　　　      var Index = arrUrl[1].indexOf("/");
              var surl=arrUrl[1].substring(0,Index);
              //console.log(Index);
              //console.log(surl);
              window.location.href="http://"+surl;
          }
       });
}



