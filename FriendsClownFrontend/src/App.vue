<template>
  <div class="vue-template">
    <div class="App">
      <div class="vertical-center" v-if="!authenticated">
        <div class="inner-block">
          <router-view @authenticated="setAuthenticated"/>
        </div>
      </div>
      <div class="wrapper" v-if="authenticated">
        <nav class="navbar navbar-default navbar-static-top m-b-0" style="padding:  0px;">
          <div class="navbar-header">
            <div class="top-left-part">
              <a class="logo" href="index.html">
                <b>
                  <img src="./assets/images/logo.png" alt="Friends"/>
                </b>
                <span>
                            <img src="./assets/images/logo_text.png" alt="Cloud" class="dark-logo"/>
                        </span>
              </a>
            </div>
            <ul class="nav navbar-top-links navbar-left hidden-xs">
              <li>
                <form role="search" class="app-search hidden-xs">
                  <i class="icon-magnifier"></i>
                  <input type="text" placeholder="Search..." class="form-control">
                </form>
              </li>
            </ul>
            <ul class="nav navbar-top-links navbar-right pull-right">
              <li class="right-side-toggle">
                <a class="dropdown-toggle waves-effect waves-light b-r-0 font-20" data-toggle="dropdown" role="button"
                   v-on:click="$root.activeToggle('toggleProfile')"
                   aria-haspopup="true" aria-expanded="false">
                  <i class="icon-user dropdown-toggle"></i>
                </a>
                <ul id="toggleProfile" class="dropdown-menu animated flipInY">
                  <li class="text-center"><b v-html="userInfo.fullname"></b></li>
                  <li role="separator" class="divider"></li>
                  <li>
                    <router-link to="/profile"><i class="fa fa-user"></i> Profile</router-link>
                  </li>

                  <li role="separator" class="divider"></li>
                  <li><a href="#" v-on:click="logout()"><i class="fa fa-power-off"></i> Logout</a></li>
                </ul>
              </li>
            </ul>
          </div>
        </nav>
        <aside class="sidebar" style="position: relative; margin-top: 0px">
          <div class="scroll-sidebar">
            <nav class="sidebar-nav">
              <ul id="side-menu">
                <li>
                  <router-link class="waves-effect" to="/dashboard" active-class="active waves-effect"><i class="icon-screen-desktop fa-fw"></i> <span class="hide-menu"> Dashboard </span></router-link>
                </li>
                <li>
                  <router-link class="waves-effect" to="/files" active-class="active waves-effect" aria-expanded="false"><i
                      class="icon-folder fa-fw"></i> <span class="hide-menu">File</span></router-link>
                  <ul aria-expanded="false" class="collapse">
                    <li><router-link class="waves-effect" to="/files" active-class="active waves-effect"><i class="icon-folder fa-fw"></i> All files</router-link></li>
                    <li><router-link class="waves-effect" to="/recentfiles" active-class="active waves-effect"><i class="icon-clock fa-fw"></i> Recent</router-link></li>
                    <li><router-link class="waves-effect" to="/favorites" active-class="active waves-effect"><i class="icon-star fa-fw"></i> Favorites</router-link></li>
                    <li><router-link class="waves-effect" to="/shares" active-class="active waves-effect"><i class="icon-share fa-fw"></i> Shares</router-link></li>
                    <li><router-link class="waves-effect" to="/tags" active-class="active waves-effect"><i class="icon-tag fa-fw"></i> Tags</router-link></li>
                  </ul>
                </li>
                <li>
                  <router-link class="waves-effect" to="/contacts" active-class="active waves-effect" aria-expanded="false"><i
                      class="icon-user-follow fa-fw"></i> <span class="hide-menu"> Contact</span></router-link>
                  <ul aria-expanded="false" class="collapse">
                    <li><router-link class="waves-effect" to="/contacts" active-class="active waves-effect"><i class="icon-user fa-fw"></i> All Contact</router-link></li>
                  </ul>
                </li>
              </ul>
            </nav>
          </div>
        </aside>

        <div class="page-wrapper" style="padding-top: 0px">
          <div class="container-fluid" style="min-height:  915px">
            <router-view/>
          </div>
          <footer class="footer t-a-c">
            © 2020 Friend Clown
          </footer>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import JQuery from 'jquery';

window.$ = JQuery;
import axios from "axios";


export default {
  name: 'App',
  data() {
    return {
      authenticated: false,
      userInfo: {
        id: "",
        username: "",
        fullname: "",
        email: ""
      }
    }
  },
  mounted() {
    this.checkAuthenticaion();

    window.$(document).click(function(e) {
      var target = window.$( e.target );
      if ( !target.is( "ul" ) && !target.hasClass('dropdown-toggle')) {
        window.$('.dropdown-menu').hide();
      }
    });
  },
  methods: {
       setAuthenticated(status) {
      this.authenticated = status;
    },
    logout() {
      axios({
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Credentials" : true
        },
        withCredentials: true,
        method: "POST",
        "url": this.$root.$data.host + "/api/auth/logout",
      }).then(result => {
        if (result.data.code == 200) {
          this.setAuthenticated(false);
          this.$router.replace({name: "login"});
        } else {
          this.message = '<p class=\'text-danger text-right\'>' + result.data.result + '</p>';
        }
      }, error => {
        console.error(error);
      });
    },
    checkAuthenticaion() {
      axios({
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Credentials": true
        },
        withCredentials: true,
        method: "POST",
        "url": this.$root.$data.host + "/api/auth/getUserInfo"
      }).then(result => {
        if (result.data.code == 200) {
          this.authenticated = true;
          this.userInfo.id = result.data.result.id;
          this.userInfo.username = result.data.result.username;
          this.userInfo.fullname = result.data.result.fullname;
          this.userInfo.email = result.data.result.email;
        } else {
          this.authenticated = false;
          this.$router.replace({name: "login"});
        }
      }, error => {
        console.log(error);
        this.$router.replace({name: "notfound"});
      });
    }
  }
}
</script>

<style>
body {
  background-color: #F0F0F0;
}

h1 {
  padding: 0;
  margin-top: 0;
}

#app {
  width: 1024px;
  margin: auto;
}
</style>