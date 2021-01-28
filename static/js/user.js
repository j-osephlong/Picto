let tokenInRoute = false

function auth(username, password) {
    $.ajax({
        url: '/user/auth', // point to server-side URL
        cache: false,
        contentType: false,
        processData: false,
        data: JSON.stringify({'userName':username,'password':password}),
        type: 'POST',
        error: ()=>{
            if ('error' in res)
                alert(res['error'])
        }
    }).done(function (res) {
        console.log(res)
        appV.username = username
        setToken(res['token'], username)
    }) 
}

function register(username, password) {
    $.ajax({
        url: '/user/register', // point to server-side URL
        cache: false,
        contentType: false,
        processData: false,
        data: JSON.stringify({'userName':username,'password':password}),
        type: 'POST',
        error: ()=>{
            if ('error' in res)
                alert(res['error'])
        }
    }).done(function (res) {
        console.log(res)
        appV.username = username
        setToken(res['token'], username)
    }) 
}

function setToken(newToken, username = null)
{   
    tokenInRoute = false;

    appV.token = newToken
    $cookies.set('tempToken', newToken)
    if (username != null)
    {
        $cookies.set('username', username)
    }
}

function getToken()
{
    tokenInRoute = true;
    if (appV.token != null)
        return appV.token 
   
    if (!$cookies.isKey('tempToken'))
        return null
    appV.token = $cookies.get('tempToken')

    return appV.token
}

function badToken() {
    console.log('removed bad user data')
    $cookies.remove('username')
    $cookies.remove('tempToken')
    appV.token = null
    appV.username = null
    // alert('Token in route?:'+tokenInRoute)

    if (document.location.pathname != "/")
        document.location = "/#badtoken"
}

function testToken() {
    function test()
    {
        var valid = null

        $.ajax({
            url: '/user/me', // point to server-side URL
            cache: false,
            contentType: false,
            processData: false,
            data: JSON.stringify({'userName':appV.username,'token':getToken()}),
            type: 'POST',
            async: false,
            success: function (res) {
                console.log(res)
                if ('error' in res)
                {
                    console.log('server rejects token')  
                    valid = false;
                }
                else
                {
                    console.log('server accepts token')
                    setToken(res['newToken'])
                    valid = true
                }
            }
        }) 
        return valid;
    }

    if (!test())
        badToken()
}