$(document).ready(function() {
    loadMessages(senderId, receiverId);

    setInterval(function() {
        loadMessages(senderId, receiverId);
    }, 10000);

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!this.crossDomain) {
                xhr.setRequestHeader('X-CSRFToken', csrfToken);
            }
        }
    });

   
    function sendMessage(senderId, receiverId, messageText) {
        $.ajax({
            url: '/chat/send-message/',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                'sender_id': senderId,
                'receiver_id': receiverId,
                'message_text': messageText,
            }),
            success: function(data) {
                if (data.success) {
                    $('#message-text').val('');
                } else {
                    alert('Ошибка при отправке сообщения.');
                }
            },
            error: function(xhr, status, error) {
                console.error('Ошибка при отправке сообщения:', error);
            }
        });
    }

    function loadMessages(senderId, receiverId) {
        $.ajax({
            url: `/chat/load-messages/${senderId}/${receiverId}/`, 
            method: 'GET',
            success: function(data) {               
                $('#chat-container').empty();
                var currentUserId = parseInt($('#current-user-id').val());
                data.messages.forEach(function(message) {
                    var isSentMessage = (message.sender_id == currentUserId);
                    console.log(isSentMessage);
                    var messageHtml = `
                        <div class="message ${isSentMessage ? 'sent' : 'received'}">
                            <p class="message-sender"><strong>${message.sender_username}</strong></p><hr>
                            <p class="message-content">${message.content}</p>
                            <p class="message-timestamp">${message.timestamp}</p>
                        </div>
                    `;
                    $('#chat-container').append(messageHtml);
                });
            },
            error: function(xhr, status, error) {
                console.error('Ошибка при загрузке сообщений:', error);
            }
        });
    }

    $('#message-form').submit(function(e) {
        e.preventDefault();
        var senderId = $('#sender-id').val();
        var receiverId = $('#receiver-id').val();
        var messageText = $('#message-text').val();

        sendMessage(senderId, receiverId, messageText);
    });
});