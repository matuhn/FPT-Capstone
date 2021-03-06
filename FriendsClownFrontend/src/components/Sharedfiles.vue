<template>
  <div class="row">
    <div class="col-md-12">
      <div class="white-box" style="padding-bottom: 70px;">
<!--        <nav aria-label="breadcrumb">-->
<!--          <ol class="breadcrumb">-->
<!--            <li class="breadcrumb-item">-->
<!--              <a href="/files">Home</a>-->
<!--            </li>-->
<!--            <li class="breadcrumb-item" v-for="(dir,idir) in listDir" :key="idir"><a-->
<!--                :href="'/files' + '?dir=' + getDir(idir)">{{ dir }}</a></li>-->
<!--          </ol>-->
<!--        </nav>-->
        <div class="table-responsive">
          <table style="margin-bottom: 100px;" class="table table-striped table-borderless table-hover">
            <thead>
            <tr>
              <th>
                <div class="checkbox checkbox-info">
                  <input id="c1" type="checkbox">
                  <label for="c1"></label>
                </div>
              </th>
              <th></th>
              <th style="width: 9999px;">Name</th>
              <th style="width: 300px;">Size</th>
              <th style="width: 700px;">Modified</th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="(item,i) in listFiles" :key="i">
              <td>
                <div class="checkbox checkbox-info">
                  <input :id="'cb'+item.file_name" type="checkbox">
                  <label :for="'cb'+item.file_name"></label>
                </div>
              </td>
              <td>
<!--                <i :class="'fa fa-' + getIcon(item.file_type)"></i>-->
              </td>
              <td class="">
                <a href="#"
                   class="text-link">{{
                    item.file_name.substring(9)
                  }}</a></td>
              <td>1 KB</td>
              <td>

<!--                {{ getTime(item.modified) }}-->
              </td>
            </tr>

            </tbody>
          </table>
        </div>
        <ul class="pagination">

        </ul>

      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
// import qs from "qs";

export default {
  name: "files",
  data() {
    return {
      url: '',
      listDir: '',
      currentDir: '',
      file: '',
      listFiles: '',
    }
  },
  mounted() {
    var dir = '/';
    if (this.$route.query.dir !== undefined) {
      var tmp = this.$route.query.dir;
      this.currentDir = tmp;
      if (tmp.charAt(0) == '/') {
        tmp = tmp.substring(1);
      }
      dir += tmp;
    }

    this.loadFiles();
    console.log(dir);
    this.listDir = dir.split("/");
    this.listDir.shift();
  },
  methods: {
    // getLink(file) {
    //   if (file.file_type === 'd') {
    //     if (this.currentDir === "") {
    //       return '/files?dir=' + this.currentDir + file.file_name;
    //     } else {
    //       return '/files?dir=' + this.currentDir + '/' + file.file_name;
    //     }
    //   } else {
    //     return this.$root.$data.host + '/api/downloadFile?' + file.download
    //   }
    // },
    getIcon(file_type) {
      switch (file_type) {
        case 'd' :
          return 'folder';
        default :
          return 'file'
      }
    },
    getTime(time) {
      let date = new Date(0);
      date.setUTCSeconds(time);
      return date.getUTCDate() + '/' + (date.getUTCMonth() + 1) + '/' + date.getUTCFullYear() + ' ' + date.getUTCHours() + ':' + date.getUTCMinutes() + ':' + date.getUTCSeconds();
    },
    getSharedList() {
      var input = this.shareForm.get_list;
      (async () => {
        await axios({
          headers: {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": true
          },
          withCredentials: true,
          method: "POST",
          "url": this.$root.$data.host + "/api/editFile",
          data: input
        }).then(result => {
          if (result.data.code == 200) {
            let tmp = result.data.result;
            if (tmp === '|') {
              this.shareForm.sharedList = null;
            } else {
              tmp = tmp.substring(1);
              tmp = tmp.slice(0, -1);
              this.shareForm.sharedList = tmp.split("|");
              const index = this.shareForm.sharedList.indexOf(this.$parent.$data.userInfo.username);
              if (index > -1) {
                this.shareForm.sharedList.splice(index, 1);
              }
            }
          }
        }, error => {
          console.error(error);
        });
      })();
    },
    loadFiles() {
      this.$parent.checkAuthenticaion();
      (async () => {
        await axios({
          headers: {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": true
          },
          withCredentials: true,
          method: "POST",
          "url": this.$root.$data.host + "/api/listSharedFile",
        }).then(result => {
          if (result.data.code == 200) {
            this.listFiles = JSON.parse(result.data.result.sharedFileList);
            console.log(this.listFiles);
          }
        }, error => {
          console.error(error);
        });
      })();
    },
    getDir(i) {
      var text = '';
      for (i = 0; i < (this.listDir.length); i++) {
        text = text + '/' + this.listDir[i];
      }
      return text;
    }
  }
}
</script>
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<style scoped>
.fa-ellipsis-h:hover {
  transform: scale(1.5);
}

.dropdown-menu > li > a {
  display: block;
  padding: 3px 20px;
  clear: both;
  font-weight: normal;
  line-height: 1.42857143;
  color: #333;
  white-space: nowrap;

}
</style>