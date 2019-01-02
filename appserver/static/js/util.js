function getQueryString(name)
{
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
    var r = window.location.search.substr(1).match(reg);
    if (r != null) return decodeURI(r[2]); return null;
}

function reloadpage()
{
    window.location.reload();
}

function setupdatepasswdvalidate()
{
     $('#updatepasswdForm').bootstrapValidator({
             message: '验证失败',
             feedbackIcons: {
                 valid: 'glyphicon glyphicon-ok',
                 invalid: 'glyphicon glyphicon-remove',
                 validating: 'glyphicon glyphicon-refresh'
             },
             fields: {
                oldpasswd: {
                    validators: {
                        notEmpty: {
                            message: '原密码不能为空'
                        },
                        stringLength: {
                            min: 8,
                            max: 20,
                            message: '长度必须在8-20个字符之间'
                        },
                         regexp: {
                            regexp: /^.*(?=.{8,})(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*? ]).*$/,
                            message: '最少8位,至少包含1个大小写字母,1个数字,1个特殊字符'
                        }
                    }
                },
                newpasswd: {
                    validators: {
                        notEmpty: {
                            message: '密码不能为空'
                        },
                        stringLength: {
                            min: 8,
                            max: 20,
                            message: '密码的长度必须在8-20个字符之间'
                        },
                         regexp: {
                            regexp: /^.*(?=.{8,})(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*? ]).*$/,
                            message: '最少8位,至少包含1个大小写字母,1个数字,1个特殊字符'
                        },
                        identical: {
                            field: 'newconfirmPassword',
                            message: '和确认密码输入的内容不一致'
                        }
                    }
                },
                newconfirmPassword: {
                    validators: {
                        notEmpty: {
                            message: '确认密码不能为空'
                        },
                        identical: {
                            field: 'newpasswd',
                            message: '和密码输入的不一致'
                        }
                    }
                }
            }
        });
}

function updateuserpasswd()
{
     $("#updatepasswdForm").bootstrapValidator('validate'); //提交表单验证
     var res=$("#updatepasswdForm").data('bootstrapValidator').isValid(); //获取验证结果
    if(res)
    {
        $.ajax({
            url: restapi + '/updateuserpasswd',
            crossDomain: true,
            xhrFields: {
                withCredentials: true
            },
            data: {newpwd: $("#newpasswd").val()},
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
}