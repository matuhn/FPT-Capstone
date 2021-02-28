<template>
  <div class="vue-tempalte">
    <section id="wrapper" class="login-register">
      <div class="login-box">
        <div class="white-box">
          <form class="form-horizontal form-material" id="loginform" action="">
            <h3 class="box-title m-b-20">Sign In</h3>
            <div class="form-group ">
              <div class="col-xs-12">
                <input v-model="input.username" class="form-control" type="text" required="" placeholder="Username">
              </div>
            </div>
            <div class="form-group">
              <div class="col-xs-12">
                <input  @keyup.enter="login()" v-model="input.password" class="form-control" type="password" required="" placeholder="Password">
              </div>
            </div>
            <div class="form-group">
              <div class="col-md-12">
                <a href="javascript:void(0)" id="to-recover" class="text-dark pull-right"><i
                    class="fa fa-lock m-r-5"></i> Forgot pwd?</a></div>
            </div>
            <span v-html="message"></span>
            <div class="form-group text-center m-t-20">
              <div class="col-xs-12">
                <button class="btn btn-info btn-lg btn-block text-uppercase waves-effect waves-light"
                        v-on:click="login()" type="button">Log In
                </button>
              </div>
            </div>

            <div class="form-group m-b-0">
              <div class="col-sm-12 text-center">
                <p>Don't have an account?
                  <router-link class="text-primary m-l-5" to="/signup">Sign up</router-link>
                </p>
              </div>
            </div>
          </form>
          <form class="form-horizontal" id="recoverform" action="">
            <div class="form-group ">
              <div class="col-xs-12">
                <h3>Recover Password</h3>
                <p class="text-muted">Enter your Email and instructions will be sent to you! </p>
              </div>
            </div>
            <div class="form-group ">
              <div class="col-xs-12">
                <input v-model="input.email" class="form-control" type="text" required="" placeholder="Email">
              </div>
            </div>
            <div class="form-group text-center m-t-20">
              <div class="col-xs-12">
                <button v-on:click="reset()"
                        class="btn btn-primary btn-lg btn-block text-uppercase waves-effect waves-light" type="button">
                  Reset
                </button>
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
import qs from 'qs';


export default {
  name: 'login',
  data() {
    return {
      input: {
        username: "",
        password: "",
        email: ""
      },
      message: ""
    }
  },
  mounted() {
    this.$parent.checkAuthenticaion();
  },
  methods: {
    login() {
      if (this.input.username != "" && this.input.password != "") {
        axios({
          headers: {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials" : true
          },
          withCredentials: true,
          method: "POST",
          "url": this.$root.$data.host + "/api/auth/login",
          data: qs.stringify({
            username_or_email: this.input.username,
            password: this.input.password
          })
        }).then(result => {
          if (result.data.code == 200) {
            this.$emit("authenticated", true);
            this.$router.replace({name: "hello"});
          } else {
            this.message = '<p class=\'text-danger text-right\'>' + result.data.result + '</p>';
          }
        }, error => {
          console.error(error);
        });
      } else {
        this.message = '<p class=\'text-danger text-right\'>Tài khoản và mật khẩu không được bỏ trống</p>';
      }

    },
    reset() {
      axios({
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods": "GET, POST, PATCH, PUT, DELETE, OPTIONS",
          "Access-Control-Allow-Headers": "Origin, Content-Type, X-Auth-Token"
        }
        ,
        method: "POST",
        "url": this.$root.$data.host + "/api/auth/reset",
        data: qs.stringify({
          username_or_email: this.input.email
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
    }

  }
}
</script>

<style scoped>

</style>