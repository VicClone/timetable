<template>
  <div class="login">
    <div class="login__form">
      <!-- <label for="username"></label> -->
      <input
        class="login__input"
        type="text"
        v-model="login"
        placeholder="Введите логин"
        id="username">
      <!-- <label for="password"></label> -->
      <input
        class="login__input"
        type="password"
        v-model="password"
        placeholder="Введите пароль"
        id="password">
      <button
        class="login__send"
        @click="sendLogin"
        @keyup.enter="sendLogin()">
        Войти
      </button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import querystring from 'querystring'

export default {
  name: 'Login',
  data() {
    return {
      login: '',
      password: '',
    }
  },

  methods: {
    sendLogin() {
      axios.post('http://127.0.0.1:8000/auth/token/login', querystring.stringify({
        username: this.login,
        password: this.password
      }))
      .then(response => {
        sessionStorage.setItem('auth_token', response.data.data.attributes.auth_token)
        alert('Авторизация прошла успешно! Ваш токен: ' + response.data.data.attributes.auth_token)
        console.log(response.data.data.attributes.auth_token)
      })
      .catch(e => {
        alert('Ошибка! Неверно введен логин или пароль')
        console.log(e)
      })
    }
  },
}
</script>

<style>
  .login {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    min-height: 100%;
    height: 100%;
  }
  .login__form {
    margin: auto;
  }
  .login__input {
    display: block;
    margin: 20px;
    padding: 10px;
    color: black;
    width: 300px;
  }
  .login__send {
    width: 320px;
    padding: 10px;
    cursor: pointer;
  }
</style>
