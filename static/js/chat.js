let socket = io.connect('http://' + document.domain + ':' + location.port);

let bucketMessages = []
let message_offset = 0

document.addEventListener('DOMContentLoaded', e=>{
    socket.on('newMessage', (message) =>
    {
        if (message['bucket'] != appV.bucket) return
        
        console.log(message)
        bucketMessages.push({id : message['messageID'], name : message['userName'], message :message['image']})
        
        $('#messages-container').animate({scrollTop :  $('#messages-container').prop('scrollHeight')}, 750)
    })

})

function sendMessage() {
    let reqJSON = {
        'image': ""+canvas.toDataURL('image/png'),
        'userID': appV.$cookies.get('userID'),
        'bucket': appV.bucket
    }

    $.ajax({
        url: '/send_message', // point to server-side URL
        cache: false,
        contentType: false,
        processData: false,
        data: JSON.stringify(reqJSON),
        type: 'POST',
        success: function (response) { // display success response
            console.log('Message sent')
        },
        error: function (response) {
            console.log('Message not sent')
        }

    }); 
}

function fetchMessages(n, offset) {
    let preScroll = $('#messages-container').scrollTop()
    let oldHeight = $('#messages-container').height()

    $.ajax({
        url: '/get_messages', // point to server-side URL
        cache: false,
        contentType: false,
        processData: false,
        data: JSON.stringify({'n' : n, 'offset': offset, 'bucket' : appV.bucket}),
        type: 'POST',
        success: function (res) { // display success response   
            messages = JSON.parse(res)

            if (messages.length == 0) {
                console.log('[chat.js] No messages to fetch')
                return 
            }
            console.log(messages)
            
            let newBatch = []
            messages.reverse().forEach(message => {
                newBatch.push({id : message['messageID'], name : message['userName'], message :message['image']})
                message_offset++
            });
            bucketMessages = [...newBatch, ...bucketMessages]

            appV.messages = bucketMessages
        },
        error: function (res) {
            console.log('Could not fetch messages')
        }

    }) 

}