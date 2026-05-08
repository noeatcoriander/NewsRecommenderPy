<template>
  <div class="main-container">
    <div class="main-title">
      <div class="title-name">修改信息</div>
    </div>
    <div class="main-content">
      <el-row :gutter="30">
        <el-col :span="5">
          <Menu/>
        </el-col>
        <el-col :span="19">
          <div class="content-right">
            <div>
              <el-form ref="formRef" :rules="data.formRules" :model="data.formModel" label-width="25%"
                       style="max-width: 90%" label-suffix="：">
                <el-row :gutter="10">
                  <el-col :span="5">
                    <el-form-item label-width="10%" style="margin-top: 10px;" prop="avatar">
                      <!--
                        element plus文件上传组件
                        action：文件上传服务端url地址
                        headers：配置文件上传请求头（添加请求参数）
                        accept：允许上传的文件类型
                        before-upload：文件上传前的钩子函数（上传文件格式、大小校验）
                        on-success：文件上传成功后的钩子函数
                        on-error：文件上传失败后的钩子函数
                        show-file-list：是否显示已上传文件列表
                      -->
                      <el-upload class="image-upload"
                                 :action="baseUrlGlobal + 'user/public/doUpload'"
                                 :headers="uploadHeaders"
                                 :accept="uploadImageTypesGlobal"
                                 :before-upload="handleUploadImageBefore"
                                 :on-success="doUploadSuccess"
                                 :on-error="doUploadError"
                                 :show-file-list="false">
                        <el-image v-if="data.formModel.avatar" :src="baseUploadUrlGlobal+data.formModel.avatar"
                                  fit="fill" style="width: 100%;"/>
                        <el-icon v-else class="image-uploader-icon">
                          <upload-filled/>
                        </el-icon>
                        <template #tip>
                          <div class="el-upload__tip">
                            点击图片上传<br>
                            {{ uploadImageTypesTipGlobal }} 格式<br>
                            最大 {{ uploadImageSizeLimitGlobal }} MB
                          </div>
                        </template>
                      </el-upload>
                    </el-form-item>
                  </el-col>
                  <el-col :span="19">
                    <el-form-item label="用户名" prop="loginname">
                      <el-input v-model.trim="data.formModel.loginname" maxlength="30"/>
                    </el-form-item>
                    <el-form-item label="姓名" prop="realname">
                      <el-input v-model.trim="data.formModel.realname" maxlength="30"/>
                    </el-form-item>
                    <el-form-item label="电话" prop="mobile">
                      <el-input v-model.trim="data.formModel.mobile" maxlength="11"
                                oninput="value=value.replace(/[^\d]/g,'')"/>
                    </el-form-item>
                    <el-form-item label="邮箱" prop="email">
                      <el-input v-model.trim="data.formModel.email" maxlength="50"/>
                    </el-form-item>
                    <el-form-item label="性别" prop="sex">
                      <el-radio-group v-model="data.formModel.sex">
                        <el-radio :value="1">男</el-radio>
                        <el-radio :value="2">女</el-radio>
                      </el-radio-group>
                    </el-form-item>
                    <el-form-item label="年龄" prop="age">
                      <el-input v-model.trim="data.formModel.age" maxlength="2"
                                oninput="value=value.replace(/[^\d]/g,'')"/>
                    </el-form-item>
                    <el-form-item label="个人简介" prop="introduction">
                      <el-input type="textarea" v-model.trim="data.formModel.introduction" :rows="6" maxlength="2000"/>
                    </el-form-item>
                  </el-col>
                </el-row>
                <div style="display: flex;justify-content: center;margin: 30px 0;">
                  <el-button type="warning" @click="doSubmit">提交</el-button>
                  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                  <el-button type="info" @click="router.push('/user/user/updatePassword')">修改密码</el-button>
                </div>
              </el-form>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import Menu from "@/components/user/Menu.vue"
import { reactive, ref } from 'vue'
import {
  baseUploadUrlGlobal,
  baseUrlGlobal,
  uploadImageSizeLimitGlobal,
  uploadImageTypesGlobal,
  uploadImageTypesTipGlobal
} from "@/tool/public"
import request from "@/tool/request"
import { useRouter } from "vue-router"
import { handleUploadImageBefore, handleValidateAge, handleValidateMobile } from "@/tool/tool"
import { useUserStore } from "@/store/userStore"
import { ElMessage } from "element-plus"

//获取全局路由器实例对象
const router = useRouter()
//获取当前登录用户的状态管理实例对象
const userStore = useUserStore()

//创建表单组件的引用实例对象，可调用表单的属性和方法
const formRef = ref()

//创建页面的响应式数据对象
const data = reactive({
  formModel: {}, //表单数据对象
  formRules: { //表单校验规则对象
    loginname: [
      { required: true, message: '请输入用户名', trigger: 'blur' },
      { min: 5, message: '长度最少5位', trigger: 'blur' }
    ],
    avatar: [
      { required: true, message: '请上传头像', trigger: 'blur' }
    ],
    realname: [
      { required: true, message: '请输入姓名', trigger: 'blur' }
    ],
    mobile: [
      { required: true, message: '请输入电话', trigger: 'blur' },
      { validator: handleValidateMobile, trigger: 'blur' } //电话格式校验
    ],
    email: [
      { required: true, message: '请输入邮箱', trigger: 'blur' },
      { type: 'email', message: '邮箱格式不正确', trigger: 'blur' } //邮箱格式校验
    ],
    sex: [
      { required: true, message: '请选择性别', trigger: 'blur' }
    ],
    age: [
      { required: true, message: '请输入年龄', trigger: 'blur' },
      { validator: handleValidateAge, trigger: 'blur' } //年龄格式校验
    ],
    introduction: [
      { required: true, message: '请输入个人简介', trigger: 'blur' }
    ]
  }
})

//提交数据
const doSubmit = () => {
  //校验表单数据
  formRef.value.validate((valid) => {
    if (valid) {
      //提交数据
      request.put('/user/user/doUpdate', data.formModel).then(res => {
        if (res.success > 0) {//操作成功
          userStore.doUpdate(res.user) //更新登录用户信息
          router.push('/user/user/detail') //跳转到个人信息页面
        }
      })
    }
  })
}

//创建图片上传请求的请求头数据对象，在上传图片请求的请求头中添加token
const uploadHeaders = ref({
  Authorization: 'Bearer ' + userStore.token //添加token参数
})

//创建图片上传成功函数
const doUploadSuccess = (res) => {
  ElMessage.success("上传成功！!")
  data.formModel.avatar = res.newFileName //获取新图片名称并回显
}

//创建图片上传失败函数
const doUploadError = (res) => {
  console.info(res)
  ElMessage.error("上传失败！!")
}

//加载用户信息
const loadData = () => {
  //请求数据
  request.get('/user/user/detail').then(res => {
    data.formModel = res.user //用户数据
  })
}

//加载数据
loadData()
</script>

<style scoped>

</style>