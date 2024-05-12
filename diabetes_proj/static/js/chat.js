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
                data.messages.forEach(function(message) {
                    var messageHtml = `
                        <div class="message">
                            <p><strong>${message.sender_username}</strong> -> ${message.recipient_username}: ${message.content}</p>
                            <p>Отправлено: ${message.timestamp}</p>
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