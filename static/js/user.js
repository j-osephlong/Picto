function setupServerListeners()
{
    socket.on('reload-device', (res) => {forceReload()})
    socket.on('server-message', (res) => {alert(res['message'])})
}

function verifyID (res)
{
    if (appV.$cookies.isKey("userID") == false)
    {
        appV.$cookies.set('userID', res['newID'], 60*60*24*365)

        appV.id = appV.$cookies.get('userID')
        console.log('[user.js] New ID assigned, ' + appV.id)
    }
    else if (res['isValid'])
    {
        appV.id = appV.$cookies.get('userID')
        console.log('[user.js] userID valid')
        //do stuff
    }
    else 
    {
        console.log('[user.js] userID invalid')
        alert("ID Invalid, reloading.")
        appV.$cookies.remove('userID')
        forceReload()
    }
} 

function vIDAjax ()
{
    let reqJSON = {}
    if (appV.$cookies.isKey('userID') == false)
        reqJSON['newName'] = prompt("New User", "What do you wanna be known as?")
    else 
        reqJSON['userID'] = appV.$cookies.get('userID')

    $.ajax({
        url: '/check_id',
        contentType: "application/json",
        // dataType: "json", this prevents done from firing
        data: JSON.stringify(reqJSON),
        type: 'POST',
        success: function(res) {
            verifyID(res)
        }
    })
} 

function forceReload()
{
    $.ajax({
        url: window.location.href,
        headers: {
            "Pragma": "no-cache",
            "Expires": -1,
            "Cache-Control": "no-cache"
        }
    }).done(function () {
        window.location.reload(true);
    });
}

function getUserData()
{
    let reqJSON = {'userID' : appV.id}

    $.ajax({
        url: '/user_data',
        contentType: "application/json",
        // dataType: "json", this prevents done from firing
        data: JSON.stringify(reqJSON),
        type: 'POST',
        success: function(res) {
            user = JSON.parse(res)
            console.log(res)
        }
    })
}

function updateUserData(name = null, color = null)
{
    let reqJSON = {'userID' : appV.id}
    if (name != null)
        reqJSON['name'] = name
    if (color != null)
        reqJSON['color'] = color

    $.ajax({
        url: '/update_user',
        contentType: "application/json",
        // dataType: "json", this prevents done from firing
        data: JSON.stringify(reqJSON),
        type: 'POST',
        success: function(res) {
            console.log(res)
        }
    })
}