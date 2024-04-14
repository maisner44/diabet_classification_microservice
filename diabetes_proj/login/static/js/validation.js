document.addEventListener('DOMContentLoaded', function(){

    var form = document.getElementById('patient');

    form.addEventListener('submit', function(event){
        event.preventDefault();

        if (!username_validation() 
        || !email_validation() 
        || !password_validation()
        || !initials_validation()
        || !phone_validator()
        || !height_weight_validator()){
            return false;
        }

        form.submit();    
    });

    function username_validation(){
        var username = document.getElementById('username').value;
        var usernameFeedback = document.getElementById('username-feedback');
        var username_error = document.getElementById('username');

        if (username === ''){
            usernameFeedback.innerText = 'Заповніть поле логіну';
            username_error.classList.add('invalid');
            return false;
        } else if (username.length < 6 || username.length > 32){
            usernameFeedback.innerText = 'Логін повинен бути більшим ніж 6 символів, але не більше 32';
            username_error.classList.add('invalid');
            return false;
        } else if (!isNaN(parseInt(username[0]))){
            usernameFeedback.innerText = 'Першим символом не повинно бути число';
            username_error.classList.add('invalid');
            return false;
        }
        usernameFeedback.innerText = '';
        username_error.classList.remove('invalid');
        return true;
    }

    function email_validation(){
        var email = document.getElementById('email').value;
        var emailFeedback = document.getElementById('email-feedback');
        var email_error = document.getElementById('email');

        var re = /\S+@\S+\.\S+/;
        if (!re.test(email)){
            emailFeedback.innerText = 'Некоректна адреса електронної пошти';
            email_error.classList.add('invalid');
            return false;
        }
        emailFeedback.innerText = '';
        email_error.classList.remove('invalid');
        return true;
    }

    function password_validation(){
        var password = document.getElementById('password').value;
        var password_repeat = document.getElementById('password2').value;
        var passwordError = document.getElementById('password');
        var passwordRepError = document.getElementById('password2');
        var passwordFeedback = document.getElementById('password-feedback');
        var passwordRepFeedback = document.getElementById('password1-feedback');

        if (password.length < 6 || password.length > 32){
            passwordError.classList.add('invalid');
            passwordFeedback.innerText = 'Пароль повинен бути від 6 до 32 символів';
            return false;
        } else if (password != password_repeat){
            passwordRepFeedback.innerText = 'Паролі не співпадають';
            passwordRepError.classList.add('invalid');
            return false;
        }

        passwordError.classList.remove('invalid');
        passwordRepError.classList.remove('invalid');
        passwordFeedback.innerText = '';
        passwordRepFeedback.innerText = '';
        return true;
    }

    function initials_validation(){
        var last_name = document.getElementById('last-name').value;
        var first_name = document.getElementById('first-name').value;
        var patronymic = document.getElementById('patronymic').value;
        var lastnameError = document.getElementById('last-name');
        var firstnameError = document.getElementById('first-name');
        var patronymicError = document.getElementById('patronymic');
        var lastnameFeedback = document.getElementById('lastname-feedback');
        var firstnameFeedback = document.getElementById('firstname-feedback');
        var patronymicFeedback = document.getElementById('patronymic-feedback');

        if (last_name === ''){
            lastnameError.classList.add('invalid');
            lastnameFeedback.innerText = 'Заповніть поле';
            return false;
        } else if (!checkForDigits(last_name)){
            lastnameError.classList.add('invalid');
            lastnameFeedback.innerText = 'У прізвищі не може бути цифр';
            return false;
        }

        if (first_name === ''){
            firstnameError.classList.add('invalid');
            firstnameFeedback.innerText = 'Заповніть поле';
            return false;
        } else if (!checkForDigits(last_name)){
            firstnameError.classList.add('invalid');
            firstnameFeedback.innerText = 'У імені не може бути цифр';
            return false;
        }

        if (patronymic === ''){
            patronymicError.classList.add('invalid');
            patronymicFeedbackFeedback.innerText = 'Заповніть поле';
            return false;
        } else if (!checkForDigits(last_name)){
            patronymicError.classList.add('invalid');
            patronymicFeedback.innerText = 'У прізвищі не може бути цифр';
            return false;
        }
        
        firstnameError.classList.remove('invalid');
        lastnameError.classList.remove('invalid');
        patronymicError.classList.remove('invalid');
        firstnameFeedback.innerText = '';
        lastnameFeedback.innerText = '';
        patronymicFeedback.innerText = '';
        return true;
    }

    function phone_validator(){
        var phone_number = document.getElementById('phone_number').value;
        var phoneNumError = document.getElementById('phone_number');
        var phoneFeedback = document.getElementById('phone_number-feedback');
        var re = /^\d+$/;

        if (phone_number.length > 10){
            phoneNumError.classList.add('invalid');
            phoneFeedback.innerText = 'Занадто довгий номер телефону (пишіть без +38)';
            return false;
        } else if (!re.test(phone_number)){
            phoneNumError.classList.add('invalid');
            phoneFeedback.innerText = 'Номер телефону може містити лише цифри';
            return false;
        }
        phoneNumError.classList.remove('invalid');
        phoneFeedback.innerText = '';
        return true;
    }

    function height_weight_validator(){
        var height = document.getElementById('height').value;
        var weight = document.getElementById('weight').value;
        var heightError = document.getElementById('height');
        var weightError = document.getElementById('weight');
        var heightFeedback = document.getElementById('height-feedback');
        var weightFeedback = document.getElementById('weight-feedback');

        if (height.length > 5){
            heightError.classList.add('invalid');
            heightFeedback.innerText = 'Некоректний зріст';
            return false;
        } else if (height[1] != '.'){
            var validHeight = height.substring(0,1) + '.' + height.substring(1);
            heightError.value = validHeight;
        }

        if (weight.length > 4){
            weightError.classList.add('invalid');
            weightFeedback.innerText = 'Некоректна вага';
            return false;
        }

        heightError.classList.remove('invalid');
        weightError.classList.remove('invalid');
        heightFeedback.innerText = '';
        weightFeedback.innerText = '';
        return true;
    }



    function checkForDigits(word) {
        var regex = /\d/;
        return !regex.test(word);
    }
});

