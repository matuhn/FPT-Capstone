<template>
  <div class="profile row">
    <div class="col-md-4 col-xs-12">
      <div class="white-box">
        <div class="user-bg"><img width="100%" alt="user" src="../assets/images/large/img1.jpg">
          <div class="overlay-box">
            <div class="user-content">
              <a href="javascript:void(0)"><img src="../assets/images/users/1.jpg" class="thumb-lg img-circle"
                                                alt="img"></a>
              <h4 class="text-white">User Name</h4>
              <h5 class="text-white" v-html="$parent.userInfo.username"></h5></div>
          </div>
        </div>

      </div>
    </div>
    <div class="col-md-8 col-xs-12">
      <div class="white-box">
        <form class="form-horizontal form-material">
          <div class="form-group">
            <label class="col-md-12">Full Name</label>
            <div class="col-md-12">
              <input type="text" name="fullname" v-model="input.fullname" placeholder="Johnathan Doe"
                     class="form-control form-control-line">
            </div>
          </div>
          <div class="form-group">
            <label for="example-email" class="col-md-12">Email</label>
            <div class="col-md-12">
              <input type="email" v-model="input.email" placeholder="johnathan@admin.com"
                     class="form-control form-control-line"
                     name="email" id="example-email"></div>
          </div>
          <div class="form-group">
            <label class="col-md-12">Password</label>
            <div class="col-md-12">
              <input type="password" name="password" v-model="input.password" v-on:change="setChangePassStatus()"
                     id="password_change_btn" disabled value="password" class="form-control form-control-line"></div>
          </div>

          <div class="form-group">
            <div class="col-sm-12">
              <button v-on:click="updateProfile()" class="btn btn-success">Update Profile</button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>

</template>

<script>
import axios from "axios";
import qs from "qs";

export default {
  name: "profile",
  data() {
    return {
      changePass : false,
      input: {
        fullname: this.$parent.userInfo.fullname,
        email: this.$parent.userInfo.email,
        password: "password"
      }
    }
  },
  methods: {
    setChangePassStatus(){
      this.changePass = true;
    },
    updateProfile() {
      let password = "";
      if (this.changePass == true) {
         password = this.input.password;
      }

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
          email: this.input.email,
          password: password
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