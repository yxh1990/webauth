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
             else
             {
                getusernavhtml2();
             }
             $("#username").html(user["username"]);
          },
          error:function()
          {
              alert("获取用户权限异常");
          }
       });
}


function updateuserpasswd()
{
   $.ajax({
             url: restapi + '/updateuserpasswd',
             crossDomain: true,
             xhrFields: {
               withCredentials: true
             },
             data:{newpwd:$("#newpasswd").val()},
             type: 'POST',
             success: function () {
               alert("修改密码成功");
               $("#myModal").modal('hide');
               $(".modal-backdrop").hide();
             },
             error: function () {
               alert("修改密码失败");
             }
         });
}
