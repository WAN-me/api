# wm-api
## How to use?
Для начала необходимо зарегистрироваться. Для этого небходимо сделать запрос на /reg передав несколько параметров:

`name` - имя пользователя

`email` - ваш адрес эл.почты. Он никак не проверяется, можно закинуть любую строку, но тогда восстановить доступ при потере пароля будет невозможно 

`password` - пароль. На сервере он хранится в виде хеша 

Ответом будет json содержащий в себе информацию о только что зарегистрированном пользователе 

так же есть метод /user возвращающий информацию о пользователе, чей `accesstoken` был передан 
 
