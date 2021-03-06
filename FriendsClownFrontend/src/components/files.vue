<template>
  <div class="row">
    <div class="col-md-12">
      <div class="white-box" style="padding-bottom: 70px;">
        <nav aria-label="breadcrumb">
          <ol class="breadcrumb">
            <li class="breadcrumb-item">
              <a href="/files">Home</a>
            </li>
            <li class="breadcrumb-item" v-for="(dir,idir) in listDir" :key="idir"><a
                :href="'/files' + '?dir=' + getDir(idir)">{{ dir }}</a></li>
          </ol>
        </nav>
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
              <th style="width: 500px;"></th>
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
                <i :class="'fa fa-' + getIcon(item.file_type)"></i>
              </td>
              <td class="">
                <a :href="getLink(item)"
                   class="text-link">{{
                    item.file_name.substring(9)
                  }}</a></td>
              <td class="dropdown open text-center"><a class="dropdown-toggle" data-toggle="dropdown" role="button"
                                                       v-on:click="$root.activeToggle('togglefile'+i)"
                                                       aria-haspopup="true" aria-expanded="false"><i
                  class="dropdown-toggle fa fa-ellipsis-h"></i></a>
                <ul :id="'togglefile' + i" class="dropdown-menu animated flipInY" style="top: 50px; display: none">
                  <li><a role="button" v-on:click="editFileIn(item)"><i class="fa fa-edit"> Edit file's name</i></a>
                  </li>
                  <li><a role="button" v-on:click="shareFileIn(item)"><i class="fa fa-share"> Share file</i></a></li>
                  <li role="separator" class="divider"></li>
                  <li><a role="button" v-on:click="deleteFileIn(item)"><i class="fa fa-trash-o text-danger"> Delete</i></a>
                  </li>
                </ul>
              </td>
              <td>{{Number((item.size/1000).toFixed(0))}} KB</td>
              <td>{{ getTime(item.modified) }}</td>
            </tr>

            </tbody>
          </table>
        </div>
        <ul class="pagination">

        </ul>

        <div class="row" style="display: none" id="processbar">
          <div class="col-md-10"></div>
          <div class="col-md-2">
            <b-progress :max="100" height="3rem">
              <b-progress-bar :value="uploadPercentage" style="padding: 8px;">
                <span style=" margin-top: 5px"><strong style="color: white;">{{ uploadPercentage }} / {{ 100 }}</strong></span>
              </b-progress-bar>
            </b-progress>
          </div>
        </div>

        <input style="display: none" type="file" multiple id="file" ref="file" v-on:change="handleFileUpload()"/>
        <div class="dropdown open text-center">
          <button type="button" v-on:click="$root.activeToggle('addFile')" style=" border: 2px solid #e5ebec;
    width: 45px;
    height: 45px;
    border-radius: 100%;
    line-height: 28px;" class="btn btn-success dropdown-toggle pull-right m-t-10 font-20" data-toggle="dropdown"
                  aria-haspopup="true" aria-expanded="false">+
          </button>

          <ul :id="'addFile'" class="dropdown-menu animated flipInY pull-right" style="top: 50px; display: none">
            <li><a role="button" v-on:click="createFolderIn(item)"><i class="fa fa-folder"> Create New Folder</i></a>
            </li>
            <li role="separator" class="divider"></li>
            <li><a role="button" v-on:click="addFile()"><i class="fa fa-file"> Upload File</i></a></li>
          </ul>
        </div>


        <div id="editNameModal" class="modal fade" style="background-color: rgba(0,0,0,0.4);" tabindex="-1"
             role="dialog" aria-labelledby="editFileName"
             aria-hidden="true">
          <div class="modal-dialog">
            <div class="modal-content">
              <div class="modal-header">
                <button type="button" class="close" v-on:click="editFileOut()" data-dismiss="modal" aria-hidden="true">
                  x
                </button>
                <h4 class="modal-title" id="editFileNameModalLabel">{{ editForm.title }}</h4></div>
              <div class="modal-body" style="min-height: 100px">
                <div class="form-group">
                  <label class="col-md-12">Name</label>
                  <div class="col-md-12">
                    <input type="text" name="name" v-model="editForm.name"
                           class="form-control">
                  </div>
                </div>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-info waves-effect" data-dismiss="modal"
                        v-on:click="editFileSubmit()">Submit
                </button>
              </div>
            </div>
          </div>
        </div>

        <div id="deleteModal" class="modal fade" style="background-color: rgba(0,0,0,0.4);" tabindex="-1"
             role="dialog" aria-labelledby="deleteFile"
             aria-hidden="true">
          <div class="modal-dialog">
            <div class="modal-content">
              <div class="modal-header">
                <button type="button" class="close" v-on:click="deleteFileOut()" data-dismiss="modal"
                        aria-hidden="true">
                  x
                </button>
                <h4 class="modal-title" id="deleteFileModalLabel">Delete File</h4></div>
              <div class="modal-body" style="min-height: 100px">
                <div class="form-group">
                  <p>Do you want to delete this file (<b>{{ editForm.name }}</b>) ?</p>
                </div>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-danger waves-effect" data-dismiss="modal"
                        v-on:click="editFileSubmit()">Delete
                </button>
                <button type="button" class="btn btn-default waves-effect" data-dismiss="modal"
                        v-on:click="deleteFileOut()">Cancle
                </button>
              </div>
            </div>
          </div>
        </div>

        <div id="shareModal" class="modal fade" style="background-color: rgba(0,0,0,0.4);" tabindex="-1"
             role="dialog" aria-labelledby="editFileName"
             aria-hidden="true">
          <div class="modal-dialog">
            <div class="modal-content">
              <div class="modal-header">
                <button type="button" class="close" v-on:click="shareFileOut()" data-dismiss="modal" aria-hidden="true">
                  x
                </button>
                <h4 class="modal-title" id="shareModalLabel">Share with people and groups </h4></div>
              <div class="modal-body" style="min-height: 100px">
                <div class="form-group">
                  <div class="col-md-10">
                    <multiselect v-model="shareForm.seleted" :options="shareForm.users" :multiple="true"
                                 :close-on-select="false" :clear-on-select="false" :preserve-search="true"
                                 placeholder="Select peoples or groups" :preselect-first="true">
                    </multiselect>
                  </div>
                  <div class="col-md-2">
                    <button style="margin-top: 2px; margin-left: 25px" v-on:click="shareFileAdd()"
                            class="btn btn-info waves-effect">Add
                    </button>
                  </div>
                </div>
                <br><br>
                <div class="form-group">
                  <table class="table table-striped table-hover">
                    <thead>
                    <tr>
                      <th style="width: 1000px; text-align: center">Name</th>
                      <th style="width: 100px; text-align: center">Role</th>
                      <th style="width: 100px; text-align: center">Action</th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr style="color: black">
                      <td style="text-align: left"><b>{{ $parent.$data.userInfo.username }}</b></td>
                      <td style="text-align: right">Owner</td>
                      <td style="text-align: center;"></td>
                    </tr>
                    <tr v-for="(user,i) in shareForm.sharedList" :key="i">
                      <td style="text-align: left"><b>{{ user }}</b></td>
                      <td style="text-align: right">Viewer</td>
                      <td style="text-align: center;">
                        <button type="button" class="btn btn-danger waves-effect" data-dismiss="modal"
                                v-on:click="revolkShareFile(user)">Revoke
                        </button>
                      </td>
                    </tr>
                    </tbody>
                  </table>
                </div>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-info waves-effect" data-dismiss="modal"
                        v-on:click="shareFileOut()">Submit
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import qs from "qs";
import Multiselect from 'vue-multiselect'

export default {
  components: {
    Multiselect
  },
  name: "files",
  data() {
    return {
      url: '',
      listDir: '',
      currentDir: '',
      file: '',
      uploadPercentage: 0,
      listFiles: '',
      editForm: {
        type: 0,
        file: '',
        name: '',
        title: '',
        link: '',
      },
      shareForm: {
        users: '',
        file: '',
        link: '',
        get_list: '',
        sharedList: '',
        revoke_link: '',
        seleted: null
      }
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
    getLink(file) {
      if (file.file_type === 'd') {

        if (this.currentDir === "") {
          return '/files?dir=' + this.currentDir + file.file_name;
        } else {
          return '/files?dir=' + this.currentDir + '/' + file.file_name;
        }
      } else {
        return this.$root.$data.host + '/api/downloadFile?' + file.download
      }
    },
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
    handleFileUpload() {
      this.file = this.$refs.file.files[0];
      this.submitFile();
    },
    addFile() {
      window.$('#file').trigger('click');
    },
    submitFile() {
      let formData = new FormData();
      // for (var i = 0; i < this.files.length; i++) {
      //   let file = this.files[i];
      //
      //   formData.append('files[' + i + ']', file);
      // }
      formData.append('file', this.file);
      formData.append('dir', this.currentDir);
      window.$('#processbar').show();
      (async () => {
        await axios.post(this.$root.$data.host + '/api/uploadFile',
            formData,
            {
              headers: {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": true,
                'Content-Type': 'multipart/form-data',
              },
              onUploadProgress: function (progressEvent) {
                this.uploadPercentage = parseInt(Math.round((progressEvent.loaded / progressEvent.total) * 100));
              }.bind(this),
              withCredentials: true,
            }
        ).then(result => {
          if (result.data.code == 200) {
            console.log('UPLOAD SUCCESS!!');
            this.uploadPercentage = 0;
            window.$('#processbar').hide();
            this.loadFiles();
          }
        }, error => {
          console.error(error);
        });
      })();
    },
    editFileIn(file) {
      var filename = file.file_name.substring(9);
      this.editForm.file = file.download;
      this.editForm.name = filename;
      this.editForm.title = 'Edit File\'s Name';
      this.editForm.type = 0;
      this.editForm.link = file.rename;
      var modal = window.$('#editNameModal');
      modal.addClass('in');
      modal.show();
    },
    shareFileIn(file) {
      var filename = file.file_name.substring(9);
      this.shareForm.file = filename;
      this.shareForm.link = file.share;
      this.shareForm.get_list = file.list_share;
      this.shareForm.revoke_link = file.revoke;
      this.getSharedList();
      this.getListUser();
      var modal = window.$('#shareModal');
      modal.addClass('in');
      modal.show();
    },
    getListUser() {
      (async () => {
        await axios({
          headers: {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": true
          },
          withCredentials: true,
          method: "POST",

          "url": this.$root.$data.host + "/api/listUser",
        }).then(result => {
          if (result.data.code == 200) {
            this.shareForm.users = result.data.result.userList;
            for (let i = 0; i < this.shareForm.sharedList.length; i++) {
              let tmp = this.shareForm.sharedList[i];
              const index = this.shareForm.users.indexOf(tmp);
              if (index > -1) {
                this.shareForm.users.splice(index, 1);
              }
            }
            const index = this.shareForm.users.indexOf(this.$parent.$data.userInfo.username);
            if (index > -1) {
              this.shareForm.users.splice(index, 1);
            }
          }
        }, error => {
          console.error(error);
        });
      })();
    },
    createFolderIn() {
      this.editForm.name = '';
      this.editForm.title = 'Create New Folder'
      this.editForm.type = 2;
      var modal = window.$('#editNameModal');
      modal.addClass('in');
      modal.show();
    },
    editFileOut() {
      var modal = window.$('#editNameModal');
      modal.removeClass('in');
      modal.hide();
    },
    shareFileOut() {
      var modal = window.$('#shareModal');
      modal.removeClass('in');
      modal.hide();
    },
    deleteFileIn(file) {
      var filename = file.file_name.substring(9);
      this.editForm.file = file.download;
      this.editForm.name = filename;
      this.editForm.type = 1;
      this.editForm.link = file.delete;
      var modal = window.$('#deleteModal');
      modal.addClass('in');
      modal.show();
    },
    deleteFileOut() {
      var modal = window.$('#deleteModal');
      modal.removeClass('in');
      modal.hide();
    }
    ,
    createNewFolder() {
      var dir = (this.currentDir === '' ? '' : this.currentDir + '/') + this.editForm.name;
      var input = qs.stringify({
        dir: dir
      });
      (async () => {
        await axios({
          headers: {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": true
          },
          withCredentials: true,
          method: "POST",
          "url": this.$root.$data.host + "/api/createDirectory",
          data: input
        }).then(result => {
          if (result.data.code == 200) {
            console.log('EDIT SUCCESS!!');
            this.loadFiles();
            this.editFileOut();
            this.deleteFileOut();
          }
        }, error => {
          console.error(error);
        });
      })();
    },
    shareFileAdd() {
      var userList = this.shareForm.seleted.join('|');
      userList = '|' + userList + '|';
      var input = this.shareForm.link + userList;
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
            console.log('Share SUCCESS!!');
            this.getSharedList();
            this.getListUser();
            this.shareForm.seleted = '';
          }
        }, error => {
          console.error(error);
        });
      })();

    },
    revolkShareFile(user) {
      var userList = '|' + user + '|';
      var input = this.shareForm.revoke_link + userList;
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
            console.log('REVOLK SUCCESS!!');
            this.getSharedList();
            this.getListUser();
            this.shareForm.seleted = '';
          }
        }, error => {
          console.error(error);
        });
      })();

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
    editFileSubmit() {
      if (this.editForm.type == 2) {
        this.createNewFolder();
        return;
      }
      var input = this.editForm.link + this.editForm.name;
      if (this.editForm.type == 1) {
        input = this.editForm.link
      }
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
            console.log('EDIT SUCCESS!!');
            this.loadFiles();
            this.editFileOut();
            this.deleteFileOut();
          }
        }, error => {
          console.error(error);
        });
      })();

    },
    loadFiles() {
      this.$parent.checkAuthenticaion();
      var input = qs.stringify({
        dir: this.currentDir,
      });
      (async () => {
        await axios({
          headers: {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": true
          },
          data: input,
          withCredentials: true,
          method: "POST",
          "url": this.$root.$data.host + "/api/listFile",
        }).then(result => {
          if (result.data.code == 200) {
            this.listFiles = JSON.parse(result.data.result.fileList);
            console.log('SUCCESS!!');
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