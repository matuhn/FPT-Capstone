<template>
  <div class="vue-tempalte">
    <section id="wrapper" class="login-register">
      <div class="login-box">
        <div class="white-box">
          <form class="form-horizontal form-material" id="loginform" action="index.html">
            <h3 class="box-title m-b-20">Sign Up</h3>
            <div class="form-group ">
              <div class="col-xs-12">
                <input class="form-control" v-model="input.fullname" type="text" required="" placeholder="Name">
              </div>
            </div>
            <div class="form-group ">
              <div class="col-xs-12">
                <input class="form-control" v-model="input.email" type="text" required="" placeholder="Email">
              </div>
            </div>
            <div class="form-group ">
              <div class="col-xs-12">
                <input class="form-control" v-model="input.username" type="text" required="" placeholder="Username">
              </div>
            </div>
            <div class="form-group ">
              <div class="col-xs-12">
                <input class="form-control" v-model="input.password" type="password" required="" placeholder="Password">
              </div>
            </div>
            <div class="form-group">
              <div class="col-xs-12">
                <input class="form-control" v-model="input.passwordConfirm" type="password" required="" placeholder="Confirm Password">
              </div>
            </div>
            <span v-html="message"></span>
            <div class="form-group">
              <div class="col-md-12">
                <div class="checkbox checkbox-primary p-t-0">
                  <input id="checkbox-signup" type="checkbox">
                  <label for="checkbox-signup"> I agree to all <a href="#">Terms</a></label>
                </div>
              </div>
            </div>
            <div class="form-group text-center m-t-20">
              <div class="col-xs-12">
                <button class="btn btn-info btn-lg btn-block text-uppercase waves-effect waves-light" v-on:click="signup()" type="button">Sign Up</button>
              </div>
            </div>
            <div class="form-group m-b-0">
              <div class="col-sm-12 text-center">
                <p>Already have an account? <router-link to="/login" class="text-primary m-l-5"><b>Sign In</b></router-link></p>
              </div>
            </div>
          </form>
        </div>
      </div>
    </section>

  </div>
</template>

<script>
import axios from "axios";
import qs from 'qs'

export default {
  name: 'signup',
  data() {
    return {
      input: {
        fullname: "",
        username: "",
        email: "",
        password: "",
        passwordConfirm: ""
      },
      message: ""
    }
  },
  methods: {
    signup() {
      if (this.input.username != "" && this.input.password != "") {
        axios({
          headers: {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PATCH, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "Origin, Content-Type, X-Auth-Token"
          },
          method: "POST",
          "url": this.$root.$data.host + "/api/auth/register",
          data: qs.stringify({
            fullname : this.input.fullname,
            username: this.input.username,
            password: this.input.password,
            email: this.input.email,
            confirm_password: this.input.passwordConfirm
          })
        }).then(result => {
          if (result.data.code == 200) {
            this.message = '<p class=\'text-success text-right\'>' + result.data.result + '</p>';
          } else {
            this.message = '<p class=\'text-danger text-right\'>' + result.data.result + '</p>';
          }
        }, error => {
          console.error(error);
        });
      } else {
        this.message = '<p class=\'text-danger text-right\'>Username/Password can not be blank!</p>';
      }

    }
  }
}

</script>