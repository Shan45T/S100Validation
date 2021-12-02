$(document).ready(function () {
    
    $('#btnLogin').on('click', function () {
        var vUserName = $("#txtUserName").val();
        var vPassword = $("#txtPassword").val();
        if(vUserName == "" && vPassword=="")
        {
            alert("Plese enter UserName and Password.");
            $("#txtUserName").focus()
        }
        else if(vUserName == "")
        {
            alert("Plese enter UserName.");
            $("#txtUserName").focus();
        }
        else if(vPassword == "" )
        {
            alert("Plese enter Password.")
            $("#txtPassword").focus();
        }
        else
        {         
            $.ajax({
                type: "Post",
                url: "/api-token-auth",
                data: {username:vUserName,password:vPassword},
                async: false,
                success: function (response) {         
                    if (response != null && response != '') {
                       console.log(response);
                       localStorage.setItem('Auth',response.token);
                       let Authloken = localStorage.getItem('Auth');
                       window.location = '/home'
                    }
                    else {
                        alert(" Not Found ");
                        return false;
                    }
                },
                error: function (xhr, status, error) {
                    alert("Username or Password is invalid...Please enter valid Username and Password");
                    return false;
                },
                failure: function (xhr, status, failure) {
                    alert(failure);
                    return false;
                }
            });

        }

    });
});


document.addEventListener('keydown', function () {
    if (event.keyCode == 123) {
          //alert("This function has been disabled to prevent you from stealing my code!");
          return false;
    } else if (event.ctrlKey && event.shiftKey && event.keyCode == 73) {
          // alert("This function has been disabled to prevent you from stealing my code!");
          return false;
    } else if (event.ctrlKey && event.keyCode == 85) {
          //alert("This function has been disabled to prevent you from stealing my code!");
          return false;
    }
}, false);

if (document.addEventListener) {
    document.addEventListener('contextmenu', function (e) {
          // alert("This function has been disabled to prevent you from stealing my code!");
          e.preventDefault();
    }, false);
} else {
    document.attachEvent('oncontextmenu', function () {
          // alert("This function has been disabled to prevent you from stealing my code!");
          window.event.returnValue = false;
    });
}



document.onkeypress = function (event) {  
    event = (event || window.event);  
    if (event.keyCode == 123) {  
    return false;  
    }  
    }  
    document.onmousedown = function (event) {  
    event = (event || window.event);  
    if (event.keyCode == 123) {  
    return false;  
    }  
    }  
    document.onkeydown = function (event) {  
    event = (event || window.event);  
    if (event.keyCode == 123) {  
    return false;  
    }  
}
function Signup(){
    window.location = '/signup'    
}
function Clear(){    
    $("#txtUserName").val("");
    $("#txtPassword").val("");
    $("#txtUserName").focus();
}
function ChangePassword(){
    window.location = '/changepassword'
}